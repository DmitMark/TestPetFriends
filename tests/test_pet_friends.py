from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password, invalid_key
import os

pf = PetFriends()
def test_get_api_key_for_valid_user(email = valid_email, password = valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result


def test_get_api_key_for_invalid_user(email = invalid_email, password = invalid_password):
    """ Проверяем что запрос api ключа возвращает статус 403 при использовании данных
    незарегистрированного пользователя(отсутствует в базе) и в ответе нет слова key"""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result


def test_get_api_key_for_valid_user_invalid_password(email=valid_email, password=invalid_password):
    """ Проверяем что запрос api ключа возвращает статус 403 при использовании неверного пароля
     пользователя(отсутствует в базе) и в ответе нет слова key"""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
        запрашиваем список всех питомцев и проверяем что список не пустой."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_get_all_pets_with_invalid_key(filter=''):
    """ Проверяем, что при использовании в запросе невалидного ключа в ответе
    получаем статус 403"""

    """Присваиваем ключу невалидное значение"""
    auth_key = invalid_key
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403


def test_get_my_pets_with_valid_key(filter='my_pets'):
    """ Проверяем что запрос мои питомцы('my_pets') возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
        запрашиваем список мои питомцы и проверяем что список не пустой."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Jack', animal_type='dog',
                                     age='4', pet_photo='images/dog1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age

def test_add_new_pet_with_invalid_data_photo(name='Jack', animal_type='dog',
                                     age='4', pet_photo='images/dog3.ico'):
    """Проверяем что нельзя добавить питомца с фото в неверном формате. Ожидаем
    в ответе статус код 400 - данные некоректны"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400


def test_add_new_pet_with_invalid_key(name='Jack', animal_type='dog',
                                     age='4', pet_photo='images/dog1.jpg'):
    """Проверяем что нельзя добавить питомца используя невалидный ключ. Ожидаем
       в ответе статус код 403"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    """Присваиваем ключу невалидное значение"""
    auth_key = invalid_key

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 403

def test_add_new_pet_with_invalid_data_age(name='Bobik', animal_type='двортерьер',
                                     age='four', pet_photo='images/dog1.jpg'):
    """Проверяем что нельзя добавить питомца указав возраст словом. Ожидаем
       в ответе статус код 400 - данные некоректны"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Jack", "doge", "3", "images/dog1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    assert status == 200
    assert pet_id not in my_pets.values()

def test_failed_delete_self_pet_with_invaled_key():
    """Проверяем возможность удаления питомца используя невалидный ключ
    В ответе ожидаем статус код 403"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Jack", "doge", "3", "images/dog1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']

    """Присваиваем ключу невалидное значение"""
    auth_key = invalid_key
    status, _ = pf.delete_pet(auth_key, pet_id)

    assert status == 403

def test_successful_update_self_pet_info(name='Tom', animal_type='cat', age='5'):
    """Проверяем возможность обновления информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name

    else:
        raise Exception("There is no my pets")

def test_successful_create_pet_simle(name='Tom', animal_type='cat', age='5'):
    """Проверяем что можно добавить питомца с корректными данными(без добавления фото)"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age

def test_successful_add_pet_photo(pet_photo='images/dog2.jpg'):
    """Проверяем что можно добавить фото питомца к существующему питомцу"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status = pf.add_photo_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 200

    else:
        raise Exception("There is no my pets")











