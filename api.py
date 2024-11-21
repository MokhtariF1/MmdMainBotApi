from fastapi import FastAPI
from fastapi.responses import Response
import helper
import json
import config


app = FastAPI()


@app.get("/get-service/")
async def get_service(number):
    try:
        username, password, client_id = await helper.get_service(num=number)
        if username is None or password is None or client_id is None:
            response = {
                "status": 500,
            }
            return Response(json.dumps(response), 500)
        else:
            response = {
                "status": 200,
                "username": username,
                "password": password,
                "client_id": client_id
            }
            text = f"""✅ #سرویس جدید
➖➖➖➖➖➖➖➖➖
👤نام کاربری : {username}
🔑پسورد : {password}
"""
            await helper.send_telegram_message(config.REPORT_CHANNEL_ID, text)
            return Response(json.dumps(response), 200)
    except Exception as e:
        print(e)
        response = {
            "status": 500,
        }
        return Response(json.dumps(response), 500)

@app.get("/service-extension/")
async def service_extension(client_id, number):
    try:
        status = await helper.service_extension(client_id=client_id, plan_id=number)
        if status is None:
            response = {
                "status": 500,
            }
            return Response(json.dumps(response), 500)
        else:
            if status == 500:
                response = {
                    "message": "an error to service extension",
                    "status": 500,
                }
                return Response(json.dumps(response), 500)
            else:
                response = {
                    "message": "plan added to user service!",
                    "status": 200,
                }
                return Response(json.dumps(response), 200)
    except Exception as e:
        print(e)
        response = {
            "status": 500,
        }
        return Response(json.dumps(response), 500)


@app.get("/client-info/")
async def client_info_http(username):
    try:
        status = await helper.client_info(username)
        if status is None:
            response = {
                "status": 500,
            }
            return Response(json.dumps(response), 500)
        else:
            if status == 500:
                response = {
                    "message": "an error to get service details!",
                    "status": 500,
                }
                return Response(json.dumps(response), 500)
            else:
                response = {
                    "message": "plan finded!",
                    "info": status,
                    "status": 200,
                }       
                return Response(json.dumps(response), 200)
    except Exception as e:
        print(e)
        response = {
            "status": 500,
        }
        return Response(json.dumps(response), 500)
