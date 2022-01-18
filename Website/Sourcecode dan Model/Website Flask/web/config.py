
import os 

class Config(object):
    SECRET_KY = os.environ.get('SECRET_KEY') or "secret_string"

    MONGODBB_SETTINGS = {'db' : 'UTA_Enrollment'}