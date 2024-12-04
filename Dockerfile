FROM python:3.12

COPY pyproject.toml poetry.lock README.md /interop_aws_reporter/
COPY interop_aws_reporter /interop_aws_reporter/interop_aws_reporter/

WORKDIR /interop_aws_reporter

ENV POETRY_HOME=/interop_aws_reporter
ENV PATH="/interop_aws_reporter/bin:$PATH"

RUN python3 -m pip install pip --upgrade \
  && python3 -m pip install poetry \
  && poetry config cache-dir /interop_aws_reporter \
  && poetry config virtualenvs.in-project true \
  && poetry config installer.max-workers 10 \
  && poetry config --list \
  && poetry install

# ENTRYPOINT ["aws-reporter"]
CMD ["poetry", "run", "python", "interop_aws_reporter/app.py"]
