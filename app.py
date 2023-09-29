from flask import Flask,request,abort
from events.service import *
from line_bot_api import *
# from events.basic import *
# from events.admin import *
from extensions import db, migrate
from models.user import User    
from models.service_item import Service_Item

import os

app = Flask(__name__)#admin: !QAZ2wsx資料庫的帳號和密碼
#讓程式自己去判斷如果是測試端就會使用APP_SETTINGS

app.config.from_object(os.environ.get('APP_SETTINGS', 'config.DevConfig'))
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://reservation:kk4VynPz2FbwuaqYNrQc24db8r2TTOia@dpg-ck7v30vsasqs73cfise0-a.singapore-postgres.render.com/reservation_we30"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)
migrate.init_app(app, db)


#callback

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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    message_text = str(event.message.text).lower()
    user = User.query.filter(User.line_id == event.source.user_id).first()#取得user的第一筆資料
    #如果沒有user資料時，才會透過api去取得
    if not user:
        profile = line_bot_api.get_profile(event.source.user_id)#Line API 中說明get_profile可以取得的資料
        print(profile.display_name)
        print(profile.user_id)#相同的好以會因為不同的profile 而有不同的user_id

        user = User(profile.user_id, profile.display_name, profile.picture_url)
        db.session.add(user)
        db.session.commit()

    print(user.id)
    print(user.line_id)
    print(user.display_name)



    if message_text =='@預約服務':
        service_category_event(event)

    # elif message_text.startswith('*'):
    #     if event.source.user_id not in ['U135d0047f682b28ef4001bcb47d0d21f']:
    #         return
    #     if message_text in ['*data', '*d']:
    #         list_reservation_event(event)
    elif message_text == '@取消預約':
        pass

        


#接收postback的訊息
#parse_qsl解析data中的資料
@handler.add(PostbackEvent)
def handle_postback(event):
    #把傳進來的event儲存在postback.data中再利用parse_qsl解析data中的資料然漚轉換成dict
    data = dict(parse_qsl(event.postback.data))
    #建立好def service_event(event) function後要來這裡加上判斷式
    #直接呼叫service_event(event)

    if data.get('action') == 'service':
        service_event(event)
    elif data.get('action') == 'select_date':
        service_select_date_event(event)
    elif data.get('action') == 'select_time':
        service_select_time_event(event)
    elif data.get('action') == 'confirm':
        service_confirm_event(event)
    elif data.get('action') == 'confirmed':
        service_confirmed_event(event)
    elif data.get('action') == 'cancel':
        service_cancel_event(event)

    #用get()來取得data中的資料，好處是如果備有data時會顯示None，而不會出線錯物
    


@app.before_first_request

def init_products():
    with app.app_context():

        service_item_count = db.session.query(Service_Item).count()
        if service_item_count >0 :
            pass
        else:
            init_data=[
                Service_Item(
                            category='SPA',
                            img_url = 'https://i.imgur.com/XHkio0m.jpg',
                            title = '全身指壓',
                            duration = '90min',
                            description =  '指壓屬於東方式按摩，是一種強調經絡、穴道等特定位置的加壓按摩，透過按摩師的手指指尖、指腹、掌根等部位，以按壓、捏、敲打、搓揉等方式，刺激人體特定部位、放鬆深層肌肉，幫助能量經絡順暢流動、促進神經機能。',
                            price =100,
                            ),
                Service_Item(
                            category='SPA',
                            img_url = 'https://i.imgur.com/svAaI3j.jpg',
                            title = '足底按摩',
                            duration = '90min',
                            description =  '「腳底按摩」能藉著刺激各部位反射區，使血液循環順暢，排除積聚在體內的廢物或毒素，使新陳代謝作用正常運作，達到治療的效果。',
                            price =100,
                ),
                Service_Item(
                            category='美甲美睫',
                            img_url = 'https://i.imgur.com/9b42t9d.png',
                            title = '美甲',
                            duration = '一次',
                            description =  '打造專屬個人風格的亮麗指甲',
                            price =100,
                ),
                Service_Item(
                            category='美甲美睫',
                            img_url = 'https://i.imgur.com/auEtnrJ.jpg',
                            title = '美睫',
                            duration = '一次',
                            description =  '使您的雙眼閃閃動人',
                            price =100,
                )]
            db.session.add_all(init_data)
            db.session.commit()


if __name__ == '__main__':
    init_products()
    app.run()