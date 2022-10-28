# Builder
FROM python:3.9-slim as builder

ARG PYTHONDONTWRITEBYTECODE=1
ARG PYTHONUNBUFFERED=1

RUN python -m venv /venv \
  && /venv/bin/python -m pip install --upgrade pip
ENV PATH="/venv/bin:$PATH"

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt \
  && python setup.py install


# Final
FROM python:3.9-slim

LABEL org.opencontainers.image.source=https://github.com/m3h7/smartmeter2mqtt
LABEL org.opencontainers.image.description="Reads from smartmeter and sends obis messages to MQTT."
LABEL org.opencontainers.image.licenses=MIT

COPY --from=builder /venv /venv

ENV PATH="/venv/bin:$PATH"

CMD ["smartmeter2mqtt", "-c", "/config/config.yml"]
