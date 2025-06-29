from fastapi import FastAPI
from fastapi.responses import Response
import helper
import json
import config
from config import plan_names, amounts

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
async def get_service_rep(number: int, user_id: int, rep_code: str):
    db_path = helper.get_db_path()
    # find_rep = helper.execute_with_retry(db_path=db_path, query=f"SELECT * FROM users WHERE rep_code = '{rep_code}'")
    user_inventory = None
    result = None
    with helper.sqlite_connection(db_path) as conn:
        cursor = conn.cursor()
        result = cursor.execute(f"SELECT * FROM users WHERE rep_code='{rep_code}'").fetchone()
        conn.commit()
        if result is None:
            return Response(json.dumps({"status": 404, "message": "user not found"}), 404)
        user_inventory = result[1]
        service_price = amounts[number] // 2
        if (user_inventory - service_price) < 0:
            return Response(json.dumps({"status": 403, "message": "inventory is none!"}), 403)
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
                plan_name = plan_names[number]
                rep_after_inventory = user_inventory - service_price
                cursor.execute(f"UPDATE users SET inventory={rep_after_inventory} WHERE rep_code='{rep_code}'")
                conn.commit()
                text = f"""📣 جزئیات ساخت اکانت در ربات نماینده شما ثبت شد .
    ▫️آیدی عددی کاربر : {user_id}
    ▫️آیدی عددی نماینده : {result[0]}
    ▫️نام کاربری کانفیگ :{username}
    ▫️رمز عبور کانفیگ :{password}
    ▫️پلن سرویس : {plan_name}
    ▫️موجودی نماینده قبل از خرید :{user_inventory} تومان
    ▫️موجودی نماینده قبل از خرید : {rep_after_inventory}"""
                await helper.send_telegram_message(config.REPORT_CHANNEL_ID, text)
                return Response(json.dumps(response), 200)
        except Exception as e:
            print(e)
            response = {
                "status": 500,
            }
            return Response(json.dumps(response), 500)


@app.get("/service-extension-rep/")
async def service_extension_rep(number: int, username: str, rep_code: str, user_id: int):
    db_path = helper.get_db_path()
    # find_rep = helper.execute_with_retry(db_path=db_path, query=f"SELECT * FROM users WHERE rep_code = '{rep_code}'")
    user_inventory = None
    result = None
    with helper.sqlite_connection(db_path) as conn:
        cursor = conn.cursor()
        result = cursor.execute(f"SELECT * FROM users WHERE rep_code='{rep_code}'").fetchone()
        conn.commit()
        if result is None:
            return Response(json.dumps({"status": 404, "message": "user not found"}), 404)
        user_inventory = result[1]
        service_price = amounts[number] // 2
        if (user_inventory - service_price) < 0:
            return Response(json.dumps({"status": 403, "message": "inventory is none!"}), 403)
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
                    plan_name = plan_names[number]
                    rep_after_inventory = user_inventory - service_price
                    cursor.execute(f"UPDATE users SET inventory={rep_after_inventory} WHERE rep_code='{rep_code}'")
                    conn.commit()
                    text = f"""📣 جزئیات تمدید سرویس در ربات نماینده شما ثبت شد .
                    ▫️آیدی عددی کاربر : {user_id}
                    ▫️آیدی عددی نماینده : {result[0]}
                    ▫️نام کاربری کانفیگ :{username}
                    ▫️پلن سرویس : {plan_name}
                    ▫️موجودی نماینده قبل از خرید :{user_inventory} تومان
                    ▫️موجودی نماینده قبل از خرید : {rep_after_inventory}"""
                    await helper.send_telegram_message(config.REPORT_CHANNEL_ID, text)
                    return Response(json.dumps(response), 200)
        except Exception as e:
            print(e)
            response = {
                "status": 500,
            }
            return Response(json.dumps(response), 500)
