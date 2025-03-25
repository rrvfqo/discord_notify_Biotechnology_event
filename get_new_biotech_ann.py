'''
查詢公告快易查網站，取得生技公告，關鍵字為"批准"
'''


import requests
import json
from datetime import datetime  
import os


# 台灣證券交易所公告網址
announcement_url = "https://mopsov.twse.com.tw/mops/web/ezsearch_query"

# 紀錄已發送的公告檔案路徑
sent_announcements_file = "sent_announcements.txt"
# 紀錄上次檢查日期的檔案路徑
last_checked_date_file = "last_checked_date.txt"

def load_sent_announcements():
    if os.path.exists(sent_announcements_file):
        with open(sent_announcements_file, "r", encoding="utf-8") as file:
            return set(line.strip() for line in file if line.strip())
    return set()

def save_sent_announcements(sent_announcements):
    with open(sent_announcements_file, "w", encoding="utf-8") as file:
        for announcement in sent_announcements:
            file.write(announcement + "\n")

def load_last_checked_date():
    if os.path.exists(last_checked_date_file):
        with open(last_checked_date_file, "r", encoding="utf-8") as file:
            return file.read().strip()
    return None

def save_last_checked_date(date):
    with open(last_checked_date_file, "w", encoding="utf-8") as file:
        file.write(date)

# 紀錄已發送的公告
sent_announcements = load_sent_announcements()

# 紀錄上次檢查日期
last_checked_date = load_last_checked_date()

def get_sii_announcement():

    today = datetime.now().strftime('%Y%m%d')

    # 上市公司公告參數，關鍵字為"批准"
    announcement_body =  f'step=00&RADIO_CM=1&TYPEK=sii&CO_MARKET=22&CO_ID=&PRO_ITEM=&SUBJECT=%E6%89%B9%E5%87%86&SDATE={today}&EDATE=&lang=TW&AN='

    # 取得公告資訊
    response = requests.post(announcement_url, data=announcement_body)

    if response.status_code == 200:
        # 移除 UTF-8 BOM
        json_data = response.text.lstrip('\ufeff')
        # 將 JSON 資料轉換為 Python dict
        response_dict = json.loads(json_data)
        return response_dict
    return {"data": [], "message": ["查無公告資料"], "status": "fail"}

def get_otc_announcement():

    today = datetime.now().strftime('%Y%m%d')

    # 上市公司公告參數，關鍵字為"批准"
    announcement_body =  f'step=00&RADIO_CM=1&TYPEK=otc&CO_MARKET=22&CO_ID=&PRO_ITEM=&SUBJECT=%E6%89%B9%E5%87%86&SDATE={today}&EDATE=&lang=TW&AN='


    # 取得公告資訊
    response = requests.post(announcement_url, data=announcement_body)
    

    if response.status_code == 200:
        # 移除 UTF-8 BOM
        json_data = response.text.lstrip('\ufeff')
        # 將 JSON 資料轉換為 Python dict
        response_dict = json.loads(json_data)
        return response_dict
    return {"data": [], "message": ["查無公告資料"], "status": "fail"}

def check_new_announcements():
    global last_checked_date
    today = datetime.now().strftime('%Y%m%d')
    
    # 如果跨日，清空 sent_announcements
    if today != last_checked_date:
        sent_announcements.clear()
        save_sent_announcements(sent_announcements)
        last_checked_date = today
        save_last_checked_date(today)

    sii_response_dict = get_sii_announcement()
    otc_response_dict = get_otc_announcement()

    new_announcements = []

    if sii_response_dict["status"] == "success":
        for announcement in sii_response_dict["data"]:
            announcement_text = announcement["SUBJECT"]
            if announcement_text not in sent_announcements:
                new_announcements.append(announcement)
                sent_announcements.add(announcement_text)
    
    if otc_response_dict["status"] == "success":
        for announcement in otc_response_dict["data"]:
            announcement_text = announcement["SUBJECT"]
            if announcement_text not in sent_announcements:
                new_announcements.append(announcement)
                sent_announcements.add(announcement_text)
    
    if new_announcements:
        # 處理新公告，例如發送通知
        print("有新的公告：")
        for announcement in new_announcements:
            announcement_details = f"{announcement['CDATE']}\n{announcement['COMPANY_ID']}{announcement['COMPANY_NAME']}\n{announcement['SUBJECT']}\n{announcement['HYPERLINK']}"
            print(announcement_details)
        save_sent_announcements(sent_announcements)  # 儲存已發送的公告
    else:
        print("沒有新的公告")

    return new_announcements


if __name__ == "__main__":

    check_new_announcements()





