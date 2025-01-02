FROM python:3.12

COPY pyproject.toml poetry.lock README.md /interop_aws_reporter/
COPY interop_aws_reporter /interop_aws_reporter/interop_aws_reporter/

WORKDIR /interop_aws_reporter
ENV POETRY_HOME=/interop_aws_reporter
ENV PATH="/interop_aws_reporter/bin:$PATH"

RUN python3 -m pip install pip --upgrade \
  && python3 -m pip install poetry \
  && poetry config cache-dir $POETRY_HOME \
  && poetry config virtualenvs.in-project true \
  && poetry config installer.max-workers 10 \
  && poetry install

RUN mkdir -p /tmp/ && chmod 777 /tmp/
RUN touch /interop_aws_reporter/cleanup.log && chmod 777 /interop_aws_reporter/cleanup.log
RUN touch /interop_aws_reporter/vcd_sdk.log && chmod 777 /interop_aws_reporter/vcd_sdk.log
RUN touch /interop_aws_reporter/cleanup_resource_AWS.html && chmod 777 /interop_aws_reporter/cleanup_resource_AWS.html

CMD ["poetry", "run", "python3", "interop_aws_reporter/app.py"]
