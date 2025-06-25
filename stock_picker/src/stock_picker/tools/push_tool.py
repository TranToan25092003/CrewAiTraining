from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import requests

class PushNotificationInput(BaseModel):
    """A message to be sent to the user."""
    message: str = Field(..., description="Message to be sent to the user.")

class PushNotificationTool(BaseTool):
    name: str = "Send a push notification"
    description: str = (
        "this tool is used to send a push notification to the user"
    )
    args_schema: Type[BaseModel] = PushNotificationInput

    def _run(self, message: str) -> str:
        # Implementation goes here
        return "This text appear mean message sent to the user successfully."
