'''
查詢公告快易查網站，取得生技公告，關鍵字為"批准"
'''


import requests
import json
from datetime import datetime
# import schedule
# import time
# import threading    


# 台灣證券交易所公告網址
announcement_url = "https://mopsov.twse.com.tw/mops/web/ezsearch_query"

# 紀錄已發送的公告
sent_announcements = set()

# 紀錄上次檢查日期
last_checked_date = datetime.now().strftime('%Y%m%d')

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
        last_checked_date = today

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
    else:
        print("沒有新的公告")

    return new_announcements

# # 設定每5秒鐘檢查一次公告
# schedule.every(5).minutes.do(check_new_announcements)

# def run_schedule():
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# if __name__ == "__main__":
#     # 啟動定時任務的背景執行緒
#     schedule_thread = threading.Thread(target=run_schedule)
#     schedule_thread.start()

#     # 主執行緒繼續執行其他任務
#     while True:
#         time.sleep(1)


    

