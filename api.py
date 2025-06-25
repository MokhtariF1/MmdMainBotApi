from fastapi import FastAPI
from fastapi.responses import Response
import helper
import json
import config

app = FastAPI()


@app.get("/get-service/")
async def get_service(number, user_id):
    try:
        username, password, client_id = await helper.get_service(num=int(number), user_id=user_id)
        if username is None or password is None:
            response = {
                "status": 500,
            }
            return Response(json.dumps(response), 500)
        else:
            response = {
                "status": 200,
                "username": username,
                "password": password,
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
async def service_extension(number, username):
    try:
        status = await helper.service_extension(plan_id=int(number), username=username)
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
    print(username)
    try:
        status = await helper.client_info(username)
        if status is None:
            response = {
                "status": 500,
            }
            return Response(json.dumps(response), 500)
        else:
            print(status)
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


@app.get("/get-service-iphone/")
async def get_service_iphone(data_limit, expire):
    expire = int(expire) * 86400
    data_limit = int(data_limit)
    username, sub = await helper.get_iphone_service(expire, data_limit)
    if username is None:
        response = {
            "status": 500,
            "message": "cant make service"
        }
        return Response(json.dumps(response), 500)
    else:
        response = {
            "status": 200,
            "username": username,
            "sub_link": sub,
        }
        return Response(json.dumps(response), 200)


@app.get("/get-service-rep/")
async def get_service_rep(number, user_id, rep_code, user_inventory):
    db_path = helper.get_db_path()
    # find_rep = helper.execute_with_retry(db_path=db_path, query=f"SELECT * FROM users WHERE rep_code = '{rep_code}'")
    with helper.sqlite_connection(db_path) as conn:
        cursor = conn.cursor()
        result = cursor.execute(f"SELECT * FROM users WHERE rep_code='{rep_code}'").fetchone()
        conn.commit()
        print(result)

    # print(find_rep.fetchone())
#     try:

#         username, password, client_id = await helper.get_service(num=int(number), user_id=user_id)
#         if username is None or password is None:
#             response = {
#                 "status": 500,
#             }
#             return Response(json.dumps(response), 500)
#         else:
#             response = {
#                 "status": 200,
#                 "username": username,
#                 "password": password,
#             }
#             text = f"""✅ #سرویس جدید
# ➖➖➖➖➖➖➖➖➖
# 👤نام کاربری : {username}
# 🔑پسورد : {password}
# """
#             await helper.send_telegram_message(config.REPORT_CHANNEL_ID, text)
#             return Response(json.dumps(response), 200)
#     except Exception as e:
#         print(e)
#         response = {
#             "status": 500,
#         }
#         return Response(json.dumps(response), 500)
