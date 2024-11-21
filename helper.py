# from playwright.async_api import async_playwright
# import asyncio
# import config


# async def get_service(num):
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True, slow_mo=80)
#         page = await browser.new_page()
#         await page.goto("https://seller.connectix.vip/")
#         await page.get_by_label("Email").fill(config.EMAIL)
#         await page.get_by_label("Password").fill(config.PASSWORD)
#         await page.get_by_role("button", name="Login").click()
#         await page.get_by_role("link", name="Accounts").click()
#         await page.get_by_role("button", name="Create").click()
#         element_handle = await page.query_selector('input[placeholder="Client Password"]')
#         pass_wd = await page.evaluate('(element) => element.value', element_handle)
#         await page.get_by_label("PlanYou can add a plan(1x)").select_option(value=config.plans_json[int(num)])
#         await page.locator("#modalSection").get_by_role("button", name="Create").click()
#         username = await page.inner_html("span.mb-1.v-popper--has-tooltip")
#         return username, pass_wd

import requests
import json
import string
import config
import random
async def get_service(num):
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
        "email": "speedconnect2962@connectix.panel",
        "password": "%2kZpMtsx@R8qPE7pN!Brq4wPKYc^#",
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
        if response["message"] == "client has been created":
            text_to_copy = response["text_to_copy"]
            username = text_to_copy.split("\n")[2][text_to_copy.split("\n")[2].index("username: ")+11:].replace("`", "")
            password = text_to_copy.split("\n")[3][text_to_copy.split("\n")[3].index("password: ")+11:].replace("`", "")
            return username, password, response["client_id"]
        else:
            print(response)
            return None, None, None
async def service_extension(client_id, plan_id):
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
        "email": "speedconnect2962@connectix.panel",
        "password": "%2kZpMtsx@R8qPE7pN!Brq4wPKYc^#",
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

        # Define the parameters
        data = {
            "id": client_id,
            "plan_id": plan_id,
        }

        # Make the POST request
        response = requests.post(url, headers=headers, data=json.dumps(data))

        # Print the response
        status = response.status_code
        if status != 200:
            return 500
        else:
            return 200
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
        "email": "speedconnect2962@connectix.panel",
        "password": "%2kZpMtsx@R8qPE7pN!Brq4wPKYc^#",
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
        
# تنظیمات تلگرام
TELEGRAM_API_URL = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage"

async def send_telegram_message(chat_id, text):
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    print(requests.post(TELEGRAM_API_URL, data=payload).json())
