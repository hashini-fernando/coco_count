
from flask import Flask, render_template, Response, request, jsonify, send_file
import threading
import webview
import datetime
from main import process_ip_camera, process_web_camera
from data import Hour_data, Month_data, Day_data, Week_data, Hour_createcsv, Hour_createcsv_reset, Day_createcsv, Week_createcsv, Month_createcsv, Hour_data_reset, Day_data_reset, Day_createcsv_reset, Week_createcsv_reset, Month_createcsv_reset
import os

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('index.html')

@app.route('/video_feed_cam1')
def video_feed_cam1():
    return Response(process_ip_camera(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_cam2')
def video_feed_cam2():
    return Response(process_web_camera(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/trends', methods=['GET', 'POST'])
def trends():
    date_list = []
    count_list = []

    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        form_type = request.form.get('dateForm')  

        time1 = datetime.datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
        time2 = datetime.datetime.strptime(end_date, "%Y-%m-%dT%H:%M")

        # Fetch data from the database based on the data type
        data_type = request.form.get('data_type', 'hour')

        if form_type == 'Cam1':
            if data_type == 'hour':
                date_list, count_list = Hour_data(time1, time2)
            elif data_type == 'day':
                date_list, count_list = Day_data(time1, time2)
            elif data_type == 'week':
                date_list, count_list = Week_data(time1, time2)
            elif data_type == 'month':
                date_list, count_list = Month_data(time1, time2)
        if form_type == 'Cam2':
            if data_type == 'hour_reset':
                date_list,count_list = Hour_data_reset(time1,time2)
            elif data_type == 'day_reset':
                date_list,count_list = Day_data_reset(time1,time2)

    return render_template('trends.html', date_list=date_list, count_list=count_list)

@app.route('/get_trends', methods=['POST'])
def get_trends():
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    data_type = request.form.get('data_type')
    form_type = request.form.get('dateForm') 
    
    time1 = datetime.datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
    time2 = datetime.datetime.strptime(end_date, "%Y-%m-%dT%H:%M")

    if form_type == 'Cam1':
        if data_type == 'hour':
            date_list, count_list = Hour_data(time1, time2)
        elif data_type == 'day':
            date_list, count_list = Day_data(time1, time2)
        elif data_type == 'week':
            date_list, count_list = Week_data(time1, time2)
        elif data_type == 'month':
            date_list, count_list = Month_data(time1, time2)
    elif form_type == 'Cam2':
        if data_type == 'hour_reset':
            date_list,count_list = Hour_data_reset(time1,time2)
        elif data_type == 'day_reset':
            date_list,count_list = Day_data_reset(time1,time2)
        elif data_type == 'week_reset':
            date_list, count_list = Week_data(time1, time2)
        elif data_type == 'month_reset':
            date_list, count_list = Month_data(time1, time2)

    return jsonify(date_list=date_list, count_list=count_list)

@app.route('/reports', methods=['GET', 'POST'])
def reports():
    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        data_type = request.form.get('reportType')
        form_type = request.form.get('dateForm')

        time1 = datetime.datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
        time2 = datetime.datetime.strptime(end_date, "%Y-%m-%dT%H:%M")        

        if form_type == 'Cam1':
            if data_type == 'hour':
                file_path = Hour_createcsv(time1, time2)
            elif data_type == 'day':
                file_path = Day_createcsv(time1, time2)
            elif data_type == 'week':
                file_path = Week_createcsv(time1, time2)
            elif data_type == 'month':
                file_path = Month_createcsv(time1, time2)

        if form_type == 'Cam2':
            if data_type == 'hour_reset':
                file_path = Hour_createcsv_reset(time1,time2)
            elif data_type == 'day_reset':
                file_path = Day_createcsv_reset(time1,time2)
            elif data_type == 'week_reset':
                file_path = Week_createcsv_reset(time1,time2)
            elif data_type == 'month_reset':
                file_path = Month_createcsv_reset(time1,time2)

        return send_file(file_path, mimetype='text/csv', as_attachment=True)

    return render_template('reports.html')

def start_flask():
    app.run(host="127.0.0.1", port=5000)

def create_gui():
    webview.create_window('Coconut Counter', 'http://127.0.0.1:5000', width=800, height=600)
    webview.start()

def run_camera_feeds():
    # Thread for the IP camera
    thread_ip_camera = threading.Thread(target=process_ip_camera)
    thread_ip_camera.start()

    # Thread for the web camera
    thread_web_camera = threading.Thread(target=process_web_camera)
    thread_web_camera.start()

    # thread_ip_camera.join()
    # thread_web_camera.join()

if __name__ == "__main__":
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Run camera feeds and GUI in separate threads
    camera_thread = threading.Thread(target=run_camera_feeds)
    camera_thread.daemon = True
    camera_thread.start()
    
    create_gui()