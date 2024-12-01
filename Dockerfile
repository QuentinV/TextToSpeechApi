FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libsndfile1 \
    git \
    ffmpeg \
    && apt-get clean

RUN pip install flask
RUN pip install coqui-tts
RUN pip install pydub
RUN pip install numpy
RUN pip install soundfile

EXPOSE 5000

ENV NAME CoquiTTSAPI

CMD ["python", "app.py"]
