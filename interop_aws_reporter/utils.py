import json
import requests
from typing import Any


def send_slack_message(message: str, webhook_url: str, logger: Any) -> None:
    try:
        if webhook_url:
            slack_data = {"text": message}
            logger.info(f"Sending message to slack: {message}")
            response = requests.post(
                webhook_url,
                data=json.dumps(slack_data),
                headers={"Content-Type": "application/json"},
            )
            if response.status_code != 200:
                logger.error(
                    f"Request to slack returned an error {response.status_code} with the following message: {response.text}"
                )
                raise
            logger.info(f"Slack message sent successfully: {response.text}")
    except Exception as ex:
        logger.error(f"Failed to send slack message. error: {ex}")
        raise
