import requests
import os
import yadisk
token_my ='AgAAAAA-8XOVAADLW5hOojoh30fmqPEGbnCrZRI'
#  документация https://yandex.ru/dev/translate/doc/dg/reference/translate-docpage/

API_KEY = 'trnsl.1.1.20190712T081241Z.0309348472c8719d.0efdbc7ba1c507292080e3fbffe4427f7ce9a9f0'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
URL_upload = 'https://cloud-api.yandex.net/v1/disk/resources/upload'


def dir_input(prompt):
    f = False
    dir_name = ''
    while not f:
        dir_name = input(prompt)
        if len(dir_name) == 0:
            dir_name = os.path.dirname(os.path.abspath(__file__))
        f = os.path.exists(dir_name)
        if not f:
            print('Вы ввели не существующий путь, попробуйте еще раз')
    return dir_name


def lang_input(prompt):
    f = False
    lang = 'ru'
    while not f:
        try:
            lang_n = int(input(prompt))
            if int(lang_n) in [0, 1, 2, 3]:
                f = True
                if lang_n == 1:
                    lang = 'de'
                elif lang_n == 2:
                    lang = 'es'
                elif lang_n == 3:
                    lang = 'fr'
                elif lang_n == 0:
                    lang = 'ru'

        except ValueError:
            f = False
        if not f:
            print('Пожалуйста, повторите попытку')
    return lang


def load_text(dir_name, file_name):
    file = os.path.join(dir_name, file_name)
    if os.path.exists(file):
        with open(file, encoding='utf-8') as f:
            text = f.read()
    else:
        text = 'Файл ', file, 'не найден'
        print(text)
    return text

def save_text(text, dir_name, file_name):
    file = os.path.join(dir_name, file_name)
    print(file_name)
    with open(file, "w", encoding='utf-8') as f:
        f.write(text)
    print('Результат перевода сохранен в файле:', file)
    uploading_disk = int(input("Вы хотите загрузить данные Яндекс.Диск: 0 - Да, 1 - Нет  "))
    if uploading_disk == 0:
      #resp = requests.get(URL_upload, params=params)
      #print(resp.text)
      y = yadisk.YaDisk(token=token_my)
      #print(y.check_token())
      #print(y.get_disk_info())
      #print(list(y.listdir("/")))
      params ={
              'overwrite': True,
      }
      with open(file_name, "rb") as ff:
        y.upload(ff, "/"+file_name, overwrite=True)
        print(f"Файл {file_name} записан на Яндекс диск ")
# Как исключить ошибку при перезаписи

def translate_it(text, to_lang, out_lang):
    """
    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]
    :param to_lang:
    :return:
    """
    #print(text)

    #print(to_lang)
    #print(out_lang)
    params = {
        'key': API_KEY,
        'text': text,
        'lang': format(out_lang).format(to_lang),
    }

    response = requests.get(URL, params=params)
    json_ = response.json()
    return ''.join(json_['text'])


# print(translate_it('В настоящее время доступна единственная опция — признак включения в ответ автоматически определенного языка переводимого текста. Этому соответствует значение 1 этого параметра.', 'no'))

if __name__ == '__main__':
  inputdir = dir_input('Введите путь к файлу с текстом (по умолчанию Enter, если файл в рабочей директории):')
  outputdir = dir_input('Введите путь к файлу с результатом (по умолчанию Enter, если файл в рабочей директории):')
  inlang = lang_input('Выберите язык с которого необходимо перевести. 1 - DE, 2 - ES, 3 - FR  : ')
  outlang = 0
  outlang = lang_input('Выберите язык на который необходимо перевести. 0 - RU, 1 - DE, 2 - ES, 3 - FR  : ')
  a = translate_it(load_text(inputdir, inlang + '.txt'), inlang, outlang)
  save_text(a, outputdir, inlang + '-' + outlang + '.txt') 
  pass