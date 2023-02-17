import requests, yadisk
from tqdm import tqdm
import json

#Подключаем яДиск
y = yadisk.YaDisk(token="")

#Сюда токен Вк
access_token = ''

#Ссылка на метод вк
url = 'https://api.vk.com/method/photos.getAll'
user_id = input('Введите ID пользователя Вк для сохранения фото: ')
summ_photo = input('Введите колличество фото для сохранения: ')

#Параметры метода
params = {
    'owner_id': user_id,
    'extended': 1,
    'access_token': access_token,
    'count': summ_photo,
    'v': 5.131
}
#Работаем с ссылкой
res = requests.get(url, params=params).json()
res = res['response']['items']

#Переменные для работы с размерами фото
sizes_photos = {}
last_photos = {}
all_size = []
json_files = []

#Разбираем ссылку на состовляющие
for i in res:
    likes = i['likes']
    sizes = i['sizes']

    for i2 in sizes:
        urls = i2['url']
        size = urls.rpartition('size=')[-1].rpartition('&quality=')[0].split('x')
        summ = int(size[0]) + int(size[1])
        sizes_photos[summ] = [i2['url']]
        all_size.append(i)

    peremennaya_sort = sorted(sizes_photos.keys())[-1]
    url_for_download = sizes_photos[peremennaya_sort]

    #Чистим all_size
    while len(all_size) > 1:
        for i in all_size:
            if len(all_size) > 1:
                all_size.pop(0)

    #Закидываем данные для json файла в переменную
    for i in all_size:
        for i in i['sizes']:
            if url_for_download[0] == i['url']:
                j_file = {
                    "file_name": likes['count'],
                    "size": i['type']
                }
                json_files.append(j_file)

    last_photos[url_for_download[0]] = str(likes['count'])
    sizes_photos.clear()

folder_path = input('Введите название папки для загрузки фото: ')

#Проверка наличия папки в яДиске и если нет то ее создание
if not y.is_dir(folder_path):
    y.mkdir(folder_path)

#Запись фото на яДиск с прогресс баром
for key, value in tqdm(last_photos.items()):
    y.upload_url(key, f'{folder_path}/{value}.jpeg')

with open("data_file.json", "w") as write_file:
    json.dump(json_files, write_file)