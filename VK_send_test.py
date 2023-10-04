import vk_api

def vk_init():
    token = '   '
    vk_session = vk_api.VkApi(token=token)
    return vk_session.get_api()

vk = vk_init()
name = 'Анна Ушакова'
friends = vk.friends.search(user_id=446499034, q=name)
friend_id = friends['items'][0]['id']
vk.messages.send(user_id=friend_id, message='В автоматическом режиме))))', random_id = 0)
