from flask import *
from flask_httpauth import HTTPTokenAuth
from Article import load_freq_history

path_prefix = '/var/www/wordfreq/wordfreq/'
path_prefix = './'  # comment this line in deployment

apiService = Blueprint('site',__name__)

auth = HTTPTokenAuth(scheme='Bearer')

tokens = {
    "token": "token",
    "secret-token": "lanhui"  # token, username
}


@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]


@apiService.route('/api/mywords')  # HTTPie usage: http -A bearer -a secret-token  http://127.0.0.1:5000/api/mywords
@auth.login_required
def show():
    username = auth.current_user()
    word_freq_record = path_prefix + 'static/frequency/' + 'frequency_%s.pickle' % (username)
    d = load_freq_history(word_freq_record)
    return jsonify(d)

