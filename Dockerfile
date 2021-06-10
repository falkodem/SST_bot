FROM python:3.7.10-buster as bot_builder
RUN apt update && apt -y install gettext-base && apt -y install libsndfile1 && apt -y install ffmpeg
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["bash", "/run.sh"]