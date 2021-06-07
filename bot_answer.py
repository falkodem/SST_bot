from pydub import AudioSegment
import io
import bs4
import subprocess
import requests
import librosa
import soundfile as sf

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
        date_time_list = self._clean_all_tag_from_str(str(b.select(".page")[0].findAll("h2")[0])).replace("В", " В") \
            .replace(", ", " ").split()
        date = " ".join(date_time_list[0:4])
        day_of_week = date_time_list[4]
        time = " ".join(date_time_list[5:])
        return date+"\n"+day_of_week+"\n"+time

    # Получение погоды
    def _get_weather(self, city: str = "москва") -> list:
        request = requests.get("https://sinoptik.com.ru/погода-" + city)
        b = bs4.BeautifulSoup(request.text, "html.parser")
        p3 = b.select('temperature')
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
            return f"Бывай, {self._USERNAME}!"

        else:
            return "Не понимаю о чем вы..."

    def audio_message(self, message_url):

        audio_bytes = requests.get(message_url).content
        with open('audio.mp3', 'wb') as f:
            f.write(audio_bytes)
        y, sr = librosa.load('audio.mp3')
        y_16k = librosa.resample(y, sr, 16000)
        filename = './audio.wav'
        sf.write(filename, y_16k, 16000)
        # audio_mp3 = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3").set_frame_rate(16000)
        # # audio_samples = np.array(audio_mp3.get_array_of_samples())  # для графика например, тупо аудиомассив
        # filename = './audio.wav'
        # audio_mp3.export(filename, format="wav")

        return self.transcribe(filename)

    def transcribe(self, filename):
        command = "deepspeech --model output_graph.pb --alphabet alphabet.txt --lm lm.binary --trie trie --audio " + filename
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        output = output.decode('utf-8')
        if output == "\n":
            return "Я не услышал тут речи"
        else:
            return output
        # if isinstance(output, str):
        #     return output
        # else:
        #     return "Не понимаю. \nПохоже на эльфийский"


vk_bot = VKBot
