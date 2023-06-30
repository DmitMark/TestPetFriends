import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder

class PetFriends:
    """API библиотека к веб приложению Pet Friends"""
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email, password):
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
           JSON с уникальным ключем пользователя, найденного по указанным email(str) и паролем(str)
           Статусы запроса:
           200 - A secret key which can be used in Header "auth_key" for other API methods
           403 - The error code means that provided combination of user email and password is incorrect"""

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key, filter):
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
            со списком наденных питомцев, совпадающих по filter(str). На данный момент фильтр может иметь
            либо пустое значение - получить список всех питомцев, либо 'my_pets' - получить список собственных питомцев
            Статусы запроса:
            200 - The list of available pets from database in JSON format.
            403 - The error code means that provided auth_key is incorrect"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key, name, animal_type, age, pet_photo):
        """Метод создает (постит) на сервер данные о добавляемом питомце и возвращает статус
            запроса на сервер и результат в формате JSON с данными добавленного питомца.
            Принимает данные auth_key, name, animal_type - в формате str, age - number, pet_photo - JPG, JPEG or PNG
            Статусы запроса:
            200 - The status code 200 means that pet was successfully added to the database
            400 - The error code means that provided data is incorrect
            403 - The error code means that provided auth_key is incorrect"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            }
        )
        headers = {'auth_key': auth_key['key'], 'Content-type': data.content_type}

        res = requests.post(self.base_url+'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pet(self, auth_key, pet_id):
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
            статус запроса и результат в формате JSON с текстом уведомления о успешном удалении.
            На сегодняшний день тут есть баг - в result приходит пустая строка, но status при этом = 200
            Принимает данные в форматах: auth_key, pet_id - str
            Статусы запроса:
            200 - status code means that the pet was removed from database successfully
            403 - The error code means that provided auth_key is incorrect"""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key, pet_id, name, animal_type, age):
        """Метод отправляет запрос на сервер о обновлении данных питомуа по указанному ID и
            возвращает статус запроса и result в формате JSON с обновлённыи данными питомца
            Принимает данные: auth_key, name, animal_type - в формате str, age - number
            Статусы запроса:
            200 - The status code 200 means that the information about pet was successfully updated in the database.
            400 - The error code means that provided data is incorrect
            403 - The error code means that provided auth_key is incorrect"""

        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }
        headers = {'auth_key': auth_key['key']}

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def create_pet_simple(self, auth_key, name, animal_type, age):
        """Метод создает (постит) на сервер данные о добавляемом питомце без добавления фото и возвращает статус
            запроса на сервер и результат в формате JSON с данными добавленного питомца.
            Принимает данные: auth_key, name, animal_type - в формате str, age - number
            Статусы запроса:
            200 - The status code 200 means that pet was successfully added to the database.
            400 - The error code means that provided data is incorrect
            403 - The error code means that provided auth_key is incorrect"""

        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }
        headers = {'auth_key': auth_key['key']}

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_photo_pet(self, auth_key, pet_id, pet_photo):
        """Метод постит на сервер фото для питомца и возвращает статус
            запроса на сервер и результат в формате JSON с данными питомца к которому было добавлено фото.
            Принимает данные auth_key, pet_id - в формате str, pet_photo - JPG, JPEG or PNG
            Статусы запроса:
            200 - The status code 200 means that pet was successfully added to the database.
            400 - The error code means that provided data is incorrect
            403 - The error code means that provided auth_key is incorrect"""

        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            }
        )
        headers = {'auth_key': auth_key['key'], 'Content-type': data.content_type}

        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        return status


