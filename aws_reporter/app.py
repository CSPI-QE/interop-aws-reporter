import os
from typing import Any
import json
import requests
from simple_logger.logger import get_logger

logger = get_logger(name=__name__)

# docker build -t aws_reporter .
# docker run -p 8000:8000 --env-file .development/.env aws_reporter:latest
# docker run -it -p 8000:8000 --env-file .development/.env aws_reporter:latest /bin/bash


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
            logger.info(f"Slack message sent successfully: {response.text}")
    except Exception as ex:
        logger.error(f"Failed to send slack message. error: {ex}")


def aws_report() -> Any:
    message = "Hello :wave:, here is the weekly run report for [...] .\nAWS Reporting is cool from a container!"
    slack_webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    if not slack_webhook_url:
        return {"error": "slack_errors_webhook_url is required"}, 400

    if slack_webhook_url:
        send_slack_message(
            message=message,
            webhook_url=slack_webhook_url,
            logger=logger,
        )
    return {"status": "message sent"}, 200


if __name__ == "__main__":
    # dry_run(logger)
    # aws_report()
    print("Cool App")
