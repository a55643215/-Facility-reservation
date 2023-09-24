
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FollowEvent, UnfollowEvent, 
    StickerSendMessage, ImageSendMessage, LocationSendMessage,FlexSendMessage,
    TemplateSendMessage,ImageCarouselTemplate,ImageCarouselColumn,PostbackAction,
    PostbackEvent,QuickReply,QuickReplyButton,ConfirmTemplate,MessageAction,ButtonsTemplate
)

line_bot_api = LineBotApi('MPmEhpbnNr+2OQEXtojRsjd0T26QgOWkpwiC/8dxHYPD6hFALEhJTTPWmFZcyf+C9U5easP5BAP1iS+1juuVT2dbCxEqlKgmZieTh44j0+tRvlvU6UUghi3SFoOzYcU/hD7gBQcJuGY5j/5nP/1ECQdB04t89/1O/w1cDnyilFU=')
# Channel access token
handler = WebhookHandler('a71b4c671ed9692546c0242ee0f00711') 
#Channel secret