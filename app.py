from flask import Flask, request, abort
from urllib.parse import parse_qsl
from database import db_session, init_db
from sqlalchemy.sql.expression import text
from config import Config

from line_bot_api import *
from linebot.models import *
from models.user import Users
from models.product import Products
from models.cart import Cart
from models.order import Orders
from models.item import Items
from models.linepay import LinePay

import uuid


 
app = Flask(__name__)

#建立或取得user
def get_or_create_user(user_id):
    #從id=user_id先搜尋有沒有這個user，如果有的話就會直接跳到return
    user = db_session.query(Users).filter_by(id=user_id).first()
    #沒有的話就會透過line_bot_api來取得用戶資訊
    if not user:
        profile = line_bot_api.get_profile(user_id)
        #然後再建立user並且存入到資料庫當中
        user = Users(id=user_id, nick_name=profile.display_name, image_url=profile.picture_url)
        db_session.add(user)
        db_session.commit()

    return user

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
    

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_or_create_user(event.source.user_id)
    message_text = str(event.message.text).lower()
    if message_text == '@預約服務':
         message = Products.list_all()

    if message:
        line_bot_api.reply_message(
        event.reply_token,
        message) 

#初始化產品資訊
@app.before_first_request
def init_products():
    # init db
    result = init_db()#先判斷資料庫有沒有建立，如果還沒建立就會進行下面的動作初始化產品
    if result:
        init_data = [Products(name='SPA',
                              product_image_url='https://i.imgur.com/DKzbk3l.jpg',
                              price=150,
                              description='給你極致的想享受'),
                     Products(name='美甲美睫',
                              product_image_url='https://i.imgur.com/PRTxyhq.jpg',
                              price=120,
                              description='給你極致的想享受'),
                     Products(name='游泳池',
                              price=180,
                              product_image_url='https://i.imgur.com/PRm22i8.jpg',
                              description='大型浴池')]
        db_session.bulk_save_objects(init_data)#透過這個方法一次儲存list中的產品
        db_session.commit()#最後commit()才會存進資料庫
        #記得要from models.product import Products在app.py


if __name__ == "__main__":
    init_products()
    app.run()