import vk_api

def vk_init():
    token = '   '
    vk_session = vk_api.VkApi(token=token)
    return vk_session.get_api()

vk = vk_init()
conversations = vk.messages.getConversations(offsets=0, count=20)
for item in conversations['items']:
    try:
        unread_count = item['conversation']['unread_count']
        print(unread_count)
        dialog_id = item['conversation']['peer']['local_id']
        conversation = vk.messages.getHistory(
            peer_id = dialog_id,
            count = unread_count,
            extended = True
        )

        profile = conversation['profiles'][0]
        user = f"{profile['first_name']} {profile['last_name']}"

        messages = conversation['items']
        messages.reverse()

        text = ''
        for message in messages:
            text += message['text'] + '\n'
        print(f'{unread_count} сообщение от пользователя {user}:\n{text}')
    except:
        pass

