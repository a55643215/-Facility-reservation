#pip install flask_sqlalchemy
#pip install psycopg2-binary 連線的套件
#pip install Flask-Migrate 管理資料庫的套件

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



db = SQLAlchemy()
migrate = Migrate() 

