from extensions import db
import datetime

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True) #設定他為主鍵

    line_id = db.Column(db.String(50), unique= True) #unique = True 代表是不可以重複的
    display_name = db.Column(db.String(255)) #用戶的line名稱
    picture_url = db.Column(db.String(255)) #用戶大頭貼的url

    created_on = db.Column(db.DateTime, default= datetime.datetime.now())

    def __init__(self, line_id,display_name,picture_url):
        self.line_id = line_id
        self.display_name = display_name
        self.picture_url = picture_url