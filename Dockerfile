FROM python:3.7.10-buster as bot_builder
RUN apt update && apt -y install gettext-base && apt -y install libsndfile1 && apt -y install ffmpeg
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN wget https://github.com/GeorgeFedoseev/DeepSpeech/releases/download/1.0/DeepSpeech-ru-v1.0-tensorflow_pb_models.tar.gz \
    && wget https://github.com/GeorgeFedoseev/DeepSpeech/releases/download/1.0/DeepSpeech-ru-v1.0-language_model.tar.gz \
    && tar -xvf DeepSpeech-ru-v1.0-tensorflow_pb_models.tar.gz \
    && tar -xvf DeepSpeech-ru-v1.0-language_model.tar.gz
#     && cd ./DeepSpeech-ru-v1.0-language_model \
#     && mv alphabet.txt lm.binary trie ../ \
#     && cd ../DeepSpeech-ru-v1.0-tensorflow_pb_models \
#     && mv output_graph.pb ../ \
#     && cd ..
CMD ["bash", "/run.sh"]