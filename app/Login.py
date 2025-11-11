import hashlib
import string
from datetime import datetime, timedelta
import unicodedata


def md5(s):
    '''
    MD5摘要
    :param str: 字符串
    :return: 经MD5以后的字符串
    '''
    h = hashlib.md5(s.encode(encoding='utf-8'))
    return h.hexdigest()


# import model.user after the defination of md5(s) to avoid circular import
from model.user import get_user_by_username, insert_user, update_password_by_username

path_prefix = '/var/www/wordfreq/wordfreq/'
path_prefix = './'  # comment this line in deployment


def verify_user(username, password):
    user = get_user_by_username(username)
    encoded_password = md5(username + password)
    return user is not None and user.password == encoded_password


def add_user(username, password):
    start_date = datetime.now().strftime('%Y%m%d')
    expiry_date = (datetime.now() + timedelta(days=30)).strftime('%Y%m%d')  # will expire after 30 days
    # 将用户名和密码一起加密，以免暴露不同用户的相同密码
    password = md5(username + password)
    insert_user(username=username, password=password, start_date=start_date, expiry_date=expiry_date)


def check_username_availability(username):
    existed_user = get_user_by_username(username)
    return existed_user is None


def change_password(username, old_password, new_password):
    '''
    修改密码
    :param username: 用户名
    :param old_password: 旧的密码
    :param new_password: 新密码
    :return: 修改成功:True 否则:False
    '''
    if not verify_user(username, old_password):  # 旧密码错误
        return {'error':'Old password is wrong.', 'username':username}
    # 将用户名和密码一起加密，以免暴露不同用户的相同密码
    if new_password == old_password:  #新旧密码一致
        return {'error':'New password cannot be the same as the old password.', 'username':username}
    update_password_by_username(username, new_password)
    return {'success':'Password changed', 'username':username}


def get_expiry_date(username):
    user = get_user_by_username(username)
    if user is None:
        return '20191024'
    else:
        return user.expiry_date


class UserName:
    def __init__(self, username):
        self.username = username

    def contains_chinese(self):
        for char in self.username:
            # Check if the character is in the CJK (Chinese, Japanese, Korean) Unicode block
            if unicodedata.name(char).startswith('CJK UNIFIED IDEOGRAPH'):
                return True
        return False

    def validate(self):
        if len(self.username) > 20:
            return f'{self.username} is too long.  The user name cannot exceed 20 characters.'
        if self.username.startswith('.'):  # a user name must not start with a dot
            return 'Period (.) is not allowed as the first letter in the user name.'
        if ' ' in self.username:  # a user name must not include a whitespace
            return 'Whitespace is not allowed in the user name.'
        for c in self.username:  # a user name must not include special characters, except non-leading periods or underscores
            if c in string.punctuation and c != '.' and c != '_':
                return f'{c} is not allowed in the user name.'
        if self.username in ['signup', 'login', 'logout', 'reset', 'mark', 'back', 'unfamiliar', 'familiar', 'del',
                             'admin']:
            return 'You used a restricted word as your user name.  Please come up with a better one.'
        if self.contains_chinese():
            return 'Chinese characters are not allowed in the user name.'
        return 'OK'


class Password:
    def __init__(self, password):
        self.password = password

    def contains_chinese(self):
        for char in self.password:
            # Check if the character is in the CJK (Chinese, Japanese, Korean) Unicode block
            if unicodedata.name(char).startswith('CJK UNIFIED IDEOGRAPH'):
                return True
        return False

    def validate(self):
        if len(self.password) < 4:
            return 'Password must be at least 4 characters long.'
        if ' ' in self.password:
            return 'Password cannot contain spaces.'
        if self.contains_chinese():
            return 'Chinese characters are not allowed in the password.'
        return 'OK'


class WarningMessage:
    def __init__(self, s, type='username'):
        self.s = s
        self.type = type

    def __str__(self):
        if self.type == 'username':
            return UserName(self.s).validate()
        if self.type == 'password':
            return Password(self.s).validate()
