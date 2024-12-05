import os
from typing import Any
from simple_logger.logger import get_logger
from utils import send_slack_message

logger = get_logger(name=__name__)


def aws_report() -> Any:
    message = "Hello :wave:, here is the weekly run report for [...] .\nAWS Reporting is cool! (sent from Openshift-Ci)"
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


if __name__ == "__main__":
    # dry_run(logger)
    aws_report()
