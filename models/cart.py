from cachelib import SimpleCache
from linebot.models import *
from database import db_session
from models.product import Products
from app import *

cache = SimpleCache()

class Cart(object):
    def __init__(self, user_id):
        self.cache = cache
        self.user_id = user_id
    
    def bucket(self):
        return cache.get(key=self.user_id) or {}

    def add(self, product, num):
        bucket = self.bucket()
        if bucket == None:
            cache.add(key=self.user_id, value={product: int(num)})
        else:
            bucket.update({product: int(num)})
            cache.set(key=self.user_id, value=bucket)

    def reset(self): #清空購物車
        cache.set(key=self.user_id, value={})

    def display(self):#
        total = 0#總金額
        product_box_component = []#放置產品明細

        for product_name, num in self.bucket().items():
            #透過 Products.name 去搜尋
            product = db_session.query(Products).filter(Products.name.ilike(product_name)).first()
            amount = product.price * int(num)#然後再乘以購買的數量
            total += amount
            #透過 TextComponent 顯示產品明細，透過BoxComponent包起來，再append到product_box_component中
            product_box_component.append(BoxComponent(
                layout='horizontal',
                contents=[
                    TextComponent(text='{num} x {product}'.format(num=num,
                                                                  product=product_name),
                                  size='sm', color='#555555', flex=0),
                    TextComponent(text='NT$ {amount}'.format(amount=amount),
                                  size='sm', color='#111111', align='end')]
            ))

        bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='Here is your order.',
                                  wrap=True,
                                  size='md'),
                    SeparatorComponent(margin='xxl'),#顯示分隔線
                    BoxComponent(
                        layout='vertical',
                        margin='xxl',
                        spacing='sm',
                        contents=product_box_component
                    ),
                    SeparatorComponent(margin='xxl'),
                    BoxComponent(
                        layout='vertical',
                        margin='xxl',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='horizontal',
                                contents=[
                                    TextComponent(text='TOTAL',
                                                  size='sm',
                                                  color='#555555',
                                                  flex=0),
                                    TextComponent(text='NT$ {total}'.format(total=total),
                                                  size='sm',
                                                  color='#111111',
                                                  align='end')]
                            )

                        ]
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='md',
                contents=[
                    ButtonComponent(
                        style='primary',
                        color='#1DB446',
                        action=PostbackAction(label='Checkout',
                                              display_text='checkout',
                                              data='action=checkout')
                    ),
                    BoxComponent(
                        layout='horizontal',
                        spacing='md',
                        contents=[
                            ButtonComponent(
                                style='primary',
                                color='#aaaaaa',
                                flex=3,
                                action=MessageAction(label='Empty Cart',
                                                     text='Empty cart'),
                            ),
                            ButtonComponent(
                                style='primary',
                                color='#aaaaaa',
                                flex=2,
                                action=MessageAction(label='Add',
                                                     text='add'),
                            )
                        ]

                    )
                ]
            )
        )

        message = FlexSendMessage(alt_text='Cart', contents=bubble)

        return message#會回傳到app.py message = cart.display()

    def ordering(self,event):
        message_text = str(event.message.text).lower()
        product_name = message_text.split(',')[0]#利用split(',')拆解並取得第[0]個位置的值
        # 例如 Coffee,i'd like to have經過split(',')拆解並取得第[0]個位置後就是 Coffee
        num_item = message_text.rsplit(':')[1]#同理產品就用(':')拆解取得第[1]個位置的值
        #資料庫搜尋是否有這個產品名稱
        product = db_session.query(Products).filter(Products.name.ilike(product_name)).first()
        #如果有這個產品名稱就會加入
        if product:

            self.add(product=product_name, num=num_item)
            #然後利用confirm_template的格式詢問用戶是否還要加入？
            confirm_template = ConfirmTemplate(
                text='Sure, {} {}, anything else?'.format(num_item, product_name),
                actions=[
                    MessageAction(label='Add', text='add'),
                    MessageAction(label="That's it", text="That's it")
                ])

            message = TemplateSendMessage(alt_text='anything else?', template=confirm_template)

        else:
            #如果沒有找到產品名稱就會回給用戶沒有這個產品
            message = TextSendMessage(text="Sorry, We don't have {}.".format(product_name))
        print(self.bucket())
        return  message
        
