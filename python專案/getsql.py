import MySQLdb

#找尋資料庫倒數3筆資料

def show_rent_house():
    
    try:
        
        conn=MySQLdb.connect(host="localhost",
                             user="root",
                             password="hungter7",
                             database="591rent",
                             port=3306,
                             charset="utf8")
        cursor=conn.cursor()
        
        try:
            
            sql="""SELECT date,title,address,distance,price 
                   FROM RentHouse
                   ORDER BY ID DESC
                   LIMIT 3;"""
                   
            cursor.execute(sql)
            data=cursor.fetchall()

            return data
        
            conn.close()
            
            
        except Exception as e:
            print('錯誤訊息',e)
            
    except Exception as e:
        print('資料庫連線失敗',e)
        
    finally:
        print('資料庫連線結束')
        
    

