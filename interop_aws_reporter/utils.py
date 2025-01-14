import json
import requests
import os
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


def aws_report_message_with_webhook(logger: Any, message: str = "") -> None:
    if not message:
        message = (
            "Hello :wave:, here is the weekly run report for [...] .\nAWS Reporting is cool! (sent from Openshift-Ci)"
        )
    slack_webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    if not slack_webhook_url:
        logger.error("Missing env var. SLACK_WEBHOOK_URL is required.")
        raise

    if slack_webhook_url:
        send_slack_message(
            message=message,
            webhook_url=slack_webhook_url,
            logger=logger,
        )
    logger.info("Message sent")
