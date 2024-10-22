import cv2
import requests
import logging
# import urllib3
import ssl
from urllib3.exceptions import *
import ast
import json
import base64
from logging import Formatter, FileHandler, StreamHandler
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
logger = logging.getLogger('cico_log')
logger.setLevel(logging.DEBUG)

# Tắt cảnh báo liên quan đến SSL
# http = urllib3.PoolManager()
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Khai báo các biến
# API lấy thông tin bộ thiết bị
server     = 'http://172.17.128.50:58185'
api        = 'http://172.17.128.50:58185/api/MasterData/getitembycode'
# API trả về thời gian còn lại
apitimer   = 'http://172.17.128.50:58185/api/Farm/getcountdownsecond'
# API chính
url        = 'http://172.17.128.50:58185/api/Farm/postbiohistory' 
url_cico   = 'https://172.17.128.50:58187/api/Farm/postbiohistory'

# Xử lý tín hiệu phòng UV1
def on_uv1():
    logger.info("Start: on_uv1()")
    # print('hàm uv1')
    with open('./database/json/total_data.json', "r", encoding='utf-8') as fin:
        data = json.load(fin)
    ID = (data["ID"])
    reset = (data["reset"])
    check = (data["check"])
    cam_1 = (data["cam_1"])
    cam_2 = (data["cam_2"])
    status_uv1 = (data["phonguv1"]["status_uv1"])
    status_uv2 = (data["phonguv2"]["status_uv2"])
    cb_cua1 = (data["phonguv1"]["cb_cua1"])
    cb_cua2 = (data["phonguv2"]["cb_cua2"])
    # print('dữ liệu ID = {}'. format(ID))
    r = requests.post(api, data =json.dumps({"item_code": ID,"item_type":"BIO_CAMERA", "ATT1":cam_1}), 
        headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
    data_uv1 = r.json()
    rtsp_1 = (data_uv1[0]["ATT2"])
    timer_uv1 = (data_uv1[0]["ATT3"])
    cap = cv2.VideoCapture(rtsp_1)
    retval, img = cap.read()
    if retval:
        strImg64 = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
    if not retval:
        with open('./database/json/abc.jpg', "rb") as f:
            strImg64 = base64.b64encode(f.read()).decode()
    # gui data
    


    r = requests.post(url, data=json.dumps({
        "mac_address": cam_1 ,
        "action_name": "start",
        "timer": timer_uv1,
        "img": strImg64
    }), headers={
        'Content-type': 'application/json', 'Accept': 'text/plain'})

    code = r.status_code
    logger.info("Data: status_code_ATSH")
    
    # end
    file = r.json()
    if code == 200:
        status_uv1 = "1" 
        with open("./database/json/"+ ID + ".json", "r", encoding='utf-8') as fin:
            check = json.load(fin)
        stt1 = (check[ID]["statusuv_1"])
        stt2 = (check[ID]["statusuv_2"])
        stt_cb1 = (check[ID]["cb_cua1"])
        stt_cb2 = (check[ID]["cb_cua2"])
        reset = (check[ID]["reset"])
        dataa = { ID:{ "reset":"False","statusuv_1":status_uv1,"statusuv_2": status_uv2,"cb_cua1":stt_cb1,"cb_cua2":stt_cb2}}
        with open('./database/json/' + ID + '.json', 'w', encoding='utf-8') as out_file:
            json.dump(dataa, out_file, ensure_ascii=False, indent = 4)
        out = {"reset":reset,"status_uv1":status_uv1,"status_uv2":status_uv2,"cb_cua1":cb_cua1,"cb_cua2":cb_cua2}
        logger.info("End: on_uv1(): DATA = {}",format(code))
        gui = {
        "mac_address": cam_1 ,
        "action_name": "start",
        "timer": timer_uv1,
        "img": strImg64
        }
        x = requests.post(url_cico, json = gui, verify=False)
        return (out)
def off_uv1():
    # print('hàm uv1')
    with open('./database/json/total_data.json', "r", encoding='utf-8') as fin:
        data = json.load(fin)
    ID = (data["ID"])
    reset = (data["reset"])
    check = (data["check"])
    cam_1 = (data["cam_1"])
    cam_2 = (data["cam_2"])
    status_uv1 = (data["phonguv1"]["status_uv1"])
    status_uv2 = (data["phonguv2"]["status_uv2"])
    cb_cua1 = (data["phonguv1"]["cb_cua1"])
    cb_cua2 = (data["phonguv2"]["cb_cua2"])
    # print('dữ liệu ID = {}'. format(ID))
    r = requests.post(api, data =json.dumps({"item_code": ID,"item_type":"BIO_CAMERA", "ATT1":cam_1}), 
        headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
    data_uv1 = r.json()
    rtsp_1 = (data_uv1[0]["ATT2"])
    timer_uv1 = (data_uv1[0]["ATT3"])
    cap = cv2.VideoCapture(rtsp_1)
    retval, img = cap.read()
    if retval:
        strImg64 = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
    if not retval:
        with open('./database/json/abc.jpg', "rb") as f:
            strImg64 = base64.b64encode(f.read()).decode()
    # gui
    



    r = requests.post(url, data=json.dumps({
        "mac_address": cam_1 ,
        "action_name": "end",
        "timer": timer_uv1,
        "img": strImg64
    }), headers={
        'Content-type': 'application/json', 'Accept': 'text/plain'})
    # end
    # 
    code = r.status_code
    file = r.json()
    if code == 200:
        status_uv1 = "0" 
        with open("./database/json/"+ ID + ".json", "r", encoding='utf-8') as fin:
            check = json.load(fin)
        stt1 = (check[ID]["statusuv_1"])
        stt2 = (check[ID]["statusuv_2"])
        stt_cb1 = (check[ID]["cb_cua1"])
        stt_cb2 = (check[ID]["cb_cua2"])
        reset = (check[ID]["reset"])
        dataa = { ID:{ "reset":"False","statusuv_1":status_uv1,"statusuv_2": status_uv2,"cb_cua1":stt_cb1,"cb_cua2":stt_cb2}}
        with open('./database/json/' + ID + '.json', 'w', encoding='utf-8') as out_file:
            json.dump(dataa, out_file, ensure_ascii=False, indent = 4)
        out = {"reset":reset,"status_uv1":status_uv1,"status_uv2":status_uv2,"cb_cua1":cb_cua1,"cb_cua2":cb_cua2}
        gui = {
        "mac_address": cam_1 ,
        "action_name": "end",
        "timer": timer_uv1,
        "img": strImg64
        }
        x = requests.post(url_cico, json = gui, verify=False)
        return (out)

    

# Xử lý tín hiệu phòng UV2
def on_uv2():
    # print("uv2 ok")
    with open('./database/json/total_data.json', "r", encoding='utf-8') as fin:
        data = json.load(fin)
    ID = (data["ID"])
    reset = (data["reset"])
    check = (data["check"])
    cam_1 = (data["cam_1"])
    cam_2 = (data["cam_2"])
    status_uv1 = (data["phonguv1"]["status_uv1"])
    status_uv2 = (data["phonguv2"]["status_uv2"])
    cb_cua1 = (data["phonguv1"]["cb_cua1"])
    cb_cua2 = (data["phonguv2"]["cb_cua2"])
    # print('dữ liệu ID = {}'. format(ID))
    r = requests.post(api, data =json.dumps({"item_code": ID,"item_type":"BIO_CAMERA", "ATT1":cam_2}), 
        headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
    data_uv2 = r.json()
    rtsp_2 = (data_uv2[0]["ATT2"])
    timer_uv2 = (data_uv2[0]["ATT3"])
    cap = cv2.VideoCapture(rtsp_2)
    retval, img = cap.read()
    if retval:
        strImg64 = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
    if not retval:
        with open('./database/json/abc.jpg', "rb") as f:
            strImg64 = base64.b64encode(f.read()).decode()

    

    r = requests.post(url, data=json.dumps({
        "mac_address": cam_2 ,
        "action_name": "start",
        "timer": timer_uv2,
        "img": strImg64
    }), headers={
        'Content-type': 'application/json', 'Accept': 'text/plain'})
    code = r.status_code
    file = r.json()
    if code == 200:
        status_uv2 = "1" 
        with open("./database/json/"+ ID + ".json", "r", encoding='utf-8') as fin:
            check = json.load(fin)
        stt1 = (check[ID]["statusuv_1"])
        stt2 = (check[ID]["statusuv_2"])
        stt_cb1 = (check[ID]["cb_cua1"])
        stt_cb2 = (check[ID]["cb_cua2"])
        reset = (check[ID]["reset"])
        dataa = { ID:{ "reset":"False","statusuv_1":status_uv1,"statusuv_2": status_uv2,"cb_cua1":stt_cb1,"cb_cua2":stt_cb2}}
        with open('./database/json/' + ID + '.json', 'w', encoding='utf-8') as out_file:
            json.dump(dataa, out_file, ensure_ascii=False, indent = 4)
        out = {"reset":reset,"status_uv1":status_uv1,"status_uv2":status_uv2,"cb_cua1":cb_cua1,"cb_cua2":cb_cua2}
        gui = {
        "mac_address": cam_2 ,
        "action_name": "start",
        "timer": timer_uv2,
        "img": strImg64
        }
        x = requests.post(url_cico, json = gui, verify=False)
        return (out)

def off_uv2():
    # print("uv2 ok")
    with open('./database/json/total_data.json', "r", encoding='utf-8') as fin:
        data = json.load(fin)
    ID = (data["ID"])
    reset = (data["reset"])
    check = (data["check"])
    cam_1 = (data["cam_1"])
    cam_2 = (data["cam_2"])
    status_uv1 = (data["phonguv1"]["status_uv1"])
    status_uv2 = (data["phonguv2"]["status_uv2"])
    cb_cua1 = (data["phonguv1"]["cb_cua1"])
    cb_cua2 = (data["phonguv2"]["cb_cua2"])
    # print('dữ liệu ID = {}'. format(ID))
    r = requests.post(api, data =json.dumps({"item_code": ID,"item_type":"BIO_CAMERA", "ATT1":cam_2}), 
        headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
    data_uv2 = r.json()
    rtsp_2 = (data_uv2[0]["ATT2"])
    timer_uv2 = (data_uv2[0]["ATT3"])
    cap = cv2.VideoCapture(rtsp_2)
    retval, img = cap.read()
    if retval:
        strImg64 = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
    if not retval:
        with open('./database/json/abc.jpg', "rb") as f:
            strImg64 = base64.b64encode(f.read()).decode()
    
    

    r = requests.post(url, data=json.dumps({
        "mac_address": cam_2 ,
        "action_name": "end",
        "timer": timer_uv2,
        "img": strImg64
    }), headers={
        'Content-type': 'application/json', 'Accept': 'text/plain'})
    code = r.status_code
    file = r.json()
    if code == 200:
        status_uv2 = "0" 
        with open("./database/json/"+ ID + ".json", "r", encoding='utf-8') as fin:
            check = json.load(fin)
        stt1 = (check[ID]["statusuv_1"])
        stt2 = (check[ID]["statusuv_2"])
        stt_cb1 = (check[ID]["cb_cua1"])
        stt_cb2 = (check[ID]["cb_cua2"])
        reset = (check[ID]["reset"])
        dataa = { ID:{ "reset":"False","statusuv_1":status_uv1,"statusuv_2": status_uv2,"cb_cua1":stt_cb1,"cb_cua2":stt_cb2}}
        with open('./database/json/' + ID + '.json', 'w', encoding='utf-8') as out_file:
            json.dump(dataa, out_file, ensure_ascii=False, indent = 4)
        out = {"reset":reset,"status_uv1":status_uv1,"status_uv2":status_uv2,"cb_cua1":cb_cua1,"cb_cua2":cb_cua2}
        gui = {
        "mac_address": cam_2 ,
        "action_name": "end",
        "timer": timer_uv2,
        "img": strImg64
        }
        x = requests.post(url_cico, json = gui, verify=False)
        return (out)
    
# Gửi thông báo khi cửa phòng UV1 được mở
def phong_1():
    with open('./database/json/total_data.json', "r", encoding='utf-8') as fin:
        data = json.load(fin)
    ID = (data["ID"])
    reset = (data["reset"])
    check = (data["check"])
    cam_1 = (data["cam_1"])
    cam_2 = (data["cam_2"])
    status_uv1 = (data["phonguv1"]["status_uv1"])
    status_uv2 = (data["phonguv2"]["status_uv2"])
    cb_cua1 = (data["phonguv1"]["cb_cua1"])
    cb_cua2 = (data["phonguv2"]["cb_cua2"])
    r = requests.post(api, data =json.dumps({"item_code": ID,"item_type":"BIO_CAMERA", "ATT1":cam_1}), 
        headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
    data_uv1 = r.json()
    rtsp_1 = (data_uv1[0]["ATT2"])
    cap = cv2.VideoCapture(rtsp_1)
    retval, img = cap.read()
    if retval:
        strImg64 = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
    if not retval:
        with open('./database/json/abc.jpg', "rb") as f:
            strImg64 = base64.b64encode(f.read()).decode()
    r = requests.post(url, data=json.dumps({
        "mac_address": cam_1 ,
        "action_name": "RECEIVE",
        "timer": "",
        "img": strImg64
    }), headers={
        'Content-type': 'application/json', 'Accept': 'text/plain'})
    code = r.status_code
    file = r.json()
    if code == 200:
        stt_cb1 = "0"
        with open("./database/json/"+ ID + ".json", "r", encoding='utf-8') as fin:
            check = json.load(fin)
        stt1 = (check[ID]["statusuv_1"])
        stt2 = (check[ID]["statusuv_2"])
        stt_cb1 = (check[ID]["cb_cua1"])
        stt_cb2 = (check[ID]["cb_cua2"])
        reset = (check[ID]["reset"])
        dataa = { ID:{ "reset": reset,"statusuv_1":status_uv1,"statusuv_2": status_uv2,"cb_cua1":stt_cb1,"cb_cua2":stt_cb2}}
        with open('./database/json/' + ID + '.json', 'w', encoding='utf-8') as out_file:
            json.dump(dataa, out_file, ensure_ascii=False, indent = 4)
        out = [{"reset":reset,"status_uv1":status_uv1,"status_uv2":status_uv2,"cb_cua1":cb_cua1,"cb_cua2":cb_cua2}]
        return (out)
# Gửi thông báo khi cửa phòng UV2 được mở
def phong_2():
    with open('./database/json/total_data.json', "r", encoding='utf-8') as fin:
        data = json.load(fin)
    ID = (data["ID"])
    reset = (data["reset"])
    check = (data["check"])
    cam_1 = (data["cam_1"])
    cam_2 = (data["cam_2"])
    status_uv1 = (data["phonguv1"]["status_uv1"])
    status_uv2 = (data["phonguv2"]["status_uv2"])
    cb_cua1 = (data["phonguv1"]["cb_cua1"])
    cb_cua2 = (data["phonguv2"]["cb_cua2"])
    r = requests.post(api, data =json.dumps({"item_code": ID,"item_type":"BIO_CAMERA", "ATT1":cam_2}), 
        headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
    data_uv2 = r.json()
    rtsp_2 = (data_uv2[0]["ATT2"])
    cap = cv2.VideoCapture(rtsp_2)
    retval, img = cap.read()
    if retval:
        strImg64 = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
    if not retval:
        with open('./database/json/abc.jpg', "rb") as f:
            strImg64 = base64.b64encode(f.read()).decode()
    r = requests.post(url, data=json.dumps({
        "mac_address": cam_2 ,
        "action_name": "RECEIVE",
        "timer": "",
        "img": strImg64
    }), headers={
        'Content-type': 'application/json', 'Accept': 'text/plain'})
    code = r.status_code
    file = r.json()
    if code == 200:
        stt_cb2 = "0"
        with open("./database/json/"+ ID + ".json", "r", encoding='utf-8') as fin:
            check = json.load(fin)
        stt1 = (check[ID]["statusuv_1"])
        stt2 = (check[ID]["statusuv_2"])
        stt_cb1 = (check[ID]["cb_cua1"])
        stt_cb2 = (check[ID]["cb_cua2"])
        reset = (check[ID]["reset"])
        dataa = { ID:{ "reset": reset,"statusuv_1":status_uv1,"statusuv_2": status_uv2,"cb_cua1":stt_cb1,"cb_cua2":stt_cb2}}
        with open('./database/json/' + ID + '.json', 'w', encoding='utf-8') as out_file:
            json.dump(dataa, out_file, ensure_ascii=False, indent = 4)
        out = [{"reset":reset,"status_uv1":status_uv1,"status_uv2":status_uv2,"cb_cua1":cb_cua1,"cb_cua2":cb_cua2}]
        return (out)
# Phát hiện con người phòng UV2
def human_uv1():
    with open('./database/json/total_data.json', "r", encoding='utf-8') as fin:
        data = json.load(fin)
    ID = (data["ID"])
    reset = (data["reset"])
    check = (data["check"])
    cam_1 = (data["cam_1"])
    cam_2 = (data["cam_2"])
    status_uv1 = (data["phonguv1"]["status_uv1"])
    status_uv2 = (data["phonguv2"]["status_uv2"])
    cb_cua1 = (data["phonguv1"]["cb_cua1"])
    cb_cua2 = (data["phonguv2"]["cb_cua2"])
    r = requests.post(api, data =json.dumps({"item_code": ID,"item_type":"BIO_CAMERA", "ATT1":cam_1}), 
        headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
    data_uv1 = r.json()
    rtsp_1 = (data_uv1[0]["ATT2"])
    cap = cv2.VideoCapture(rtsp_1)
    retval, img = cap.read()
    if retval:
        strImg64 = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
    if not retval:
        with open('./database/json/abc.jpg', "rb") as f:
            strImg64 = base64.b64encode(f.read()).decode()
    r = requests.post(url, data=json.dumps({
        "mac_address": cam_1 ,
        "action_name": "HUMAN_DETECT",
        "timer": "",
        "img": strImg64
    }), headers={
        'Content-type': 'application/json', 'Accept': 'text/plain'})
    code = r.status_code
    file = r.json()
    return
    # if code == 200:
    #     stt_cb2 = "0"
    #     with open("./database/json/"+ ID + ".json", "r", encoding='utf-8') as fin:
    #         check = json.load(fin)
    #     stt1 = (check[ID]["statusuv_1"])
    #     stt2 = (check[ID]["statusuv_2"])
    #     stt_cb1 = (check[ID]["cb_cua1"])
    #     stt_cb2 = (check[ID]["cb_cua2"])
    #     reset = (check[ID]["reset"])
    #     dataa = { ID:{ "reset": reset,"statusuv_1":status_uv1,"statusuv_2": status_uv2,"cb_cua1":stt_cb1,"cb_cua2":stt_cb2}}
    #     with open('./database/json/' + ID + '.json', 'w', encoding='utf-8') as out_file:
    #         json.dump(dataa, out_file, ensure_ascii=False, indent = 4)
    #     out = [{"reset":reset,"status_uv1":status_uv1,"status_uv2":status_uv2,"cb_cua1":cb_cua1,"cb_cua2":cb_cua2}]
    #     return (out)

def human_uv2():
    with open('./database/json/total_data.json', "r", encoding='utf-8') as fin:
        data = json.load(fin)
    ID = (data["ID"])
    reset = (data["reset"])
    check = (data["check"])
    cam_1 = (data["cam_1"])
    cam_2 = (data["cam_2"])
    status_uv1 = (data["phonguv1"]["status_uv1"])
    status_uv2 = (data["phonguv2"]["status_uv2"])
    cb_cua1 = (data["phonguv1"]["cb_cua1"])
    cb_cua2 = (data["phonguv2"]["cb_cua2"])
    r = requests.post(api, data =json.dumps({"item_code": ID,"item_type":"BIO_CAMERA", "ATT1":cam_2}), 
        headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
    data_uv2 = r.json()
    rtsp_2 = (data_uv2[0]["ATT2"])
    cap = cv2.VideoCapture(rtsp_2)
    retval, img = cap.read()
    if retval:
        strImg64 = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
    if not retval:
        with open('./database/json/abc.jpg', "rb") as f:
            strImg64 = base64.b64encode(f.read()).decode()
    r = requests.post(url, data=json.dumps({
        "mac_address": cam_2 ,
        "action_name": "HUMAN_DETECT",
        "timer": "",
        "img": strImg64
    }), headers={
        'Content-type': 'application/json', 'Accept': 'text/plain'})
    code = r.status_code
    file = r.json()
    return