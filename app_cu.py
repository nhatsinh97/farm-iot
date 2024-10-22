import cv2
import requests
import base64
import time
import os
import ast
import json
import sqlite3
import logging
import subprocess
import data_processor
# import datetime
from config import Config
from application.controllers.main_controller import main
from file_config import *
# from logging import Formatter, FileHandler, StreamHandler
# from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from logging import Formatter, StreamHandler
from logging.handlers import TimedRotatingFileHandler
from threading import Thread
import threading
from flask import Flask, send_file, render_template, request, Response

# Tạo logger
logger = logging.getLogger('cico_log')
logger.setLevel(logging.DEBUG)

# Định dạng log
formatter = Formatter('%(asctime)s - %(levelname)s - [in %(pathname)s:%(lineno)d] %(message)s')

# Stream handler (console)
stream_handler = StreamHandler()
stream_handler.setLevel(logging.CRITICAL)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# File handler (log file, split at midnight everyday)
file_handler = TimedRotatingFileHandler('./database/log/log_cico_everyday.log', when="midnight", interval=1)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

# Đảm bảo không có nhiều file handlers
for handler in logger.handlers:
    if isinstance(handler, TimedRotatingFileHandler):
        logger.removeHandler(handler)

# Thêm lại file handler duy nhất
logger.addHandler(file_handler)


logger.info("Start: GF-CICO")

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(main)
def ping_ip(ip):
    """
    Ping một địa chỉ IP và trả về kết quả.
    
    Args:
        ip (str): Địa chỉ IP cần ping.
        
    Returns:
        bool: True nếu ping thành công, False nếu thất bại.
    """
    try:
        # Thực hiện lệnh ping và kiểm tra kết quả
        output = subprocess.check_output(["ping", "-c", "1", ip], stderr=subprocess.STDOUT, universal_newlines=True)
        logger.critical(f"{ip} is Online.")
        return True
    except subprocess.CalledProcessError:
        logger.critical(f"{ip} is Offline.")
        return False
def monitor_ips(ip_addresses, interval):
    while True:
        for ip in ip_addresses:
            ping_ip(ip)
        # Đợi khoảng thời gian đã định trước khi kiểm tra lại
        time.sleep(interval)
# Trang chính web
@app.route("/")
def home():
    log_file_path = './database/log/log_cico_everyday.log'
    return send_file(log_file_path,as_attachment=False)
@app.route("/trangchinh")
def trangchinh():
    # Kiểm tra tiêu đề X-Forwarded-For để lấy địa chỉ IP thực sự của client
    # addr_ip4 = request.remote_addr
    addr_ip4 = request.headers.get('X-Forwarded-For', request.remote_addr)
    logger.critical("\n %s: đã đăng nhập vào web",addr_ip4)
    seo = {'title': 'Farm Bình Thuận || Quản lý công việc'}
    return render_template('index.html', seo=seo)

def generate_time():
    while True:
        current_time = time.strftime('%H : %M : %S')
        yield f'data: {current_time}\n\n'
        time.sleep(1)
@app.route('/update')
def update():
    return Response(generate_time(), content_type='text/event-stream')
@app.route("/home", methods = ['POST'])
def admin():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 'admin':
        return render_template("home.html")
    return 'failed'
@app.route("/index")
def index():
    return render_template("index.html")
@app.route("/index1")
def index1():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 'admin':
        return render_template("index1.html")
    return 'failed'
    # return render_template("index1.html")
@app.route("/index2")
def index2():
    return render_template("index2.html")
@app.route("/iot")
def iot():
    return render_template("iot.html")
@app.route("/login", methods = ['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 'admin':
        return render_template("home.html")
    return 'failed'
    
# API xử lý request từ thiết bị IOT ######################################################################




#######################################################

@app.route('/api', methods = ['POST'])
def iot_request():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = ast.literal_eval(request.data.decode())
    # logger.critical(data)
    with open('./database/json/total_data.json', 'w', encoding='utf-8') as out_file:
        json.dump(data, out_file, ensure_ascii=False, indent = 4)
    id = (data["id"])
    ip = (data["ip"])
    check = (data["check"])
    cam_1 = (data["cam_1"])
    cam_2 = (data["cam_2"])
    cam_3 = (data["cam_3"])
    cam_4 = (data["cam_4"])
    data_timer_1 = (data["data_timer_1"])
    data_timer_2 = (data["data_timer_2"])
    data_timer_3 = (data["data_timer_3"])
    data_timer_4 = (data["data_timer_4"])
    LOG_1 = (data["LOG_1"])
    LOG_2 = (data["LOG_2"])
    LOG_3 = (data["LOG_3"])
    LOG_4 = (data["LOG_4"])
    

######################### Nếu thiết bị mới khởi động lại thì gửi data từ server về thiết bị
    if check == "1":
        with open("./database/json/"+ id + ".json", "r", encoding='utf-8') as fin:
            check = json.load(fin)
        LOG_1 = (check[id]["LOG_1"])
        LOG_2 = (check[id]["LOG_2"])
        LOG_3 = (check[id]["LOG_3"])
        LOG_4 = (check[id]["LOG_4"])
        reset = (check[id]["reset"])
        with open("./database/json/data_"+ id + ".json", "r", encoding='utf-8') as fin:
            data = json.load(fin)
        cam_1 = (data["cam_1"])
        cam_2 = (data["cam_2"])
        cam_3 = (data["cam_3"])
        cam_4 = (data["cam_4"])
        data_timer_1 = (data["data_timer_1"])
        data_timer_2 = (data["data_timer_2"])
        data_timer_3 = (data["data_timer_3"])
        data_timer_4 = (data["data_timer_4"])
        out = [{"reset":reset,
                "cam_1":cam_1,
                "cam_2":cam_2,
                "cam_3":cam_3,
                "cam_4":cam_4,
                "data_timer_1":data_timer_1,
                "data_timer_2":data_timer_2,
                "data_timer_3":data_timer_3,
                "data_timer_4":data_timer_4,
                "LOG_1":LOG_1,
                "LOG_2":LOG_2,
                "LOG_3":LOG_3,
                "LOG_4":LOG_4
                }]
        logger.critical("\n  Check: ID=%s, IP=%s \n %s",id,ip,out)
        return (out)
    ##################### end ##############################
    with open("./database/json/"+ id + ".json", "r", encoding='utf-8') as fin:
        check = json.load(fin)
    stt1 = (check[id]["LOG_1"])
    stt2 = (check[id]["LOG_2"])
    stt3 = (check[id]["LOG_3"])
    stt4 = (check[id]["LOG_4"])
    reset = (check[id]["reset"])
    if reset == 1:
        data = { id:{ "ip" : ip , "reset":0 ,"LOG_1":LOG_1,"LOG_2": LOG_2,"LOG_3":LOG_3,"LOG_4":LOG_4}}
        with open('./database/json/' + id + '.json', 'w', encoding='utf-8') as out_file:
            json.dump(data, out_file, ensure_ascii=False, indent = 4)
        out = [{"reset":reset,"LOG_1":LOG_1,"LOG_2":LOG_2,"LOG_3":LOG_3,"LOG_4":LOG_4}]
        return (out)

    

    ################################################################################





    if LOG_1 == "start" :
        if stt1 == "end":
            # current_time = datetime.datetime.now()
            logger.info("\n Start: \n  ID trại   : %s \n  IP        : %s \n DATA: \n  UV 1: Timer: %s, hiện tại: %s ==> %s \n  UV 2: Timer: %s, hiện tại: %s ==> %s \n  UV 3: Timer: %s, hiện tại: %s ==> %s \n  UV 4: Timer: %s, hiện tại: %s ==> %s ", 
                        id,ip,data_timer_1,stt1,LOG_1,data_timer_2,stt2,LOG_2,data_timer_3,stt3,LOG_3,data_timer_4,stt4,LOG_4)
            thread = Thread(target=on_1)
            thread.start()
    if LOG_1 == "end" :
        if stt1 == "start":
            logger.info("\n End  : \n  ID trại   : %s \n  IP        : %s \n DATA: \n  UV 1: Timer: %s, hiện tại: %s ==> %s \n  UV 2: Timer: %s, hiện tại: %s ==> %s \n  UV 3: Timer: %s, hiện tại: %s ==> %s \n  UV 4: Timer: %s, hiện tại: %s ==> %s ", 
                        id,ip,data_timer_1,stt1,LOG_1,data_timer_2,stt2,LOG_2,data_timer_3,stt3,LOG_3,data_timer_4,stt4,LOG_4)
            thread = Thread(target=off_1)
            thread.start()
    if LOG_2 == "start" :
        if stt2 == "end":
            logger.info("\n Start: \n  ID trại   : %s \n  IP        : %s \n DATA: \n  UV 1: Timer: %s, hiện tại: %s ==> %s \n  UV 2: Timer: %s, hiện tại: %s ==> %s \n  UV 3: Timer: %s, hiện tại: %s ==> %s \n  UV 4: Timer: %s, hiện tại: %s ==> %s ", 
                        id,ip,data_timer_1,stt1,LOG_1,data_timer_2,stt2,LOG_2,data_timer_3,stt3,LOG_3,data_timer_4,stt4,LOG_4)
            thread = Thread(target=on_2)
            thread.start()
    if LOG_2 == "end" :
        if stt2 == "start":
            logger.info("\n End  : \n  ID trại   : %s \n  IP        : %s \n DATA: \n  UV 1: Timer: %s, hiện tại: %s ==> %s \n  UV 2: Timer: %s, hiện tại: %s ==> %s \n  UV 3: Timer: %s, hiện tại: %s ==> %s \n  UV 4: Timer: %s, hiện tại: %s ==> %s ", 
                        id,ip,data_timer_1,stt1,LOG_1,data_timer_2,stt2,LOG_2,data_timer_3,stt3,LOG_3,data_timer_4,stt4,LOG_4)
            thread = Thread(target=off_2)
            thread.start()
    if LOG_3 == "start" :
        if stt3 == "end":
            logger.info("\n Start: \n  ID trại   : %s \n  IP        : %s \n DATA: \n  UV 1: Timer: %s, hiện tại: %s ==> %s \n  UV 2: Timer: %s, hiện tại: %s ==> %s \n  UV 3: Timer: %s, hiện tại: %s ==> %s \n  UV 4: Timer: %s, hiện tại: %s ==> %s ", 
                        id,ip,data_timer_1,stt1,LOG_1,data_timer_2,stt2,LOG_2,data_timer_3,stt3,LOG_3,data_timer_4,stt4,LOG_4)
            thread = Thread(target=on_3)
            thread.start()
    if LOG_3 == "end" :
        if stt3 == "start":
            logger.info("\n End  : \n  ID trại   : %s \n  IP        : %s \n DATA: \n  UV 1: Timer: %s, hiện tại: %s ==> %s \n  UV 2: Timer: %s, hiện tại: %s ==> %s \n  UV 3: Timer: %s, hiện tại: %s ==> %s \n  UV 4: Timer: %s, hiện tại: %s ==> %s ", 
                        id,ip,data_timer_1,stt1,LOG_1,data_timer_2,stt2,LOG_2,data_timer_3,stt3,LOG_3,data_timer_4,stt4,LOG_4)
            thread = Thread(target=off_3)
            thread.start()
    if LOG_4 == "start" :
        if stt4 == "end":
            logger.info("\n Start: \n  ID trại   : %s \n  IP        : %s \n DATA: \n  UV 1: Timer: %s, hiện tại: %s ==> %s \n  UV 2: Timer: %s, hiện tại: %s ==> %s \n  UV 3: Timer: %s, hiện tại: %s ==> %s \n  UV 4: Timer: %s, hiện tại: %s ==> %s ", 
                        id,ip,data_timer_1,stt1,LOG_1,data_timer_2,stt2,LOG_2,data_timer_3,stt3,LOG_3,data_timer_4,stt4,LOG_4)
            thread = Thread(target=on_4)
            thread.start()
    if LOG_4 == "end" :
        if stt4 == "start":
            logger.info("\n End  : \n  ID trại   : %s \n  IP        : %s \n DATA: \n  UV 1: Timer: %s, hiện tại: %s ==> %s \n  UV 2: Timer: %s, hiện tại: %s ==> %s \n  UV 3: Timer: %s, hiện tại: %s ==> %s \n  UV 4: Timer: %s, hiện tại: %s ==> %s ", 
                        id,ip,data_timer_1,stt1,LOG_1,data_timer_2,stt2,LOG_2,data_timer_3,stt3,LOG_3,data_timer_4,stt4,LOG_4)
            thread = Thread(target=off_4)
            thread.start()
    out = {"reset":reset,"LOG_1":LOG_1,"LOG_2":LOG_2,"LOG_3":LOG_3,"LOG_4":LOG_4}
    # print(out)
    return out
if __name__ == '__main__':
    try:
        # Danh sách các địa chỉ IP cần kiểm tra
        ip_addresses = ["10.16.40.52", "10.16.40.32"]  # Thay thế bằng các địa chỉ IP của bạn
        interval = 3600  # Khoảng thời gian giữa các lần kiểm tra (giây)

        # Tạo và khởi động thread để giám sát các địa chỉ IP
        monitor_thread = threading.Thread(target=monitor_ips, args=(ip_addresses, interval))
        monitor_thread.daemon = True  # Đặt thread là daemon để nó tự động dừng khi chương trình chính dừng
        monitor_thread.start()
        # Chạy ứng dụng Flask
        app.run(host='0.0.0.0', port=58888, debug=Config.DEBUG)
        # app.run(host='0.0.0.0', port=58888, debug=True)
    # app.run(host='0.0.0.0', port=58888 ,debug=True)
    except Exception as e:
        # Ghi mã lỗi vào logging
        logger.error("Đã xảy ra lỗi: \n %s", e)