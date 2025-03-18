'''
查詢公告快易查網站，取得生技公告，關鍵字為"批准"
'''

import sys
import requests

from get_new_biotech_ann import check_new_announcements  # 匯入函式



def notify_discord_webhook(msg):
    url = 'https://discord.com/api/webhooks/1328584537604751473/NRX45NRVkqrlaBWqBKTDLeYLa-rVnzBgQnT4L5QdBZYu2AxK7quw4yeXiTHDwMSXIJS9'
    headers = {"Content-Type": "application/json"}
    data = {"content": msg, "username": "公告-生技"}
    res = requests.post(url, headers = headers, json = data) 
    if res.status_code in (200, 204):
            print(f"Request fulfilled with response: {res.text}")
    else:
            print(f"Request failed with response: {res.status_code}-{res.text}")


def generate_msg():
    new_announcements = check_new_announcements()  # 呼叫函式取得新公告
    if new_announcements:
        msg = '\n\n'.join(
            f"{announcement['CDATE']}\n{announcement['COMPANY_ID']} {announcement['COMPANY_NAME']}\n{announcement['SUBJECT']}\n{announcement['HYPERLINK']}"
            for announcement in new_announcements
        )
        return msg
    return None

def job():
    msg = generate_msg()
    if msg:
        # 如果msg超過2000字元，分段發送
        if len(msg) > 2000:
            msg_list = [msg[i:i+2000] for i in range(0, len(msg), 2000)]
            for msg in msg_list:
                notify_discord_webhook(msg)
        else:
            notify_discord_webhook(msg)
    else:
        print("沒有新的公告")


def signal_handler(sig, frame):
    global running
    print('Stopping the scheduler...')
    running = False
    sys.exit(0)

if __name__ == "__main__":

    job()

