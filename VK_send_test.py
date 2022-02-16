import vk_api

def vk_init():
    token = 'ffa069d11ea54caadd873c7af5ded0accd5868b60dc47cf0f46b5d2d7452f8ff5969220c045dfd27ecd5a'
    vk_session = vk_api.VkApi(token=token)
    return vk_session.get_api()

vk = vk_init()
name = 'Анна Ушакова'
friends = vk.friends.search(user_id=446499034, q=name)
friend_id = friends['items'][0]['id']
vk.messages.send(user_id=friend_id, message='В автоматическом режиме))))', random_id = 0)
