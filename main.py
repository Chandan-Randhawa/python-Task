from fastapi import FastAPI
from starlette.responses import JSONResponse
import Constants
import re 
import asyncio as aio
import redis 

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def validate_email(email):
    if(re.fullmatch(regex, email)):
        return True
    return False
   
app = FastAPI()

try :
    @app.post("/sendEmail")
    async def task_mailing(email: str): 
        if not email:
            return JSONResponse(status_code=400, content={"message": "Missing Request Parameter Email"})
        if not validate_email(email):
            return JSONResponse(status_code=400, content={"message": "Invalid Email"})
        publish_to_redis(email)
        return JSONResponse(status_code=200, content={"message": "email has been sent"})
except Exception as error:
    print (error)

def publish_to_redis(email):
    redis_pub = redis.Redis.from_url(Constants.redis_host)
    try:
        redis_pub.publish(Constants.channel, email)
    except (ConnectionError, aio.TimeoutError, aio.CancelledError):
        pass



