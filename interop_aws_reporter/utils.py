import json
import requests
import os
from typing import Any
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


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


def send_log_file(logger: Any) -> None:
    # file_name = "./cleanup_resource_AWS.html"
    file_name = "./cleanup.log"
    # ID of channel to upload file to
    channel_id = os.environ.get("CHANNEL_ID")
    if not channel_id:
        logger.error("Missing env var. CHANNEL_ID is required.")
        raise

    slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
    if not slack_bot_token:
        logger.error("Missing env var. SLACK_BOT_TOKEN is required.")
        raise

    try:
        client = WebClient(token=slack_bot_token)
    except:
        logger.error("Couldn't get SlackAPI client, please check token value.")
        raise

    try:
        # Post cleanup log file in the Channel
        result = client.files_upload_v2(
            channel=channel_id,
            initial_comment="Here's cloudwash cleanup log file :smile:",
            file=file_name,
        )
        # Log the result
        logger.info(result)

    except SlackApiError as e:
        logger.error("Error uploading file: {}".format(e))
        raise

    logger.info("Message sent successfully")
