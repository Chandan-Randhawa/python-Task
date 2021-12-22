from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import Constants
import os
import asyncio
import redis

redis_conn = redis.Redis.from_url(Constants.redis_host)

conf = ConnectionConfig(
    MAIL_USERNAME= os.environ.get('db_username'),
    MAIL_PASSWORD= os.environ.get('db_password'),
    MAIL_FROM= os.environ.get('db_username'),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True, 
    VALIDATE_CERTS=True
)

def send_email(email): 
    print(f'sending email to {email}')
    message = MessageSchema(
    subject=Constants.theme,
    recipients = [email],
    body=Constants.text,
)
    fm = FastMail(conf)
    asyncio.run(fm.send_message(message))
    return {"message": "email has been sent"}

def listen_send_email():
    processor = redis_conn.pubsub()
    processor.subscribe(Constants.channel)
    for raw_message in processor.listen():
        if raw_message["type"] != "message":
            continue
        try:    
            print(send_email(raw_message['data'].decode('utf-8')))
        except Exception as error:
            print (error)

listen_send_email()