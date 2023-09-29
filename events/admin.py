from line_bot_api import *

from models.reservation import Reservation
import datetime
from extensions import db
from models.user import User
#用來顯示預約名單，過濾的條件為is)canceled.is_(False) 為 False

def list_reservation_event(event):
    reservations = Reservation.query.filter(Reservation.is_canceled.is_(False),
                                            Reservation.booking_datetime > datetime.datetime.now(),
                                            ).order_by(Reservation.booking_datetime.asc()).all()
    
    reservation_data_text = '## 預約名單: ## \n\n'
    #跑每一筆的預約資料
    for reservation in reservations:
        user=User.query.filter(User.id == reservation.user_id).first()
        
        reservation_data_text += f'''預約日期: {reservation.booking_datetime}
預約服務: {reservation.booking_service}
姓名: {user.display_name}\n'''

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reservation_data_text)
    )