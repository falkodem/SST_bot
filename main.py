import vk_api, vk
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload
import json
import requests
from pydub import AudioSegment
import io
import bs4
import tkinter
import numpy as np
import subprocess


session = requests.Session()
vk_session = vk_api.VkApi(token='72ebbd071624448cf812128336bce2a79eb6d030d47683496f212a8055a239819c169bdfec82748dfddad')
longpoll = VkBotLongPoll(vk_session, 202973017)
vk = vk_session.get_api()

Lslongpoll = VkLongPoll(vk_session)
Lsvk = vk_session.get_api()

keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Привет', color=VkKeyboardColor.NEGATIVE)
keyboard.add_button('Клавиатура', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_location_button()
keyboard.add_line()
keyboard.add_vkpay_button(hash="action=transfer-to-group&group_id=183415444")

LongPoll_conn_data = vk.messages.getLongPollServer(need_pts=0,
                                  group_id=202973017,
                                  lp_version=3)

###############################################################################################################


def write_msg(user_id, message):
    Lsvk.messages.send(
        user_id=user_id,
        message=message,
        random_id=get_random_id()
    )



class VKBot:
    def __init__(self, user_id):
        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)

        self._COMMANDS = ["ПРИВЕТ", "ПОГОДА", "ВРЕМЯ", "ПОКА"]

    def _get_user_name_from_vk_id(self, user_id):
        request = requests.get("https://vk.com/id" + str(user_id))
        bs = bs4.BeautifulSoup(request.text, "html.parser")

        user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])

        return user_name.split()[0]

    # Получение времени:
    def _get_time(self):
        request = requests.get("https://my-calend.ru/date-and-time-today")
        b = bs4.BeautifulSoup(request.text, "html.parser")
        return self._clean_all_tag_from_str(str(b.select(".page")[0].findAll("h2")[1])).split()[1]

    # Получение погоды
    def _get_weather(city: str = "москва") -> list:
        request = requests.get("https://sinoptik.com.ru/погода-" + city)
        b = bs4.BeautifulSoup(request.text, "html.parser")

        p3 = b.select('.temperature .p3')
        weather1 = p3[0].getText()
        p4 = b.select('.temperature .p4')
        weather2 = p4[0].getText()
        p5 = b.select('.temperature .p5')
        weather3 = p5[0].getText()
        p6 = b.select('.temperature .p6')
        weather4 = p6[0].getText()
        result = ''
        result = result + ('Утром :' + weather1 + ' ' + weather2) + '\n'
        result = result + ('Днём :' + weather3 + ' ' + weather4) + '\n'
        temp = b.select('.rSide .description')
        weather = temp[0].getText()
        result = result + weather.strip()

        return result

    # Метод для очистки от ненужных тэгов

    @staticmethod
    def _clean_all_tag_from_str(string_line):
        """
        Очистка строки stringLine от тэгов и их содержимых
        :param string_line: Очищаемая строка
        :return: очищенная строка
        """
        result = ""
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += i
            else:
                if i == ">":
                    not_skip = True

        return result

    def text_message(self, message):

        # Привет
        if message.upper() == self._COMMANDS[0]:
            return f"Привет-привет, {self._USERNAME}!"

        # Погода
        elif message.upper() == self._COMMANDS[1]:
            return self._get_weather()

        # Время
        elif message.upper() == self._COMMANDS[2]:
            return self._get_time()

        # Пока
        elif message.upper() == self._COMMANDS[3]:
            return f"Бывай!, {self._USERNAME}!"

        else:
            return "Не понимаю о чем вы..."

    def audio_message(self, message_url):

        audio_bytes = requests.get(message_url).content
        audio_mp3 = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3").set_frame_rate(16000)
        audio_samples = np.array(audio_mp3.get_array_of_samples())  # для графика например, тупо аудиомассив
        filename = './audio.wav'
        audio_mp3.export(filename, format="wav")

        return self.transcribe(filename)

    def transcribe(self, filename):
        command = "deepspeech --model output_graph.pb --alphabet alphabet.txt --lm lm.binary --trie trie --audio " + filename
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        if isinstance(output, str):
            return output
        else:
            return "Не понимаю. \nПохоже на эльфийский"


print("Server started")

for event in Lslongpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        bot = VKBot(event.user_id)
        print(event.attachments)

        if event.text != "":
            write_msg(event.user_id, bot.text_message(event.text))
        else:
            try:
                event.attachments['attach1_kind']
            except KeyError:
                Lsvk.messages.send(
                    user_id=event.user_id,
                    message="рро",
                    attachment='photo77910182_457245306',
                    random_id=get_random_id()
                )
            else:
                write_msg(event.user_id, "Перевожу..")
                audiofile_url = json.loads(event.attachments['attachments'])[0]['audio_message']['link_mp3']
                 # if event.from_user:
                write_msg(event.user_id, bot.audio_message(audiofile_url))
