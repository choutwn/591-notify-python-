import os
import requests
import renthouse, getsql
import emoji


#notify設定
def notify(msg,image_path,token):
    
    url = "https://notify-api.line.me/api/notify"         # Notify網址 
    headers = {"Authorization": "Bearer " + token}        # HTTPS表頭
    payload = {"message": msg}                            # HTTPS內容
    
    #使用特定圖片路徑
    with open(image_path, 'rb') as image:
       imageFile = {'imageFile': image}
       response = requests.post(url, headers=headers, data=payload, files=imageFile)
       
       if response.status_code == 200:
           print("通知成功")
       else:
           print("通知失敗，狀態碼:", response.status_code)
       

#取得資料庫中的data,renthouse中的網址與照片
def get_data():
    
    desktop_path=r'C:\Users\choutwn\Desktop\租屋圖片'
    
    #引用別的py檔匯入資料
    data=getsql.show_rent_house()  
    url=renthouse.get_img_data()
    
    #取得最後三段網址
    last_three_url= [x[0] for x in url[-3:]]  
    #取得所有圖片    
    all_images = [f for f in os.listdir(desktop_path) if f.endswith(('.jpg'))]
    all_images_paths = [os.path.join(desktop_path, f) for f in all_images]  
    
    #排序照片
    latest_images = sorted(all_images_paths, key=os.path.getmtime, reverse=True)[:3] 
    
    return last_three_url,latest_images,data


def sendMessage(token):
    
    last_three_urls,latest_images,data =get_data()  
    
    #將data轉成list資料型態
    data = list(data)
    
    #把迴圈中的data[0]與data[2]對調，好配對照片與網址
    data[0],data[2] = data[2],data[0]
    
    for i in range(3):
        # 如果 i 是 0 和 2，對調 image_path
        if i == 0:
            image_path = latest_images[2]  # 第三張圖片
        elif i == 2:
            image_path = latest_images[0]  # 第一張圖片
        else:
            image_path = latest_images[1]  # 第二張圖片
        
        msg=(emoji.emojize('\n小幫手來啦~ \U0001F607 \n租屋網更新資訊! \U0001F4A5  \n\n \U0001F4E2  ') +
        data[i][1] + 
        emoji.emojize('\n \U0001F3E0  ') + data[i][2] +
        emoji.emojize('\n \U0001F4DD  ') + data[i][3] + 
        emoji.emojize('\n \U0001F4B4  ') + data[i][4] +
        emoji.emojize('\n \U000023F0  ') + '3小時內更新' +
        emoji.emojize('\n\n \U0001F3E0   看更詳細點↓網址 \n ') + 
        last_three_urls[i])
             
        
        
        notify(msg, image_path, token)
        
token='HvKyDXZSIr2yWCY2PY4kEnnk0PiqOU5f0tSRuKd2kVG'
sendMessage(token)

