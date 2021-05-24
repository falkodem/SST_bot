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
import tkinter
import numpy as np
import subprocess

session = requests.Session()
vk_session = vk_api.VkApi(token='72ebbd071624448cf812128336bce2a79eb6d030d47683496f212a8055a239819c169bdfec82748dfddad')
longpoll = VkBotLongPoll(vk_session, 202973017)
vk = vk_session.get_api()

Lslongpoll = VkLongPoll(vk_session)
Lsvk = vk_session.get_api()

# keyboard = VkKeyboard(one_time=True)
# keyboard.add_button('Привет', color=VkKeyboardColor.NEGATIVE)
# keyboard.add_button('Клавиатура', color=VkKeyboardColor.POSITIVE)
# keyboard.add_line()
# keyboard.add_location_button()
# keyboard.add_line()
# keyboard.add_vkpay_button(hash="action=transfer-to-group&group_id=183415444")

LongPoll_conn_data = vk.messages.getLongPollServer(need_pts=0,
                                  group_id=202973017,
                                  lp_version=3)