import requests
import string
import config
import random
import json
import sqlite3
import time
from contextlib import contextmanager
import os


@contextmanager
def sqlite_connection(db_path):
    conn = None
    try:
        conn = sqlite3.connect(db_path, timeout=10)
        conn.execute('PRAGMA journal_mode=WAL;')
        yield conn
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise
    finally:
        if conn:
            conn.close()


def execute_with_retry(db_path, query, params=(), max_retries=3):
    for attempt in range(max_retries):
        try:
            with sqlite_connection(db_path) as conn:
                cursor = conn.cursor()
                result = cursor.execute(query, params)
                conn.commit()
                return result
        except sqlite3.OperationalError as e:
            if "locked" in str(e) and attempt < max_retries - 1:
                time.sleep(0.1 * (attempt + 1))
                continue
            raise


def get_db_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    db_path = os.path.join(parent_dir, config.BOT_DIR, "bot.db")
    return db_path


async def get_service(num, user_id):
    # Define the URL
    url = "https://api.connectix.vip/v1/seller/auth/login"

    # Define the headers
    headers = {
        "Host": "api.connectix.vip",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Origin": "https://seller.connectix.vip",
        "Connection": "keep-alive",
        "Referer": "https://seller.connectix.vip/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Priority": "u=0",
        "TE": "trailers"
    }

    # Define the parameters
    data = {
        "email": config.EMAIL,
        "password": config.PASSWORD,
        "rememberMe": False,
        "device_browser": "Firefox",
        "device_os": "Windows"
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.json())
    if response.status_code != 200:
        return None, None
    else:
        response_token = response.json()["token"]
        url = "https://api.connectix.vip/v1/seller/clients/store"

        # Define the headers
        headers = {
            "Host": "api.connectix.vip",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Authorization": f"Bearer {response_token}",
            "Origin": "https://seller.connectix.vip",
            "Connection": "keep-alive",
            "Referer": "https://seller.connectix.vip/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Priority": "u=0",
            "TE": "trailers"
        }

        # initializing size of string
        N = 5

        # using random.choices()
        # generating random strings
        res = ''.join(random.choices(string.ascii_lowercase +
                                     string.digits, k=N))
        data = {
            "password": str(res),
            "plan_id": config.plans_json[int(num)],
            "enable_plan_after_first_login": True
        }

        # Make the POST request
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response = response.json()
        print("_____", response)
        if response["message"] == "client has been created":
            text_to_copy = response["text_to_copy"]
            print(text_to_copy)
            username = text_to_copy.split("\n")[2][text_to_copy.split("\n")[2].index("username: ") + 11:].replace("`",
                                                                                                                  "")
            password = text_to_copy.split("\n")[3][text_to_copy.split("\n")[3].index("password: ") + 11:].replace("`",
                                                                                                                  "")
            return username, password, response["client_id"]
        else:
            print("error_khorde")
            # print(response)
            return None, None, None
    # if num == 1:
    #     price = 0
    #     expire = 1
    #     total = 1
    #     multi = 1
    # else:
    #     price = config.amounts[num]
    #     expire = config.expire_dates[num]
    #     total = config.data_limits[num]
    #     multi = config.user_counts[num]
    # username = ''.join(random.choices(string.ascii_letters, k=10))
    # password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
    # url = (f"{config.API_ADDRESS}?method=new_user&name={username}&pass={password}&total={total}&day={expire}&"
    #        f"id_from={user_id}&from_id={user_id}&price={int(price)}&multi={multi}")
    # response = requests.get(url)
    # print(response)
    # if response.status_code != 200:
    #     return None, None
    # else:
    #     return username, password


async def service_extension(plan_id, username):
    url = "https://api.connectix.vip/v1/seller/auth/login"

    # Define the headers
    headers = {
        "Host": "api.connectix.vip",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Origin": "https://seller.connectix.vip",
        "Connection": "keep-alive",
        "Referer": "https://seller.connectix.vip/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Priority": "u=0",
        "TE": "trailers"
    }

    # Define the parameters
    data = {
        "email": config.EMAIL,
        "password": config.PASSWORD,
        "rememberMe": False,
        "device_browser": "Firefox",
        "device_os": "Windows"
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))
    # print(response.json())
    if response.status_code != 200:
        return 500
    else:
        response_token = response.json()["token"]
        url = "https://api.connectix.vip/v1/seller/clients/add-plan"

        # Define the headers
        headers = {
            "Host": "api.connectix.vip",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Authorization": f"Bearer {response_token}",
            "Origin": "https://seller.connectix.vip",
            "Connection": "keep-alive",
            "Referer": "https://seller.connectix.vip/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Priority": "u=0",
            "TE": "trailers"
        }
        plan_id = config.plans_json[int(plan_id)]
        # Define the parameters
        data = {
            "id": username,
            "plan_id": plan_id,
        }
        print(data)
        # Make the POST request
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(response.json())
        # Print the response
        status = response.status_code
        if status != 200:
            return 500
        else:
            return 200
    # user_data = f"{config.API_ADDRESS}?method=data_user&name={username}&ADMIN=SpeedConnect"
    # user_data = requests.get(user_data).json()
    # # password_user = user_data["password"]
    # plan_total = config.data_limits[plan_id]
    # # plan_user_count = config.user_counts[plan_id]
    # plan_day = config.expire_dates[plan_id]
    # service_total = user_data["total"]
    # service_day = user_data["day"]
    # update_total = int(service_total) + int(plan_total)
    # update_day = int(service_day) + int(plan_day)
    # edit_user = f"{config.API_ADDRESS}?method=edit_user&name={username}&total={update_total}&day={update_day}&price={user_data['price']}"
    # response_update = requests.get(edit_user)
    # if response_update.status_code != 200:
    #     return None
    # else:
    #     return 200


async def client_info(username):
    url = "https://api.connectix.vip/v1/seller/auth/login"

    # Define the headers
    headers = {
        "Host": "api.connectix.vip",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Origin": "https://seller.connectix.vip",
        "Connection": "keep-alive",
        "Referer": "https://seller.connectix.vip/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Priority": "u=0",
        "TE": "trailers"
    }

    # Define the parameters
    data = {
        "email": config.EMAIL,
        "password": config.PASSWORD,
        "rememberMe": False,
        "device_browser": "Firefox",
        "device_os": "Windows"
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        return 500
    else:
        response_token = response.json()["token"]
        url = f"https://api.connectix.vip/v1/seller/clients?username={username}"
        headers = {
            "Authorization": f"Bearer {response_token}",
        }
        response = requests.get(url, headers=headers)
        print(response.status_code)
        if response.status_code != 200:
            return None
        else:
            response = response.json()
            data = response["clients"]["data"][0]
            return data
    # print(username)
    # user_data = f"{config.API_ADDRESS}?method=data_user&name={username}&ADMIN=SpeedConnect"
    # user_data = requests.get(user_data).json()
    # print(user_data)
    # try:
    #     user_data["result"]
    #     return None
    # except KeyError:
    #     return user_data


# تنظیمات تلگرام
TELEGRAM_API_URL = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage"


async def send_telegram_message(chat_id, text):
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    print(requests.post(TELEGRAM_API_URL, data=payload).json())


async def get_iphone_service(expire, data_limit):
    login_body = {
        "username": "mmd",
        "password": "mmd",
    }
    login_token = requests.post(f"{config.MARZBAN_API_URL}admin/token", data=login_body).json()["access_token"]
    username = f"user{random.choice(string.ascii_letters)}{random.randint(100000, 999999)}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {login_token}",
        "content-type": "application/json",
    }
    print(username)
    print(expire)
    data = {"username": username, "proxies": {"vless": {}}, "inbounds": {"vless": ["deco", "info", "upgrade"]},
            "expire": 0, "data_limit": data_limit, "data_limit_reset_strategy": "no_reset", "status": "on_hold",
            "note": "", "on_hold_timeout": "2023-11-03T20:30:00", "on_hold_expire_duration": expire}
    request = f"{config.MARZBAN_API_URL}user/"
    response = requests.post(request, json=data, headers=headers)
    sub = response.json()["subscription_url"]
    if response.status_code != 200:
        return None
    else:
        return username, sub
