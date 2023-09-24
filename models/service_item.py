from extensions import db
import datetime

class Service_Item(db.Model):
    __tablename__ = 'service_item'

    id = db.Column(db.Integer, primary_key = True) #設定他為主鍵

    # line_id = db.Column(db.String(50), unique= True) #unique = True 代表是不可以重複的
    category = db.Column(db.String(255)) #服務的種類(SPA，美髮美睫之類的)
    img_url = db.Column(db.String(255)) #服務的圖片
    title = db.Column(db.String(255)) #服務的項目(精油推拿)
    duration = db.Column(db.String(255)) #時長
    description = db.Column(db.String(255)) #介紹
    price = db.Column(db.String(255)) #價格 

    created_on = db.Column(db.DateTime, default= datetime.datetime.now())

    def __init__(self, category,img_url,title,duration,description,price):
        self.category = category
        self.img_url = img_url
        self.title = title
        self.duration = duration
        self.description = description
        self.price = price