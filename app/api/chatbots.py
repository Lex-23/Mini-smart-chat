from fastapi import APIRouter, HTTPException, Request
from models import User, ChatBot
from typing import List
from beanie import PydanticObjectId
from services import list_chatbots, get_chatbot, update_chatbot, create_chatbot, delete_chatbot, text_to_bot

router = APIRouter()


@router.get('/chatbots', status_code=200)
async def list() -> List[ChatBot]:
    return await list_chatbots()

    
@router.post('/chatbots', status_code=201)
async def create(request: Request, data: dict) -> dict:
    data["owner"] = request.user
    data["owner_username"] = request.user.username
    bot = ChatBot(**data)
    await create_chatbot(bot)
    return {"message": f"Chatbot <{bot.name}> has been saved"}


@router.get('/chatbots/{bot_id}', status_code=200)
async def retreive(bot_id: PydanticObjectId) -> ChatBot:
    bot = await get_chatbot(bot_id)
    if bot is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return bot


@router.put('/chatbots/{bot_id}', status_code=200)
async def update(bot_id: PydanticObjectId, data: dict) -> ChatBot:
    bot_to_update = await get_chatbot(bot_id)
    if not bot_to_update:
        raise HTTPException(status_code=404, detail="Resource has not found")
    return await update_chatbot(bot=bot_to_update, data=data)


@router.delete('/chatbots/{bot_id}', status_code=204)
async def delete(bot_id: PydanticObjectId) -> None:
    bot_to_delete = await get_chatbot(bot_id)
    if not bot_to_delete:
        raise HTTPException(status_code=404, detail="Resource has not found")
    await delete_chatbot(bot_to_delete)

@router.post('/chatbots/{bot_id}/text', status_code=201)
async def send_message(request: Request, bot_id: PydanticObjectId, data: dict) -> dict:
    bot = await get_chatbot(bot_id)
    user = request.user
    response = await text_to_bot(user=user, bot=bot, msg=data['msg'])
    return {"message": response}
