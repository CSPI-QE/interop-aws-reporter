import subprocess
from typing import Any
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def execute_dry_run(logger: Any) -> None:
    cloudwash_output = subprocess.run(["poetry", "run", "swach", "-d", "aws", "--ocps"], capture_output=True, text=True)

    if cloudwash_output.returncode != 0:
        raise Exception(f"CloudWash execution failed: {cloudwash_output.stderr}")
    else:
        cleanup_log_path = "cleanup_resource_AWS.html"
        if os.path.exists(cleanup_log_path):
            message = f"Output saved to: {cleanup_log_path}"
            logger.info(message)
        else:
            logger.error("Couldn't find cleanup output log!")
            exit(1)


def send_log_file_with_bot(logger: Any, message: str = "") -> None:
    file_name = "./cleanup_resource_AWS.html"
    if not message:
        message = "Here's cloudwash weekly cleanup log file :smile:\n*Watch report using: * `Open in new window`"

    # ID of channel to upload file to
    channel_id = os.environ.get("CHANNEL_ID")
    if not channel_id:
        logger.error("Missing env var. CHANNEL_ID is required.")
        exit(1)
    slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
    if not slack_bot_token:
        logger.error("Missing env var. SLACK_BOT_TOKEN is required.")
        exit(1)

    try:
        client = WebClient(token=slack_bot_token)
    except:
        logger.error("Couldn't get SlackAPI client, please check token value.")
        raise

    try:
        # Post cleanup log file in the Channel
        result = client.files_upload_v2(
            channel=channel_id,
            initial_comment=message,
            file=file_name,
        )
        # Log the result
        logger.info(result)
    except SlackApiError as e:
        logger.error("Error uploading file: {}".format(e))
        raise

    logger.info("Message sent successfully")
