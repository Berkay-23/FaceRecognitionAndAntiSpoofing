import subprocess
from flask import render_template
import glob
import time
import config
from spoofing.test import test


def main_get():
    return render_template('main_views/main.html')


def login_get():
    username = get_username()
    if type(username) == list:
        return {'username': 'unknown_person', 'message': 'Birden fazla kişi algılandı. Lütfen tekrar deneyiniz.'}

    label = test(
        image='static/images/temp.jpg',
        model_dir=r'spoofing/resources/anti_spoof_models',
        device_id=0
    )

    if label != 1:
        return {'username': 'unknown_person', 'message': 'Yüz verisinde sahtecilik algılandı. Lütfen tekrar deneyiniz.'}

    if username in ['unknown_person', 'no_persons_found']:
        return {'username': 'unknown_person', 'message': 'Yüzünüz veri tabanında bulunamadı.'}

    update_log('logged in', username)
    return {'username': username.capitalize()}


def register(username):
    if username:
        if check_usernames(username):
            return {'username': 'unknown_person', 'message': 'Bu kullanıcı adı zaten kullanılıyor.'}
        else:
            if get_username() == 'unknown_person':
                try:
                    username = username.replace(' ', '_').lower()
                    with open(f'{config.DB_DIR}/{username}.jpg', 'wb') as f:
                        f.write(open('static/images/temp.jpg', 'rb').read())
                        f.close()

                except Exception as e:
                    return {'username': 'unknown_person', 'message': f'Hata: {e}'}
            else:
                return {'username': 'unknown_person', 'message': 'Yüzünüz veri tabanında zaten bulunuyor.'}
    else:
        return {'username': 'unknown_person', 'message': 'Lütfen kullanıcı adınızı giriniz.'}

    update_log('signed up', username)
    return {'username': username.capitalize()}


def check_usernames(username):
    db_dir = 'static/images/db'
    db_usernames = [path.split('\\')[-1].split('.')[0] for path in glob.glob(db_dir + '/*.jpg')]
    return username.replace(' ', '_').lower() in db_usernames


def get_username():
    output = str(subprocess.check_output(['face_recognition', config.DB_DIR, 'static/images/temp.jpg']))
    fixed_output = output.replace('\\r', '').replace('\\n', '').replace('b\'', '').replace('\'', '')
    fixed_output = fixed_output.replace('static/images/temp.jpg', '')

    names = list(filter(lambda x: x != '', fixed_output.split(',')))

    return names if len(names) > 1 else names[0]


def update_log(process, username):
    with open(config.LOG_PATH, 'a') as f:
        log = f'{username} - {process.upper()} - on [{time.strftime("%d/%m/%Y %H:%M:%S")}]\n'
        f.write(log)
        f.close()
