import cv2
import requests
import base64
import time
import os
import ast
import json
import sqlite3
import logging
from file_config3 import *
from logging import Formatter, FileHandler, StreamHandler
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from threading import Thread
from flask import Flask, render_template, request, Response
logger = logging.getLogger('cico_log')
logger.setLevel(logging.DEBUG)
formatter = Formatter('%(asctime)s - %(levelname)s - [in %(pathname)s:%(lineno)d] %(message)s')

# Stream handles
stream_handler = StreamHandler()
stream_handler.setLevel(logging.CRITICAL)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# Split log at 0h everyday
file_handler = TimedRotatingFileHandler('./database/log/log_cico_everyday.log', when="midnight", interval=1)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)



logger.info("Start: GF-CICO")

app = Flask(__name__)
# Trang chính web
@app.route("/")
def home():
    with open("./database/json/server.json", "r", encoding='utf-8') as fin:
        # Chuyển chuỗi JSON thành đối tượng Python
        data_object = json.load(fin)
    return render_template('index.html', data_object = data_object)
    # return render_template("index.html")
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
    
# API xử lý request từ thiết bị IOT

@app.route('/api', methods = ['POST'])
def iot_request():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = ast.literal_eval(request.data.decode())
    logger.critical(data)
    with open('./database/json/total_data.json', 'w', encoding='utf-8') as out_file:
        json.dump(data, out_file, ensure_ascii=False, indent = 4)
    ID = (data["ID"])
    reset = (data["reset"])
    check = (data["check"])
    cam_1 = (data["cam_1"])
    cam_2 = (data["cam_2"])
    status_uv1 = (data["phonguv1"]["status_uv1"])
    status_uv2 = (data["phonguv2"]["status_uv2"])
    cb_cua1 = (data["phonguv1"]["cb_cua1"])
    cb_cua2 = (data["phonguv2"]["cb_cua2"])
    if check == "True":
        with open("./database/json/"+ ID + ".json", "r", encoding='utf-8') as fin:
            check = json.load(fin)
        stt1 = (check[ID]["statusuv_1"])
        stt2 = (check[ID]["statusuv_2"])
        stt_cb1 = (check[ID]["cb_cua1"])
        stt_cb2 = (check[ID]["cb_cua2"])
        reset = (check[ID]["reset"])
        out = [{"reset":reset,"status_uv1":stt1,"status_uv2":stt2,"cb_cua1":stt_cb1,"cb_cua2":stt_cb2}]
        return (out)
    with open("./database/json/"+ ID + ".json", "r", encoding='utf-8') as fin:
        check = json.load(fin)
    stt1 = (check[ID]["statusuv_1"])
    stt2 = (check[ID]["statusuv_2"])
    stt_cb1 = (check[ID]["cb_cua1"])
    stt_cb2 = (check[ID]["cb_cua2"])
    reset = (check[ID]["reset"])

    if reset == "True":
        dataa = { ID:{ "reset":"False","statusuv_1":status_uv1,"statusuv_2": status_uv2,"cb_cua1":stt_cb1,"cb_cua2":stt_cb2}}
        with open('./database/json/' + ID + '.json', 'w', encoding='utf-8') as out_file:
            json.dump(dataa, out_file, ensure_ascii=False, indent = 4)
        out = [{"reset":reset,"status_uv1":status_uv1,"status_uv2":status_uv2,"cb_cua1":cb_cua1,"cb_cua2":cb_cua2}]
        return (out)






    if status_uv1 == "1" :
        if stt1 == "0":
            thread = Thread(target=on_uv1)
            thread.start()
    if status_uv1 == "0" :
        if stt1 == "1":
            thread = Thread(target=off_uv1)
            thread.start()
    if status_uv2 == "1" :
        if stt2 == "0":
            thread = Thread(target=on_uv2)
            thread.start()
    if status_uv2 == "0" :
        if stt2 == "1":
            thread = Thread(target=off_uv2)
            thread.start()
    # if cb_cua1 == "1" :
    #     if stt_cb1 == "0":
    #         thread = Thread(target=phong_1)
    #         thread.start()
    # if cb_cua2 == "1" :
    #     if stt_cb2 == "0":
    #         thread = Thread(target=phong_2)
    #         thread.start()
    out = {"reset":reset,"status_uv1":status_uv1,"status_uv2":status_uv2,"cb_cua1":cb_cua1,"cb_cua2":cb_cua2}
    # print(out)
    return out
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=58888 ,debug=True)