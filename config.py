import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LINE_PAY_ID = '2000604811'
    LINE_PAY_SECRET = '85c2256b73ef51f3adfcd8bc189172f5'

    STORE_IMAGE_URL = 'https://i.imgur.com/0KinQXT.jpg'

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://reservation:kk4VynPz2FbwuaqYNrQc24db8r2TTOia@dpg-ck7v30vsasqs73cfise0-a.singapore-postgres.render.com/reservation_we30"
    #"postgresql://reservation:kk4VynPz2FbwuaqYNrQc24db8r2TTOia@dpg-ck7v30vsasqs73cfise0-a.singapore-postgres.render.com/reservation_we30"
class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')