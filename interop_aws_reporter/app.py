from simple_logger.logger import get_logger
from log_aws_report import dry_run

logger = get_logger(name=__name__)


if __name__ == "__main__":
    dry_run(logger=logger)
    # aws_report()
