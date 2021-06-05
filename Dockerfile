FROM python:3.7.10-buster as bot_builder
RUN apt update && apt -y install gettext-base
COPY requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["sh", "/run.sh"]