import subprocess
import tempfile
from typing import Any
from utils import send_slack_message
import os

AWS_CLIENT_REGION = "us-east-1"


def aws_report(logger: Any, message: str = "") -> None:
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


def dry_run(logger: Any) -> None:
    # aws_access_id = os.environ.get("AWS_ACCESS_KEY","")
    # aws_secret_key = os.environ.get("AWS_SECRET_KEY","")
    # aws_client_region = os.environ.get("AWS_CLIENT_REGION",AWS_CLIENT_REGION)
    #
    # if not all(aws_access_id, aws_secret_key):
    #     raise "AWS creds are missing!"

    cloudwash_output = subprocess.run(["poetry", "run", "swach", "--help"], capture_output=True, text=True)

    if cloudwash_output.returncode != 0:
        raise Exception(f"CloudWash execution failed: {cloudwash_output.stderr}")
    else:
        swach_output = cloudwash_output.stdout

        logger.info(swach_output)

        # Create a temporary file to store the logs
        with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
            tmpfile.write(swach_output.encode())
            tmpfile_path = tmpfile.name

            message = f"Output saved to: {tmpfile_path}"
            logger.info(message)
            aws_report(logger=logger, message=message)
