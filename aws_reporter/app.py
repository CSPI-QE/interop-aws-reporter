import os
from typing import Any

from flask import Flask
from simple_logger.logger import get_logger
from flask.logging import default_handler
from log_aws_report import send_slack_message
from multiprocessing import Process


APP = Flask("aws-reporter")
APP.logger.removeHandler(default_handler)
APP.logger.addHandler(get_logger(APP.logger.name).handlers[0])


@APP.route("/aws-report", methods=["POST"])
def aws_report() -> Any:
    message = "AWS Reporting is cool"
    slack_webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    if not slack_webhook_url:
        return {"error": "slack_errors_webhook_url is required"}, 400

    if slack_webhook_url:
        send_slack_message(
            message=message,
            webhook_url=slack_webhook_url,
            logger=APP.logger,
        )
    return {"status": "message sent"}, 200


# def process_webhook_exception(logger, ex, route, slack_errors_webhook_url=None):
#     err_msg = f"{route}: Failed to process hook{f': {ex}' if ex else ''}"
#     logger.error(err_msg)
#
#     if not isinstance(ex, OpenshiftCiReTriggerError) or not isinstance(ex, AddonsWebhookTriggerError):
#         send_slack_message(message=err_msg, webhook_url=slack_errors_webhook_url, logger=logger)
#
#     return "Process failed"


def run_in_process(targets: dict) -> None:
    for target, _kwargs in targets.items():
        proc = Process(target=target, kwargs=_kwargs)
        proc.start()


if __name__ == "__main__":
    run_in_process(
        targets={
            # run_swatch_report: {"logger": APP.logger},
        }
    )
    APP.logger.info(f"Starting {APP.name} app")
    APP.run(
        port=int(os.environ.get("AWS_REPORTER_LISTEN_PORT", 5000)),
        host=os.environ.get("AWS_REPORTER_LISTEN_IP", "127.0.0.1"),
        use_reloader=True if os.environ.get("AWS_REPORTER_USE_RELOAD") else False,
    )
