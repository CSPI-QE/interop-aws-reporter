from simple_logger.logger import get_logger
from log_aws_report import execute_dry_run, send_log_file_with_bot

logger = get_logger(name=__name__)


if __name__ == "__main__":
    execute_dry_run(logger=logger)
    send_log_file_with_bot(logger=logger)
