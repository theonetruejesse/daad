from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.daad.constants import DAILY_LOG_CHANNEL


class DiscordMessage(BaseModel):
    channel_id: int
    content: str


class LogMessage(BaseModel):
    content: str


class ServerRouter:
    def __init__(self):
        self.app = FastAPI(title="Dasein API")
        self.setup_routes()

    def setup_routes(self):
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint"""
            return {"status": "healthy"}

        @self.app.post("/discord/message")
        async def send_discord_message(message: DiscordMessage):
            """Send a message to a Discord channel"""
            try:
                await self.publish_discord_message(
                    channel_id=message.channel_id, content=message.content
                )
                return {
                    "status": "success",
                    "message": "Discord message queued for delivery",
                }
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Failed to send Discord message: {str(e)}"
                )

        @self.app.post("/discord/log")
        async def send_log_message(message: LogMessage):
            """Send a message to the daily log channel"""
            try:
                await self.publish_discord_message(
                    channel_id=DAILY_LOG_CHANNEL, content=message.content
                )
                return {
                    "status": "success",
                    "message": "Log message queued for delivery",
                }
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Failed to send log message: {str(e)}"
                )

        @self.app.get("/discord")
        async def send_log():
            """Send a message to the daily log channel"""
            try:
                await self.publish_discord_message(
                    channel_id=DAILY_LOG_CHANNEL, content="Hello"
                )
                return {
                    "status": "success",
                    "message": "Log message queued for delivery",
                }
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Failed to send log message: {str(e)}"
                )

    def get_app(self):
        return self.app
