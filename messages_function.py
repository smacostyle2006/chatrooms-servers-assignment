import asyncio
import requests
from datetime import datetime

import config as cfg

async def pull_messages(message_number):
    while True:
        r = requests.get(cfg.HOST + "/messages")

        messages = r.json()

        for msg in messages["messages"][message_number:]:
            full_stamp = f"{msg['date']} {msg['time']}"
            print(f"[{full_stamp}] {msg['username']}: {msg['content']}")
            message_number += 1
        await asyncio.sleep(0.2)
        

async def send_message(username):
    while True:
        msg = await asyncio.to_thread(input, "> ")
        msg = msg.strip()

        if msg == "":
            continue

        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")

        requests.post(
            cfg.HOST + "/send",
            data={
                "username": username,
                "content": msg,
                "date": date_str,
                "time": time_str
            }
        )

async def run_messages(username, message_number):
    await asyncio.gather(
        pull_messages(message_number),
        send_message(username),
    )