
#################### using cv2.imshow ###### (very slow)

import cv2
import imutils
import imutils.video

# RTSP URL for the camera stream
rtsp_url = "rtsp://admin:Rsroxbcscout*7@192.168.1.64:554/H.264?bitrate=256"

def display_camera_stream(rtsp_url):
    # Open the video stream
    cap = imutils.video.VideoStream(rtsp_url).start()
    # cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    # cap.set(cv2.CAP_PROP_FPS, 30)


    # Check if the video stream is successfully opened
    # if not cap.isOpened():
    #     print("Error: Unable to open the video stream.")
    #     return

    print("Press 'q' to quit.")

    # Read and display frames from the stream
    while True:
        frame = cap.read()
        
        if frame is None:
            print("Error: Unable to read a frame from the video stream.")
            break

        # Display the frame
        cv2.imshow('Camera Stream', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video stream and close the OpenCV windows
    cap.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    display_camera_stream(rtsp_url)











# import cv2
# import pandas as pd
# from ultralytics import YOLO
# from tracker import Tracker
# import imutils
# import threading
# from data import GetDATA,log_day_resets, Log_Data, Extract, Extract_hourly, Extract_daily, Extract_weekly, Extract_monthly, DELETE, createcsv,store_coconut_count,log_resets 
# from SQL_handle import log_reset_count,retrieve_last_reset_count,countres, countresw, get_total
# import datetime
# import schedule
# from SQL_Backup import backup



# # Model loading and setup
# # model = YOLO(r"D:\AVIOT\final\new_old\best.pt")

# # # Check if metadata contains version information
# # if 'meta' in model.ckpt:
# #     print("YOLO Version:", model.ckpt['meta'].get('version', 'Unknown'))
# # else:
# #     print("Metadata not available in the model.")

# # Reading COCO class list
# with open(r"D:\AVIOT\final\new_old\coco.txt", "r") as my_file:
#     class_list = my_file.read().split("\n")



# # Tracker setup
# tracker = Tracker()
# # unique_ids = set()
# idlist = {cam_id: [] for cam_id in range(2)}
# total_counters = {1: 0, 2: 0}  
# reset_limit = 20
# cy1 = 400
# cy2 = 250
# offset = 12
# IP = "rtsp://admin:Rsroxbcscout*7@192.168.1.64:554/H.264?bitrate=256"


# counter1 = 0
# counter2 = 0
# idlist = {1: [0], 2: [0]}
# idlist[1].append(0) 
# idlist[2].append(0) 


# i=0
# j = {1: 0, 2: 0}
# # Global variables for scheduling and time-based tasks
# pause = False
# days=1
# total =  0
# count2 = []
# count3 = []
# count4 = []
# count5 = []
# time_1 = []
# time_2 = []
# time_3 = []
# time_4 = []

# counter= {1: 0, 2: 0}



# # Getting the current time
# ct = datetime.datetime.now()


# # Function for 15-minute job
# def job_15_minutes():
#     for cam_id in counter:
#             global  ct
#             GetDATA(cam_id, ct, counter[1])
#             # GetDATARESET(2, ct ,counter[2])

    
#     # print("success")


# def initialize_counters():
#     # global counter_cam2
#     counter[2] = retrieve_last_reset_count(2)

# initialize_counters()


# # logging reset count in camera 2 table
# def log_camera2_count():
#     log_reset_count(datetime.datetime.now(), counter[2])

# # Function to pass data for various time intervals
# def passdata():
#     global time_1, time_2, time_3, time_4, count2, count3, count4, count5

#     time_1.clear()
#     time_2.clear()
#     time_3.clear()
#     time_4.clear()
    

#     time1, count2 = Extract_hourly()
#     time2, count3 = Extract_daily()
#     time3, count4 = Extract_weekly()
#     time4, count5 = Extract_monthly()
    

#     for time in time1:
#         time_1.append(time.strftime("%Y-%m-%d %H:%M:%S"))

#     for time in time2:
#         time_2.append(time.strftime("%Y-%m-%d %H:%M:%S"))

#     for time in time3:
#         time_3.append(time.strftime("%Y-%m-%d %H:%M:%S"))

#     for time in time4:
#         time_4.append(time.strftime("%Y-%m-%d %H:%M:%S"))

#     return time_1, time_2, time_3, count2, count3, count4, time_4, count5

# # Midnight job for resetting and backing up data
# def job_midnight():
#     for cam_id in counter:
#         global  ct 
#         Log_Data(cam_id, ct, counter[cam_id])
        
#         print("logdata")
#         createcsv(1)
#         DELETE(ct)
#         backup()

# def all_log_resets():
#     log_resets()
#     print("log")
    

# # def job_hour():
# #     log_hour_resets()
# def job_day():
#     log_day_resets()




# schedule.every(10).seconds.do(all_log_resets)
# # schedule.every().hour.do(job_hour)  # Run daily at midnight

# # schedule.every(7).days.do(store_weekly_resets)  
# # schedule.every().month.do(store_monthly_resets)  # Run monthly

# def rescount():
#         global counter1,ct,total,counter2

#         countresw(ct,counter1)
#         # y=Extract1()
#         # counter2=y

#         # h = plc_com(counter1,total)

#         # counter1=h

# # Function to reset the counter
# def reset_counter():
#     for cam_id in counter:
#         counter[cam_id] = 0
        
    

# # Scheduling tasks
# schedule.every(10).seconds.do(job_15_minutes)

# schedule.every(1).seconds.do(passdata)
# schedule.every(1).seconds.do(rescount)



# schedule.every().day.at("00:00").do(job_midnight)
# # schedule.every(1).seconds.do(job_midnight)
# schedule.every().day.at("00:00").do(reset_counter)


# def emit_data(self):
#         hourcount = count2
#         daycount= count3
#         weekcount = count4
#         monthcount = count5
#         # currenttime = time2
#         self.hour.emit(time_1,hourcount)
#         self.day.emit(time_2,daycount)
#         self.week.emit(time_3,weekcount)
#         self.month.emit(time_4,monthcount)



# # Main video processing loop
# def run(source, cam_id):
#     global j, ct, i,  counter1, counter2, count2, time_1, time_2, time_3, count3, count4, time_4, count5, total ,reset_limit

#     # Load video stream (RTSP or file)
#     cap = cv2.VideoCapture(source)
#     cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
#     cap.set(cv2.CAP_PROP_FPS, 30)
#     while True:
#         ct = datetime.datetime.now()

#         if not pause:
#             # Initialize counters if first run
#             if j[cam_id]== 0: 
#                 counter[1] = Extract()
#                 counter1 = countres()
#                 j[cam_id] = 1
#                 # print(j[cam_id])
#             else:
#                 counter[1] = counter[1]

#             # Read a frame from the video stream
#             ret, frame = cap.read()
#             if not ret:
#                 break  # End of video or error

#             total_counters[cam_id] = get_total(cam_id)
            
      
#             frame = imutils.resize(frame, width=1280, height=720)

#             # results = model.predict(frame, conf=0.5)
#             # a = results[0].boxes.data
#             # a_cpu = a.detach().cpu()
#             # a_numpy = a_cpu.numpy()

#             # px = pd.DataFrame(a_numpy).astype("float")

#             # list = []
#             # for index, row in px.iterrows():
#             #     x1 = int(row[0])
#             #     y1 = int(row[1])
#             #     x2 = int(row[2])
#             #     y2 = int(row[3])
#             #     d = int(row[5])
#             #     c = class_list[d]

#             #     if 'Coconutss' in c:
#             #         list.append([x1, y1, x2, y2])

#             # # Update tracker with detected objects
#             # bbox_id = tracker.update(list)
#             # for bbox in bbox_id:
#             #     x3, y3, x4, y4, id = bbox
#             #     cx = int(x3 + x4) // 2
#             #     cy = int(y3 + y4) // 2

#             #     x1, y1 = cx - 40 // 2, cy - 40 // 2
#             #     x2, y2 = cx + 40 // 2, cy + 40 // 2

#             #     # Drawing bounding boxes and lines
#             #     cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             #     cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
#             #     cv2.putText(frame, str(id), (cx, cy), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 255), 1)
#             #     cv2.line(frame, (220, cy1), (1050, cy1), (255, 255, 255), 1)

#             #     if cy < (cy1 + offset) and cy > (cy1 - offset):
#             #         for value in idlist[cam_id]:
#             #             if value == id:
#             #                 i = 1
#             #                 break
#             #             else:
#             #                 i = 0
#             #         idlist[cam_id].append(id)   
                        

#             #         if i != 1:
                           
                            

#             #             if cam_id == 1:
#             #                     # if cam_id == 1:
#             #                 counter[1] += 1
#             #                 counter1 += 1

#             #             elif cam_id == 2:
#             #                 print("camid =2")
#             #                 counter[2] += 1
#             #                 log_camera2_count()
                            
#             #                 if counter[2]>= reset_limit:
#             #                     store_coconut_count(counter[2])
#             #                     counter[2] =0
#             #             cv2.line(frame, (220, cy1), (1050, cy1), (0, 127, 255), 6)
                            
#             #             i = 1
                                
                         


#             # start_point = (800, 0)
#             # end_point = (1280, 150)
#             # color = (255, 255, 255)
#             # thickness = -1

#             # if cam_id == 1:
#             #     cv2.rectangle(frame, start_point, end_point, color, thickness)
#             #     cv2.putText(frame, f"Coconut counter: {counter[1]}", (810, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
#             #     cv2.putText(frame, f"Totalizer count: {total_counters[1]}", (810, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
#             # elif cam_id == 2:
#             #     cv2.rectangle(frame, start_point, end_point, color, thickness)
#             #     cv2.putText(frame, f"Reset counter: {counter[2]}", (810, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
#             #     cv2.putText(frame, f"Totalizer count: {total_counters[2]}", (810, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

#             # schedule.run_pending()

#         cv2.destroyAllWindows()

#         ret, jpeg = cv2.imencode('.jpg', frame)
#         if not ret:
#             continue

#         frame_bytes = jpeg.tobytes()
#         yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

#     cap.release()
            
# def process_ip_camera():
    
#     return run(IP, cam_id=1)

# # def process_web_camera():
# #     return run (IP, cam_id=2)


