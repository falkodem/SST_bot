import vk_api, vk
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.longpoll import VkLongPoll, VkEventType
import json
import requests

from bot_answer import vk_bot

session = requests.Session()
vk_session = vk_api.VkApi(token='72ebbd071624448cf812128336bce2a79eb6d030d47683496f212a8055a239819c169bdfec82748dfddad')
longpoll = VkBotLongPoll(vk_session, 202973017)
vk = vk_session.get_api()

Lslongpoll = VkLongPoll(vk_session)
Lsvk = vk_session.get_api()

LongPoll_conn_data = vk.messages.getLongPollServer(need_pts=0,
                                                   group_id=202973017,
                                                   lp_version=3)


###############################################################################################################


def get_image():
    upload = vk_api.VkUpload(vk)
    photo = upload.photo_messages('./image.jpg')
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    return attachment


def write_msg(user_id, message, attach=None):
    if attach is None:
        Lsvk.messages.send(
            user_id=user_id,
            message=message,
            random_id=get_random_id()
        )
    else:
        Lsvk.messages.send(
            user_id=user_id,
            message=message,
            random_id=get_random_id(),
            attachment=attach
        )


def run_bot():
    print("Server started")

    for event in Lslongpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            bot = vk_bot(event.user_id)
            if event.text != "":
                write_msg(event.user_id, bot.text_message(event.text))
            else:
                try:
                    event.attachments['attach1_kind']
                except KeyError:
                    write_msg(event.user_id, "Я не работаю с такими запросами. Пока что", get_image())

                else:
                    write_msg(event.user_id, "Перевожу..")
                    audiofile_url = json.loads(event.attachments['attachments'])[0]['audio_message']['link_mp3']
                    # if event.from_user:
                    write_msg(event.user_id, bot.audio_message(audiofile_url))


if __name__ == '__main__':
    run_bot()
