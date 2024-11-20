FROM python:3.11

WORKDIR /interop_aws_reporter
COPY . /interop_aws_reporter/

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"
# Install dependencies via Poetry (this step will create the virtual environment inside the container)
RUN poetry install --no-root --no-interaction
COPY pyproject.toml poetry.lock* /interop_aws_reporter/


# ENTRYPOINT ["aws-reporter"]
CMD ["poetry", "run", "python", "aws_reporter/app.py"]
