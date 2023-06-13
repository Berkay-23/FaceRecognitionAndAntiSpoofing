from flask import Blueprint, request
from controllers import main_controller

page = Blueprint('main', __name__)


@page.route('/', methods=['GET'])
def index():
    return main_controller.main_get()


@page.route('/login', methods=['GET'])
def login():
    return main_controller.login_get()


@page.route('/register', methods=['GET'])
def register():
    username = request.args.get('username') if request.args.get('username') else None
    return main_controller.register(username)


@page.route('/upload', methods=['POST'])
def upload():
    if 'photo' in request.files:
        blob = request.files['photo']
        blob.save('static/images/temp.jpg')
        return 'Görüntü yüklendi.', 200
    else:
        return 'Hata: Fotoğraf bulunamadı.', 400
