FROM python:3.8-slim

WORKDIR /app

RUN pip install TTS

EXPOSE 8080

ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
