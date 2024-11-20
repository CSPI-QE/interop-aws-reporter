import subprocess
import tempfile
from typing import Any

AWS_CLIENT_REGION = "us-east-1"


def dry_run(logger: Any) -> None:
    # aws_access_id = os.environ.get("AWS_ACCESS_KEY","")
    # aws_secret_key = os.environ.get("AWS_SECRET_KEY","")
    # aws_client_region = os.environ.get("AWS_CLIENT_REGION",AWS_CLIENT_REGION)
    #
    # if not all(aws_access_id, aws_secret_key):
    #     raise "AWS creds are missing!"

    cloudwash_output = subprocess.run(["poetry", "run", "swach", "--help"], capture_output=True, text=True)

    logger.info(cloudwash_output.stdout)

    if cloudwash_output.returncode != 0:
        raise Exception(f"CloudWash execution failed: {cloudwash_output.stderr}")
    else:
        # Create a temporary file to store the logs
        with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
            tmpfile.write(cloudwash_output.stdout.encode())
            tmpfile_path = tmpfile.name

            logger.info(f"Output saved to: {tmpfile_path}")
