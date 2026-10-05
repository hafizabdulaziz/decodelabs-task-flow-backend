"""
AI Chat Assistant API router for natural language processing and automated action execution.
"""

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.services.external_service import ExternalService
from app.models.task import TaskModel
from app.models.user import UserModel
from app.core.security import hash_password
from app.schemas.error import ErrorResponse

router = APIRouter(prefix="/chat", tags=["AI Chat Assistant"])

STANDARD_RESPONSES = {
    400: {"model": ErrorResponse, "description": "Bad Request"},
    401: {"model": ErrorResponse, "description": "Unauthorized"},
    403: {"model": ErrorResponse, "description": "Forbidden"},
    404: {"model": ErrorResponse, "description": "Not Found"},
    422: {"model": ErrorResponse, "description": "Validation Error"},
    429: {"model": ErrorResponse, "description": "Rate Limit Exceeded"},
    500: {"model": ErrorResponse, "description": "Internal Server Error"},
}


class ChatRequest(BaseModel):
    prompt: str = Field(..., description="Natural language prompt from user", example="Create task Buy groceries")


class ChatResponse(BaseModel):
    reply: str = Field(..., description="AI Assistant response text")
    action_executed: str = Field(..., description="Summary of action performed, if any")
    data: dict = Field(default_factory=dict, description="Related action payload data")


@router.post(
    "/assistant",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    responses={200: {"model": ChatResponse, "description": "AI prompt successfully processed"}, **STANDARD_RESPONSES},
    summary="AI Chat Assistant Prompt Execution",
    description="AI Chat Assistant that interprets natural language commands (create task, register user, check weather, system status) and performs automated backend operations.",
)
async def chat_assistant(req: ChatRequest, db: AsyncSession = Depends(get_db)):
    """
    AI Chat Assistant that interprets natural language commands (create task, register user, check weather, system status)
    and performs automated backend operations.
    """
    prompt_lower = req.prompt.lower().strip()
    
    # 1. Weather / Third-party integration query
    if "weather" in prompt_lower or "forecast" in prompt_lower:
        weather_data = await ExternalService.fetch_weather()
        return ChatResponse(
            reply=f"Current weather at {weather_data.location}: {weather_data.temperature_celsius}°C, {weather_data.condition}.",
            action_executed="fetch_weather",
            data=weather_data.model_dump()
        )

    # 2. Create task command: e.g., "create task Buy groceries" or "add task finish report"
    elif "create task" in prompt_lower or "add task" in prompt_lower:
        title = req.prompt.replace("create task", "", 1).replace("add task", "", 1).strip()
        if not title:
            title = "New AI Generated Task"
        
        user_res = await db.execute(select(UserModel).limit(1))
        user = user_res.scalars().first()
        if not user:
            user = UserModel(
                email="ai_default_user@decodelabs.com",
                hashed_password=hash_password("password123"),
                full_name="AI Default User",
                is_active=True
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)

        new_task = TaskModel(
            title=title,
            description="Created automatically via AI Chat Assistant",
            owner_id=user.id
        )
        db.add(new_task)
        await db.commit()
        await db.refresh(new_task)
        
        return ChatResponse(
            reply=f"Task '{title}' successfully created with ID {new_task.id}!",
            action_executed="create_task",
            data={"id": new_task.id, "title": new_task.title}
        )

    # 3. Register user command: e.g., "register user test@example.com"
    elif "register user" in prompt_lower or "create user" in prompt_lower:
        parts = req.prompt.split()
        email = "ai_user@example.com"
        for p in parts:
            if "@" in p:
                email = p
                break
        
        existing = await db.execute(select(UserModel).where(UserModel.email == email))
        if existing.scalars().first():
            return ChatResponse(
                reply=f"User with email {email} already exists.",
                action_executed="user_exists",
                data={"email": email}
            )

        new_user = UserModel(email=email, hashed_password=hash_password("password123"), is_active=True, is_superuser=False)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return ChatResponse(
            reply=f"User {email} successfully registered via AI Assistant! (Default password: password123)",
            action_executed="register_user",
            data={"id": new_user.id, "email": new_user.email}
        )

    # 4. System status / general help
    elif "status" in prompt_lower or "health" in prompt_lower or "system" in prompt_lower:
        return ChatResponse(
            reply="System is healthy, FastAPI server running with Async PostgreSQL and Third-Party Weather Facade active.",
            action_executed="system_status",
            data={"status": "healthy", "environment": "development"}
        )

    # 5. Default conversational fallback
    else:
        return ChatResponse(
            reply="Hello! I am your DecodeLabs AI Assistant. You can ask me to 'check weather', 'create task [title]', 'register user [email]', or check 'system status'.",
            action_executed="none",
            data={}
        )
