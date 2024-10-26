import requests
from bs4 import BeautifulSoup
import pandas as pd
import MySQLdb
import os
import re
from datetime import datetime

#建立照片庫

desktop_img=r'C:\Users\choutwn\Desktop\租屋圖片'
if not os.path.exists(desktop_img):
    os.makedirs(desktop_img)



#取得目標網址
url='https://rent.591.com.tw/list?price=5000_10000,10000_20000,20000_30000'

#取得偽裝表頭
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
         AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}
lst1 = []
lst2 = []   
count = 0

#向網頁請求 
response = requests.get(url,headers=headers)

#用soup解析
soup = BeautifulSoup(response.text,'lxml')

#找到父標籤
info = soup.find('div',class_='wares-container-wrapper')

#找到所有子標籤
tags = info.find_all('div',class_='recommend-ware')
      
#套入迴圈找尋目標 
for row in tags:
    #只抓取前8筆
    if count >= 8:
        break
    
    #找尋標題，清理不適合的字元           
    title = row.find('a',class_='title').text.strip()
    safe_title = re.sub(r'[\\/*?:"<>|]', "_", title)
    #找尋地址             
    address = row.find('div',class_='address-info').text.strip()     
    distance = row.find('div',class_='distance-info')   
    #找尋距離           
    distance_text = distance.text.strip() if distance else ''        
    #找尋價格
    price = row.find('div',class_='price-info').text.strip().replace(',',"")
           
    #找照片與資料網頁
    pic = row.find('li').find('img')
    img = pic.get('data-src') if pic and pic.get('data-src') else ''   
    img_url = row.find('a',class_='img-container').get('href')  \
    
    #將照片存入資料夾(租屋照片)
    img_data = requests.get(img).content  #圖片網址
    img_name = "%s.jpg"%safe_title    #檔名"image_標題.jpg" 
    
    img_path = os.path.join(desktop_img,img_name)
    
    with open(img_path,'wb')as file:
        
        file.write(img_data)
        print('已下載圖片%s'%img_name)
    
    lst2.append([img_url,img])  #圖片與網址加入ls2
    
    lst1.append([title,address,distance_text,price])
    
    count+=1
    

#將lst1的資料加入DataFarame    
data = pd.DataFrame(lst1,columns=['標題','地址','距離','價格'])


#將抓到的圖片與網址另外寫方法供其他檔案使用
def get_img_data():
    
    return lst2


#取得當前時間
today = datetime.now()
print(today)

#=====================================================
# 將資料寫入資料庫
#=====================================================
try:
    conn = MySQLdb.connect(host="localhost",
                         user="root",
                         password="hungter7",
                         database="591rent",
                         port=3306,
                         charset="utf8")
    
    cursor = conn.cursor()
    
    try:                                         #插入資料進資料庫
        for i in range(len(data)):
            sql = """INSERT INTO RentHouse(date,title,address,distance,price)
                                        VALUES(%s, %s, %s, %s, %s)"""
            var = (today,data.iloc[i,0],data.iloc[i,1],data.iloc[i,2],data.iloc[i,3])
            cursor.execute(sql,var)
        conn.commit()
        print('資料寫入完成')
        conn.close()
        
    except Exception as e:
        print('錯誤訊息',e)
        
except Exception as e:
    print('資料庫連接失敗',e)
    
finally:
    print('資料庫連線結束')












    
    
