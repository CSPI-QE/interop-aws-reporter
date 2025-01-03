import subprocess
from typing import Any
from utils import send_slack_message, send_log_file
import os


def aws_report_message(logger: Any, message: str = "") -> None:
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
    cloudwash_output = subprocess.run(["poetry", "run", "swach", "-d", "aws", "--ocps"], capture_output=True, text=True)

    if cloudwash_output.returncode != 0:
        raise Exception(f"CloudWash execution failed: {cloudwash_output.stderr}")
    else:
        cleanup_log_path = "cleanup_resource_AWS.html"
        if os.path.exists(cleanup_log_path):
            # with open(cleanup_log_path) as log:
            #     print(log.read())

            # logger.info(cloudwash_output.stderr)
            message = f"Output saved to: {cleanup_log_path}"
            logger.info(message)
            # aws_report_message(logger=logger, message=message)
            send_log_file(logger=logger)
