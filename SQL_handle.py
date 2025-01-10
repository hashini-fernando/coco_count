import mysql.connector
import datetime,timedelta
import csv
import shutil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
ct = datetime.datetime.now()

mydb1 = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "Hashini@123",
        database = "coconut",
       
)

mydb2 = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "Hashini@123",
        database = "backup",
        
)

#insert in to table when count is reset to 0
def reset(time):
    mycursor = mydb1.cursor() 
    sqlFormula2 = "INSERT INTO data (Datetime,Count) VALUES (%s,%s)"
    datatransmit2 = (time,0)
    mycursor.execute(sqlFormula2,datatransmit2)
    mydb1.commit()

#get the most recent value from the count table 

def countres():

    mydb2 = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "Hashini@123",
        database = "backup",
        
    )
    try:

        mycursor = mydb2.cursor() 
        query1 = "SELECT Count FROM count ORDER BY Datetime DESC LIMIT 1"
        mycursor.execute(query1)
        result = mycursor.fetchone()

        if result is None:
            # Handle the case where no rows were returned by the query
            diff = 0  # Default value, or handle as per your requirements
        else:
            diff = result[0]

        return diff
    finally:
        mydb2.close()



def countresw(time,c):
    mycursor = mydb2.cursor() 
    sqlFormula2 = "INSERT INTO count (Datetime,Count) VALUES (%s,%s)"
    datatransmit2 = (time,c)
    mycursor.execute(sqlFormula2,datatransmit2)
    mydb2.commit()

def countdel():
    mycursor = mydb2.cursor()
    clear_query = "DELETE FROM count"
    mycursor.execute(clear_query)
    mydb2.commit() 
    
def countresR(time):
    mycursor = mydb2.cursor()
    sqlFormula2 = "INSERT INTO count (Datetime,Count) VALUES (%s,%s)"
    datatransmit2 = (time,0)
    mycursor.execute(sqlFormula2,datatransmit2)
    mydb2.commit()

def get_total(cam_id):

    mydb1 = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "Hashini@123",
        database = "coconut",
       
    )
    try:
        if cam_id == 1:

            mycursor = mydb1.cursor() 
            query1 = "SELECT Cummulative_Count FROM totalizer ORDER BY Datetime DESC LIMIT 1"
            mycursor.execute(query1)
            result=mycursor.fetchone()
            diff=result[0]
            return diff
        
        elif cam_id == 2:
            
            mycursor = mydb1.cursor() 
            query1 = "SELECT Cummulative_Count FROM totalizer_reset ORDER BY Datetime DESC LIMIT 1"
            mycursor.execute(query1)
            result=mycursor.fetchone()
            diff=result[0]
            return diff
    
    finally:
            mydb1.close



def Get_DATA(time, count):

    mydb1 = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "Hashini@123",
        database = "coconut",
        
)

    
    mycursor = mydb1.cursor()

    query1 = "SELECT Count FROM data ORDER BY Datetime DESC LIMIT 1"
    mycursor.execute(query1)
    result=mycursor.fetchone()
    print(result)
    diff=count-result[0]

    if diff>0:
        query2 = "SELECT Cummulative_Count FROM totalizer ORDER BY Datetime DESC LIMIT 1"
        mycursor.execute(query2)
        res=mycursor.fetchone()
        res=res[0]
        print(f"res :{res}")
        sqlFormula1 = "INSERT INTO totalizer (Datetime,Count,Cummulative_Count) VALUES (%s,%s,%s)"
        datatransmit1 = (time,diff,(diff+res))
        mycursor.execute(sqlFormula1,datatransmit1)
        mydb1.commit()
    else:
        query3 = "SELECT Cummulative_Count FROM totalizer ORDER BY Datetime DESC LIMIT 1"
        mycursor.execute(query3)
        res=mycursor.fetchone()
        res=res[0]
        sqlFormula2 = "INSERT INTO totalizer (Datetime,Count,Cummulative_Count) VALUES (%s,%s,%s)"
        datatransmit2 = (time,0,res)
        mycursor.execute(sqlFormula2,datatransmit2)
        mydb1.commit()

    sqlFormula = "INSERT INTO data (Datetime,Count) VALUES (%s,%s)"
    datatransmit = (time,count)
    mycursor.execute(sqlFormula,datatransmit)
    mydb1.commit()
   
    # time1= datetime.datetime.strptime(str(time),"%Y-%m-%d %H:%M:%S")

    if time.minute==00:
        sqlFormula3 = "INSERT INTO log_hourly (Datetime,Hour_Count) VALUES (%s,%s)"
        datatransmit3 = (time,count)
        mycursor.execute(sqlFormula3,datatransmit3)
        mydb1.commit()
    else:
        pass


def Get_DATA_Reset(time, count):

    mydb1 = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "Hashini@123",
        database = "coconut",
        
)

    
    mycursor = mydb1.cursor()

  
    
    query1 = "SELECT Count FROM data_reset ORDER BY Datetime DESC LIMIT 1"
    mycursor.execute(query1)
    result=mycursor.fetchone()
    diff=count-result[0]

    if diff>0:
        query2 = "SELECT Cummulative_Count FROM totalizer_reset ORDER BY Datetime DESC LIMIT 1"
        mycursor.execute(query2)
        res=mycursor.fetchone()
        res=res[0]
        print(f"res :{res}")
        sqlFormula1 = "INSERT INTO totalizer_reset (Datetime,Count,Cummulative_Count) VALUES (%s,%s,%s)"
        datatransmit1 = (time,diff,(diff+res))
        mycursor.execute(sqlFormula1,datatransmit1)
        mydb1.commit()
    else:
        query3 = "SELECT Cummulative_Count FROM totalizer_reset ORDER BY Datetime DESC LIMIT 1"
        mycursor.execute(query3)
        res=mycursor.fetchone()
        res=res[0]
        sqlFormula2 = "INSERT INTO totalizer_reset (Datetime,Count,Cummulative_Count) VALUES (%s,%s,%s)"
        datatransmit2 = (time,0,res)
        mycursor.execute(sqlFormula2,datatransmit2)
        mydb1.commit()

    sqlFormula = "INSERT INTO data_reset (Datetime,Count) VALUES (%s,%s)"
    datatransmit = (time,count)
    mycursor.execute(sqlFormula,datatransmit)
    mydb1.commit()
   
    # time1= datetime.datetime.strptime(str(time),"%Y-%m-%d %H:%M:%S")

    if time.minute==00:
        sqlFormula3 = "INSERT INTO log_hourly_reset (Datetime,Hour_Count) VALUES (%s,%s)"
        datatransmit3 = (time,count)
        mycursor.execute(sqlFormula3,datatransmit3)
        mydb1.commit()
    else:
        pass


# def LogData(time,count):

#     mycursor = mydb1.cursor()
#     if time.hour==00:
#         sqlFormula4 = "INSERT INTO log_daily (Datetime,DAY_Count) VALUES (%s,%s)"
#         datatransmit4 = (time,count)
#         mycursor.execute(sqlFormula4,datatransmit4)
#         mydb1.commit()
#     else:
#         pass

#     query4 = "SELECT Datetime FROM log_weekly ORDER BY Datetime DESC LIMIT 1"
#     mycursor.execute(query4)
#     result1=mycursor.fetchone()
#     time2 = result1[0]
#     # time2= datetime.datetime.strptime(str(time2),"%Y-%m-%d %H:%M:%S")

#     seven_days = time2.date()
#     seven_days_later = seven_days + datetime.timedelta(days=7)

#     if time.date() >= seven_days_later :

#         query5 = "SELECT DAY_Count FROM log_daily ORDER BY Datetime DESC LIMIT 7"
#         mycursor.execute(query5)
#         results=mycursor.fetchall()
#         value=[result[0] for result in results]
#         total= sum(value)

#         # time2 = result[0]
#         # time2= datetime.datetime.strptime(str(time2),"%Y-%m-%d %H:%M:%S")
#         sqlFormula5 = "INSERT INTO log_weekly (Datetime,Week_Count) VALUES (%s,%s)"
#         datatransmit5 = (time,total)
#         mycursor.execute(sqlFormula5,datatransmit5)
#         mydb1.commit()
#     else:
#         pass

#     query6 = "SELECT Datetime FROM log_monthly ORDER BY Datetime DESC LIMIT 1"
#     mycursor.execute(query6)
#     result2=mycursor.fetchone()
#     time1=result2[0]

#     if time.month>time1.month:

#         i=time1.month
         
#         query7 =f"SELECT DAY_Count FROM log_daily WHERE MONTH(Datetime) = {i}"
#         mycursor.execute(query7)
#         results1=mycursor.fetchall()
#         value1=[result[0] for result in results1]
#         total1= sum(value1)
        
        
#         sqlFormula6 = "INSERT INTO log_monthly (Datetime,Month_Count) VALUES (%s,%s)"
#         datatransmit6 = (time,total1)
#         mycursor.execute(sqlFormula6,datatransmit6)
#         mydb1.commit()
#     else:
#         pass


#     # print("Resulting:",results1)
#     # print("Resulting:",result)
#     # print("Difference:",diff)

# # t= datetime.datetime.strptime(str('2024-08-20 00:05:28'),"%Y-%m-%d %H:%M:%S")
# # LogData(t,100)
# # Get_DATA(t,100)
# # print(ct)

    

#     mydb1.close()



def LogData(cam_id, time, count):

    

    mydb1 = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "Hashini@123",
    database = "coconut",
    
)
    mycursor = mydb1.cursor()

    if cam_id == 1:

        # Log daily data at midnight
        if time.hour == 0:
            sqlFormula4 = "INSERT INTO log_daily (Cam_id ,Datetime, DAY_Count) VALUES (%s ,%s, %s)"
            datatransmit4 = (cam_id, time, count )
            mycursor.execute(sqlFormula4, datatransmit4)
            mydb1.commit()

        # Log weekly data every 7 days
        query4 = "SELECT Datetime FROM log_weekly WHERE Cam_id = %s ORDER BY Datetime DESC LIMIT 1"
        mycursor.execute(query4 , (cam_id,))
        result1 = mycursor.fetchone()
        
        if result1 is not None:
            time2 = result1[0]
            seven_days_later = time2.date() + datetime.timedelta(days=7)
            
            if time.date() >= seven_days_later:
                query5 = "SELECT DAY_Count FROM log_daily WHERE Cam_id = %s ORDER BY Datetime DESC LIMIT 7"
                mycursor.execute(query5 , (cam_id,))
                results = mycursor.fetchall()
                total = sum([result[0] for result in results])

                sqlFormula5 = "INSERT INTO log_weekly (Cam_id ,Datetime, Week_Count) VALUES (%s %s, %s)"
                datatransmit5 = (cam_id, time, total)
                mycursor.execute(sqlFormula5, datatransmit5)
                mydb1.commit()

        # Log monthly data if the month has changed
        query6 = "SELECT Datetime FROM log_monthly WHERE Cam_id = %s  ORDER BY Datetime DESC LIMIT 1"
        mycursor.execute(query6 ,(cam_id,))
        result2 = mycursor.fetchone()


        if result2 is not None:
            time1 = result2[0]
            if time.month > time1.month:
                query7 = f"SELECT DAY_Count FROM log_daily WHERE Cam_id = %s AND MONTH(Datetime) = {time1.month}"
                mycursor.execute(query7 ,(cam_id, time1.month, time1.year))
                results1 = mycursor.fetchall()
                total1 = sum([result[0] for result in results1])

                sqlFormula6 = "INSERT INTO log_monthly (Cam_id ,Datetime, Month_Count) VALUES (%s %s, %s)"
                datatransmit6 = (time, total1)
                mycursor.execute(sqlFormula6, datatransmit6)
                mydb1.commit()

        mydb1.close()

        # print("Resulting:",results1)
        # print("Resulting:",result)
        # print("Difference:",diff)

    # t= datetime.datetime.strptime(str('2024-08-20 00:05:28'),"%Y-%m-%d %H:%M:%S")
    # LogData(t,100)
    # Get_DATA(t,100)
    # print(ct)
def insert_coconut_count(count):
    # Database connection
    conn = mysql.connector.connect(user='root', password='Hashini@123', host='localhost', database='coconut')
    cursor = conn.cursor()

    # Insert count into the database
    query = "INSERT INTO coconut_counts (count) VALUES (%s)"
    cursor.execute(query, (count,))
    
    # Commit and close the connection
    conn.commit()
    cursor.close()
    conn.close()



def store_hourly_resets():
    mydb1 = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Hashini@123",
        database="coconut"
    )
    mycursor = mydb1.cursor()
    
    current_time = datetime.datetime.now()
    
    # Only proceed if the current time is the start of the hour (i.e., minutes and seconds are 0)
    if current_time.minute == 0 and current_time.second == 0:
        # Calculate the number of resets in the last hour
        one_hour_ago = current_time - datetime.timedelta(hours=1)
        query = "SELECT count(*) FROM coconut_counts WHERE Datetime BETWEEN %s AND %s"
        mycursor.execute(query, (one_hour_ago, current_time))
        result = mycursor.fetchone()
        print(f"Reset count in the last hour: {result[0]}")

        # Store the reset count in the hourly_resets table
        sql_insert = "INSERT INTO log_hourly_reset (Datetime, Hour_Count) VALUES (%s, %s)"
        mycursor.execute(sql_insert, (current_time, result[0]))
        mydb1.commit()

        print(f"Hourly resets stored: {result[0]} at {current_time}")
    else:
        print("Not the start of the hour. Waiting for the next hour.")

    mydb1.close()


# Function to store daily resets
def store_daily_resets():
    mycursor = mydb1.cursor()
    current_time = datetime.datetime.now()
    start_of_day = current_time.replace(hour=0, minute=0, second=0, microsecond=0)

    # Calculate the number of resets in the current day
    query = "SELECT count(*) FROM coconut_counts WHERE Datetime BETWEEN %s AND %s"
    mycursor.execute(query, (start_of_day, current_time))
    result = mycursor.fetchone()

    # Store the reset count in the daily_resets table
    sql_insert = "INSERT INTO log_daily_reset (Datetime, Day_Count) VALUES (%s, %s)"
    mycursor.execute(sql_insert, (current_time, result[0]))
    mydb1.commit()

    print(f"Daily resets stored: {result[0]} at {current_time}")

# Function to store monthly resets
def store_monthly_resets():
    mycursor = mydb1.cursor()
    current_time = datetime.datetime.now()
    start_of_month = current_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Calculate the number of resets in the current month
    query = "SELECT count(*) FROM coconut_counts WHERE Datetime BETWEEN %s AND %s"
    mycursor.execute(query, (start_of_month, current_time))
    result = mycursor.fetchone()

    # Store the reset count in the monthly_resets table
    sql_insert = "INSERT INTO log_monthly_reset (Datetime, Month_Count) VALUES (%s, %s)"
    mycursor.execute(sql_insert, (current_time, result[0]))
    mydb1.commit()

    print(f"Monthly resets stored: {result[0]} at {current_time}")

# Function to store weekly resets
def store_weekly_resets():
    mycursor = mydb1.cursor()
    current_time = datetime.datetime.now()
    start_of_month = current_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Calculate the number of resets in the current month
    query = "SELECT count(*) FROM coconut_counts WHERE Datetime BETWEEN %s AND %s"
    mycursor.execute(query, (start_of_month, current_time))
    result = mycursor.fetchone()

    # Store the reset count in the monthly_resets table
    sql_insert = "INSERT INTO log_weekly_reset (Datetime, Week_Count) VALUES (%s, %s)"
    mycursor.execute(sql_insert, (current_time, result[0]))
    mydb1.commit()

    print(f"Weekly resets stored: {result[0]} at {current_time}")
    

# Log reset count for camera 2 (reset counter) to `camera2_reset_counter` table
def log_reset_count(time, count, camera_id=2):
    mycursor = mydb1.cursor()
    sqlFormula = "INSERT INTO camera2_reset_counter (Datetime, Count, camera_id) VALUES (%s, %s, %s)"
    datatransmit = (time, count, camera_id)
    mycursor.execute(sqlFormula, datatransmit)
    mydb1.commit()

def retrieve_last_reset_count(camera_id):
    mycursor = mydb1.cursor()
    if camera_id == 2:
        query = "SELECT Count FROM camera2_reset_counter WHERE camera_id = %s ORDER BY Datetime DESC LIMIT 1"
    else:
        query = "SELECT Count FROM camera1_counter WHERE camera_id = %s ORDER BY Datetime DESC LIMIT 1"
    mycursor.execute(query, (camera_id,))
    result = mycursor.fetchone()
    return result[0] if result else 0 