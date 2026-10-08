FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
COPY sample_data ./sample_data

RUN pip install --no-cache-dir .

CMD ["python", "-m", "automation_demo.simulation", "--count", "100"]

