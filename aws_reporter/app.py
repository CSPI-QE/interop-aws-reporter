import os
from typing import Any
from simple_logger.logger import get_logger
from utils import send_slack_message

logger = get_logger(name=__name__)


def aws_report() -> Any:
    message = "Hello :wave:, here is the weekly run report for [...] .\nAWS Reporting is cool! (sent from a container)"
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
    aws_report()
