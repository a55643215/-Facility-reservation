from line_bot_api import *
from urllib.parse import parse_qsl
import datetime


from extensions import db
from models.user import User
from models.reservation import Reservation #資料寫入資料庫中
from models.service_item import Service_Item
#預約相關功能都會寫在這邊
#增加多個服務項目




def service_category_event(event):
     image_carousel_template_message = TemplateSendMessage(
          alt_text = '請選擇想服務類別',
          template = ImageCarouselTemplate(
            columns = [
                 ImageCarouselColumn(
                    image_url = 'https://i.imgur.com/yQhVPNj.jpg',
                    action = PostbackAction(
                        label = 'SPA',
                        display_text = 'SPA',
                        data = 'action=service&category=SPA'
                    )
                 ),
                 ImageCarouselColumn(
                    image_url = 'https://i.imgur.com/tE5e5p3.jpg',
                    action = PostbackAction(
                        label = '美甲美睫',
                        display_text = '美甲美睫',
                        data = 'action=service&category=美甲美睫'
                    )
                 )
            ]
          )
     )
     line_bot_api.reply_message(
          event.reply_token,
          [image_carousel_template_message]
     )



def service_event(event):
    #底下三個要等上面的service建立後才寫，主要是要跑service的服務
    #data = dict(parse_qsl(event.postback.data))
    #bubbles=[]
    #for service_id in services:
    services = db.session.query(Service_Item).all()
    data = dict(parse_qsl(event.postback.data))
    bubbles = []

    for service in services:
            if service.category == data['category']:
                bubble = {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover",
                    "url": service.img_url
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": service.title,
                        "wrap": True,
                        "weight": "bold",
                        "size": "xl"
                    },
                    {
                        "type": "text",
                        "text": service.duration,
                        "size": "md",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": service.description,
                        "margin": "lg",
                        "wrap": True
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                        {
                            "type": "text",
                            "text": f"NT$ {service.price}",
                            "wrap": True,
                            "weight": "bold",
                            "size": "xl",
                            "flex": 0
                        }
                        ],
                        "margin": "xl"
                    }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "action": {
                        "type": "postback",
                        "label": "預約",
                        "data": f"action=select_date&service_id={service.id}",
                        "displayText": f"我想預約【{service.title} {service.duration}】"
                        },
                        "color": "#b28530"
                    }
                    ]
                }
                }

                bubbles.append(bubble)

    flex_message = FlexSendMessage(
         alt_text = '請選擇預約項目',
         contents={
              "type":"carousel",
              "contents":bubbles
         }
    )

    line_bot_api.reply_message(
         event.reply_token,
         [flex_message]
    )


def service_select_date_event(event):
    data = dict(parse_qsl(event.postback.data))

    weekdat_string={
          0:'一',
          1:'二',
          2:'三',
          3:'四',
          4:'五',
          5:'六',
          6:'日',
     }#休息日就拿掉

    business_day = [1,2,3,4,5,6]#休息日就拿掉

    quick_reply_buttons = []

    today = datetime.datetime.today().date()#取得當天日期
    #weekday()取得星期幾?0是星期一
    for x in range(0,5):
        day = today + datetime.timedelta(days=x)#透過datetime.timedelta()可以取得隔天的日期
        

        if day != 0 and (day.weekday() in business_day):
            quick_reply_button = QuickReplyButton(
                action = PostbackAction(label=f'{day}({weekdat_string[day.weekday()]})',
                                        text=f'我要預約{day}({weekdat_string[day.weekday()]})這天',
                                        data= f'action=select_time&service_id={data["service_id"]}&date={day}'))
            quick_reply_buttons.append(quick_reply_button)

    text_message = TextSendMessage(text="請問要預約哪一天？",
                                   quick_reply=QuickReply(items=quick_reply_buttons))
    
    line_bot_api.reply_message(
         event.reply_token,
         [text_message]
    )




#選擇時間功能
def service_select_time_event(event):
    data = dict(parse_qsl(event.postback.data))

    available_time=['11:00', '14:00' ,'17:00', '20:00'] #可以自己更改時間段

    quick_reply_buttons = []

    for time in available_time:
         quick_reply_button = QuickReplyButton(action= PostbackAction(label=time,
                                                                       text=f'{time}這個時段',
                                                                       data=f'action=confirm&service_id={data["service_id"]}&date={data["date"]}&time={time}'))
         quick_reply_buttons.append(quick_reply_button)

    text_message = TextSendMessage(text='請問要預約哪個時段？',
                                   quick_reply=QuickReply(items=quick_reply_buttons))
    
    line_bot_api.reply_message(
         event.reply_token,
         [text_message]
    )

#
def service_confirm_event(event):
    services = db.session.query(Service_Item).all()
    data = dict(parse_qsl(event.postback.data))
    
    for service in services:
        if service.id == int(data['service_id']):
            booking_service = service#取得要預約的服務項目資料，會出現1234對應到上面的service

            confirm_template_message = TemplateSendMessage(
                alt_text='請確認預約項目',
                template = ConfirmTemplate(
                    text=f'您即將預約\n\n{booking_service.title} {booking_service.duration}\n預約時段: {data["date"]} {data["time"]}\n\n確認沒問題請按【確定】',
                    actions=[
                        PostbackAction(
                                label='確定',
                                display_text='確定沒問題！',
                                data=f'action=confirmed&service_id={data["service_id"]}&date={data["date"]}&time={data["time"]}'
                        ),
                        MessageAction(
                                label='重新預約',
                                text='@預約服務'
                        )
                    ]
                )
            )
            line_bot_api.reply_message(
                event.reply_token,
                [confirm_template_message]
            )


def is_booked(event, user):
    reservation = Reservation.query.filter(Reservation.user_id == user.line_id,
                                           Reservation.is_canceled.is_(False),#代表沒有被取消
                                           Reservation.booking_datetime > datetime.datetime.now()).first()
                                           #需要大於當下的時間.first()是會回傳第一筆資料
    if reservation:#text顯示預約項目名稱和服務時段
        buttons_template_message = TemplateSendMessage(
            alt_text='您已經有預約了，是否需要取消?',
            template=ButtonsTemplate(
                title='您已經有預約了',
                text=f'{reservation.booking_service}\n預約時段: {reservation.booking_datetime}',
                actions=[
                    PostbackAction(
                        label='我想取消預約',
                        display_text='我想取消預約',
                        data='action=cancel'
                    )
                ]
            )
        )

        line_bot_api.reply_message(
            event.reply_token,
            [buttons_template_message])

        return True
    else:
        return False



# def service_confirmed_event(event):
#      data = dict(parse_qsl(event.postback.data))

#      booking_service = services[int(data['service_id'])]
#      booking_datetime = datetime.datetime.strptime(f'{data["date"]}{data["time"]}', '%Y-%m-%d %H:%M')

#      user = User.query.filter(User.line_id == event.source.user_id).first()
#      if is_booked(event,user):
#           return
#      reservation = Reservation(
#           user_id= user.id,
#           booking_service_category=f'{booking_service["category"]}',
#           booking_service = f'{booking_service["title"]}{booking_service["duration"]}',
#           booking_datetime = booking_datetime 
#      )

#      db.session.add(reservation)
#      db.session.commit()

#      line_bot_api.reply_message(
#           event.reply_token,
#           [TextSendMessage(text='沒問題！感謝您的預約，我已經幫你預約成功了喔，到時候見！')]
#      )
def service_confirmed_event(event):
    data = dict(parse_qsl(event.postback.data))
    services = db.session.query(Service_Item).all()
    for service in services:
        if service.id == int(data['service_id']):
            booking_service = service
            booking_datetime = datetime.datetime.strptime(f'{data["date"]} {data["time"]}', '%Y-%m-%d %H:%M')

            user = User.query.filter(User.line_id == event.source.user_id).first()
            if is_booked(event, user):
                return

            reservation = Reservation(
                user_id=user.line_id,
                booking_service_category=f'{booking_service.category}',
                booking_service=f'{booking_service.title} {booking_service.duration}',
                booking_datetime=booking_datetime)

            db.session.add(reservation)
            db.session.commit()

            line_bot_api.reply_message(
                event.reply_token,
                [TextSendMessage(text='沒問題! 感謝您的預約，我已經幫你預約成功了喔，到時候見!')])
            
#取消預約 資料庫欄位不會drop,是 is_cacnceled欄位會變成true

def service_cancel_event(event):

    user = User.query.filter(User.line_id == event.source.user_id).first()
    reservation = Reservation.query.filter(Reservation.user_id == user.line_id,
                                           Reservation.is_canceled.is_(False),
                                           Reservation.booking_datetime > datetime.datetime.now()).first()
    if reservation:
        reservation.is_canceled = True

        db.session.add(reservation)
        db.session.commit()

        # line_bot_api.reply_message(
        #     event.reply_token,
        #     [TextSendMessage(text='您的預約已經幫你取消了')])
        buttons_cancel_message = TemplateSendMessage(
            alt_text='您的預約已幫你取消了！',
            template=ConfirmTemplate(
                text='您的預約已幫你取消了！',
                actions=[                     
                    MessageAction(
                        label='重新預約',
                        text='@預約服務'
                    ),
                    MessageAction(
                        label ='取消',
                        text='取消'
                    )
                ]
            )
        )
        line_bot_api.reply_message(
            event.reply_token,
            [buttons_cancel_message])
    else:
        buttons_cancel_message = TemplateSendMessage(
            alt_text='您的預約已幫你取消了！',
            template=ConfirmTemplate(
                text='您目前沒有預約喔！',
                actions=[                     
                    MessageAction(
                        label='我要預約',
                        text='@預約服務'
                    ),
                    MessageAction(
                        label ='取消',
                        text='取消'
                    )
                ]
            )
        )


        line_bot_api.reply_message(
            event.reply_token,
            [buttons_cancel_message])