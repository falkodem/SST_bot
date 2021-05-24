import vk_api, vk
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api import VkUpload
import json
import requests
from pydub import AudioSegment
import io
import tkinter
import numpy as np
import subprocess


session = requests.Session()

vk_session = vk_api.VkApi(token='72ebbd071624448cf812128336bce2a79eb6d030d47683496f212a8055a239819c169bdfec82748dfddad')

longpoll = VkBotLongPoll(vk_session, 202973017)
vk = vk_session.get_api()

from vk_api.longpoll import VkLongPoll, VkEventType
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

# ------------------------------------------ Конфа ------------------------------------------
# for event in longpoll.listen():
#     if event.type == VkBotEventType.MESSAGE_NEW:
#         print(event)
#         if 'Ку' in str(event) or 'Привет' in str(event) or 'Хай' in str(event) or 'Хелло' in str(event) or 'Хеллоу' in str(event):
#             if event.from_chat:
#                 vk.messages.send(
#                     key=(LongPoll_conn_data['key']),
#                     server=(LongPoll_conn_data['server']),
#                     ts=(LongPoll_conn_data['ts']),
#                     random_id=get_random_id(),
#                     message='йоу',
#                     chat_id=event.chat_id
#                 )
#         if 'Клавиатура' in str(event):
#             if event.from_chat:
#                 vk.messages.send(
#                     keyboard = keyboard.get_keyboard(),
#                     key = ('a1cd7f2c07e1096d4948e0c7f449dcb9db2303b9'),
#                     server = ('https://lp.vk.com/wh202973017'),
#                     ts=('5'),
#                     random_id = get_random_id(),
#                     message='Держи',
#                     chat_id=event.chat_id
#                     )
#         if 'кота' in str(event):
#             if event.from_chat:
#                 attachments = []
#                 upload = VkUpload(vk_session)
#                 image_url = 'https://storage.theoryandpractice.ru/tnp/uploads/image_block/000/052/014/image/base_d9dd9b626f.jpg'
#                 image = session.get(image_url, stream=True)
#                 photo = upload.photo_messages(photos=image.raw)[0]
#                 attachments.append(
#                     'photo{}_{}'.format(photo['owner_id'], photo['id'])
#                 )
#                 vk.messages.send(
#                     key=('a1cd7f2c07e1096d4948e0c7f449dcb9db2303b9'),
#                     server=("https://lp.vk.com/wh202973017"),
#                     ts=('5'),
#                     random_id=get_random_id(),
#                     message='котик!',
#                     chat_id=event.chat_id,
#                     attachment=','.join(attachments),
#                 )

# ----------------------------- ЛС старое ----------------------------------------------------------
# for event in Lslongpoll.listen():
#     if event.type == VkEventType.MESSAGE_NEW and event.to_me:
#         audiofile_url = json.loads(event.attachments['attachments'])[0]['audio_message']['link_mp3']
#         audio_bytes = requests.get(audiofile_url).content
#         audio_int = np.array(AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3").get_array_of_samples())
#         plt.plot(audio_int)
#         plt.show()
#         print(audio_int.shape)
#         vars1 = ['Привет', 'Ку', 'Хай', 'Хеллоу']
#         if event.text in vars1:
#             if event.from_user:
#                 Lsvk.messages.send(
#                     user_id = event.user_id,
#                     message = 'Катя Жопка)',
#                     random_id = get_random_id()
#                     )
#         vars2 = ['Клавиатура', 'клавиатура']
#         if event.text in vars2:
#             if event.from_user:
#                 Lsvk.messages.send(
#                     user_id = event.user_id,
#                     random_id = get_random_id(),
#                     keyboard = keyboard.get_keyboard(),
#                     message = 'Держи'
#                     )
# -------------------------------------ЛСновое-------------------------------------------
for event in Lslongpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        audiofile_url = json.loads(event.attachments['attachments'])[0]['audio_message']['link_mp3']
        audio_bytes = requests.get(audiofile_url).content
        audio_mp3 = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3").set_frame_rate(16000)
        audio_samples = np.array(audio_mp3.get_array_of_samples()) # для графика например, тупо аудиомассив
        audio_mp3.export('./audio.wav', format="wav")
        if event.from_user:
            Lsvk.messages.send(
                user_id=event.user_id,
                message="Перевожу...",
                random_id=get_random_id()
            )
            command = "deepspeech --model output_graph.pb --alphabet alphabet.txt --lm lm.binary --trie trie --audio audio.wav"
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            Lsvk.messages.send(
                user_id = event.user_id,
                message = output,
                random_id = get_random_id()
                )
        vars2 = ['Клавиатура', 'клавиатура']
        if event.text in vars2:
            if event.from_user:
                Lsvk.messages.send(
                    user_id = event.user_id,
                    random_id = get_random_id(),
                    keyboard = keyboard.get_keyboard(),
                    message = 'Держи'
                    )