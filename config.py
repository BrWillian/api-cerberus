DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///storage.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = True
DEFAULT_PARSERS = [
    'flask_api.parsers.JSONParser'
]
CLIENT_IMAGES = 'tf_model/predict/'