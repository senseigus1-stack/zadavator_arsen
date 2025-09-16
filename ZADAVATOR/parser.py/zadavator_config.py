# файл моей шизы, которую я пока не сделал не смотри сюда, мне стыдно



import requests



# URL страницы входа или целевой страницы
login_url = 'https://zadavator.spbal.ru/login/index.php'  # замените на правильный URL входа, если другой

# Ваши логин и пароль
payload = {
    'username': 's3nsei_GUS',
    'password': '6ViuQ2WjMEWw94h'
}


# Создаем сессию
session = requests.Session()
# Отправляем POST-запрос для входа
response = session.post(login_url, data=payload)
# После входа можно перейти на нужную страницу
target_url = 'https://zadavator.spbal.ru/course/view.php?id=121'
response = session.get(target_url)

print(response.text)

