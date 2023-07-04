import pytest

from api import PetFriends
from settings import valid_email, valid_password
import os

from settings import invalid_auth_key

pf = PetFriends()


def test_get_api_key_for_valid_user(email:str = valid_email, password: str = valid_password) -> None:
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
        запрашиваем список всех питомцев и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/tager.jpg.'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

# тесты домашнего задания
#№1
def test_add_new_pet_without_photo(name='Сарделька', animal_type='корги', age='5'):
    """Проверяем что можно добавить питомца"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

# №2
def test_add_photo_to_pet(pet_photo="images/Corgi.jpg"):
    '''Проверка метода добавления фото к существующему питомцу с валидными данными'''

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то добавляем фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_to_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # сверяем полученный ответ с результатом
        assert status == 200
        assert result['pet_photo'] is not None
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

# №3
def test_get_api_key_for_invalid_user(email:str = 'not_real_email@mail.com', password: str= "not_real_password")-> None:
     '''Проверка получения api-ключа с данными незарегистрированного пользователя'''

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
     status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
     assert status == 403
     assert 'key' not in result

# №4
def test_get_all_pets_with_invalid_key(filter=''):
    '''Проверка получения списка питомцев с несуществующим api-ключом
    (замена api-ключа на несуществующий у существующего пользователя)'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # замена ключа на несуществующий
    auth_key = invalid_auth_key

    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403

# №5
def test_add_new_pet_with_invalid_key(name='Лошарик', animal_type='Бобтейл',
                                     age='2', pet_photo='images/tager.jpg.'):
    """Проверяем что можно добавить питомца с несуществующим api-ключом
    (замена api-ключа на несуществующий у существующего пользователя)"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # замена ключа на несуществующий
    auth_key = invalid_auth_key

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403

# №6
def test_post_new_pet_with_invalid_photo(name="шарик", animal_type="пес",
                                         age='8', pet_photo="images/Pes.txt"):
    '''Проверка на добавление питомца с текстовым файлом вместо фото.
    БАГ. Должен выдавать ошибку 400, потому что фото нужно в формате JPG, JPEG, PNG.'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400
    assert result['name'] == name

# №7
def test_add_new_pet_without_photo(name="Бука", animal_type="улитка", age="старая"):
    '''Проверка добавление питомца (без фото) с неверно написанным возрастом.
    БАГ. Должен выдавать ошибку 400, потому что возраст должен быть введен числом.'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 400
    assert result['age'] == age

# №8
def test_add_new_pet_without_photo_invalid_data(name="", animal_type="", age=""):
    '''Проверка на добавление питомца(без фото) с пустыми полями.
    БАГ. Должен быть негативный результат, потому что заполнение данных полей обязательно.'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 400
    assert result['name'] == name

# №9
def test_successful_delete_self_pet():
    """Проверка на возможность удаления питомца с несуществующим api-ключом
    (замена api-ключа на несуществующий у существующего пользователя)"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # замена ключа на несуществующий
    auth_key = invalid_auth_key

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 403

# №10
def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверка возможности обновления информации о питомце с несуществующим api-ключом
    (замена api-ключа на несуществующий у существующего пользователя)"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # замена ключа на несуществующий
    auth_key = invalid_auth_key

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 403