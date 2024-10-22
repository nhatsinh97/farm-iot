import cv2
import requests
import logging
import datetime
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
def on_1():
    with open('./database/json/total_data.json', "r", encoding='utf-8') as fin:
        data = json.load(fin)
    id = (data["id"])
    ip = (data["ip"])
    check = (data["check"])
    cam_1 = (data["cam_1"])
    data_timer_1 = (data["data_timer_1"])
    data_timer_2 = (data["data_timer_2"])
    data_timer_3 = (data["data_timer_3"])
    data_timer_4 = (data["data_timer_4"])
    LOG_1 = (data["LOG_1"])
    cap = cv2.VideoCapture(cam_1)
    retval, img = cap.read()
    if retval:
        strImg64 = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
    if not retval:
        with open('./database/json/abc.jpg', "rb") as f:
            strImg64 = base64.b64encode(f.read()).decode()
    # Tạo data gửi server
    data = json.dumps({
        "mac_address": id +"_CAMERA1" ,
        "action_name": LOG_1,
        "timer": data_timer_1,
        "img": strImg64
    })
    # gui data
    r = requests.post(url, data, headers = {'Content-type': 'application/json', 'Accept': 'text/plain'})
    code = r.status_code
    logger.info("Mã trạng thái HTTP server 1: %s", code)
    # end
    file = r.json()
    if code == 200:
        with open("./database/json/"+ id + ".json", "r", encoding='utf-8') as fin:
            check = json.load(fin)
        # LOG_1 = (check[id]["LOG_1"])
        LOG_2 = (check[id]["LOG_2"])
        LOG_3 = (check[id]["LOG_3"])
        LOG_4 = (check[id]["LOG_4"])
        reset = (check[id]["reset"])
        data = { id:{ "reset":0, "ip":ip,"LOG_1":LOG_1,"LOG_2": LOG_2,"LOG_3":LOG_3,"LOG_4":LOG_4}}
        with open('./database/json/' + id + '.json', 'w', encoding='utf-8') as out_file:
            json.dump(data, out_file, ensure_ascii=False, indent = 4)
        out = {"reset":reset,"LOG_1":LOG_1,"LOG_2":LOG_2,"LOG_3":LOG_3,"LOG_4":LOG_4}
        x = requests.post(url_cico, data, headers = {'Content-type': 'application/json', 'Accept': 'text/plain'},verify=False)
        code = r.status_code
        logger.info("Mã trạng thái HTTP server 2: %s", code)
        return (out)
    
##############################################################################################




def off_1():
    with open('./database/json/total_data.json', "r", encoding='utf-8') as fin:
        data = json.load(fin)
    id = (data["id"])
    ip = (data["ip"])
    check = (data["check"])
    cam_1 = (data["cam_1"])
    data_timer_1 = (data["data_timer_1"])
    data_timer_2 = (data["data_timer_2"])
    data_timer_3 = (data["data_timer_3"])
    data_timer_4 = (data["data_timer_4"])
    LOG_1 = (data["LOG_1"])
    cap = cv2.VideoCapture(cam_1)
    retval, img = cap.read()
    if retval:
        strImg64 = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
    if not retval:
        with open('./database/json/abc.jpg', "rb") as f:
            strImg64 = base64.b64encode(f.read()).decode()
    # gui data
    r = requests.post(url, data=json.dumps({
        "mac_address": id +"_CAMERA1" ,
        "action_name": LOG_1,
        "timer": data_timer_1,
        "img": strImg64
    }), headers={
        'Content-type': 'application/json', 'Accept': 'text/plain'})
    code = r.status_code
    logger.info("\n Mã trạng thái HTTP server 1: %s", code)
    
    # end
    file = r.json()
    if code == 200:
        # if LOG_1 == "start":
        with open("./database/json/"+ id + ".json", "r", encoding='utf-8') as fin:
            check = json.load(fin)
        # LOG_1 = (check[id]["LOG_1"])
        LOG_2 = (check[id]["LOG_2"])
        LOG_3 = (check[id]["LOG_3"])
        LOG_4 = (check[id]["LOG_4"])
        reset = (check[id]["reset"])
        data = { id:{ "reset":0, "ip":ip,"LOG_1":LOG_1,"LOG_2": LOG_2,"LOG_3":LOG_3,"LOG_4":LOG_4}}
        with open('./database/json/' + id + '.json', 'w', encoding='utf-8') as out_file:
            json.dump(data, out_file, ensure_ascii=False, indent = 4)
        out = {"reset":reset,"LOG_1":LOG_1,"LOG_2":LOG_2,"LOG_3":LOG_3,"LOG_4":LOG_4}
        # logger.info("End: on_uv1(): DATA = {}",format(code))
        gui = {
        "mac_address": id +"_CAMERA1" ,
        "action_name": LOG_1,
        "timer": data_timer_1,
        "img": strImg64
        }
        x = requests.post(url_cico, json = gui, verify=False)
        return (out)

 ##########################################################################################################   

# Xử lý tín hiệu phòng UV2
def on_2():
    with open('./database/json/total_data.json', "r", encoding='utf-8') as fin:
        data = json.load(fin)
    id = (data["id"])
    ip = (data["ip"])
    check = (data["check"])
    cam_2 = (data["cam_2"])
    data_timer_1 = (data["data_timer_1"])
    data_timer_2 = (data["data_timer_2"])
    data_timer_3 = (data["data_timer_3"])
    data_timer_4 = (data["data_timer_4"])
    LOG_2 = (data["LOG_2"])
    cap = cv2.VideoCapture(cam_2)
    retval, img = cap.read()
    if retval:
        strImg64 = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
    if not retval:
        with open('./database/json/abc.jpg', "rb") as f:
            strImg64 = base64.b64encode(f.read()).decode()
    # gui data
    r = requests.post(url, data=json.dumps({
        "mac_address": id +"_CAMERA2" ,
        "action_name": LOG_2,
        "timer": data_timer_2,
        "img": strImg64
    }), headers={
        'Content-type': 'application/json', 'Accept': 'text/plain'})
    code = r.status_code
    logger.info("\n Mã trạng thái HTTP server 1: %s", code)
    
    # end
    file = r.json()
    if code == 200:
        # if LOG_1 == "start":
        with open("./database/json/"+ id + ".json", "r", encoding='utf-8') as fin:
            check = json.load(fin)
        LOG_1 = (check[id]["LOG_1"])
        # LOG_2 = (check[id]["LOG_2"])
        LOG_3 = (check[id]["LOG_3"])
        LOG_4 = (check[id]["LOG_4"])
        reset = (check[id]["reset"])
        data = { id:{ "reset":0, "ip":ip,"LOG_1":LOG_1,"LOG_2": LOG_2,"LOG_3":LOG_3,"LOG_4":LOG_4}}
        with open('./database/json/' + id + '.json', 'w', encoding='utf-8') as out_file:
            json.dump(data, out_file, ensure_ascii=False, indent = 4)
        out = {"reset":reset,"LOG_1":LOG_1,"LOG_2":LOG_2,"LOG_3":LOG_3,"LOG_4":LOG_4}
        # logger.info("End: on_uv1(): DATA = {}",format(code))
        gui = {
        "mac_address": id +"_CAMERA2" ,
        "action_name": LOG_1,
        "timer": data_timer_2,
        "img": strImg64
        }
        x = requests.post(url_cico, json = gui, verify=False)
        return (out)
    
##############################################################################################

def off_2():
    # print('hàm uv1')
    with open('./database/json/total_data.json', "r", encoding='utf-8') as fin:
        data = json.load(fin)
    id = (data["id"])
    ip = (data["ip"])
    check = (data["check"])
    cam_2 = (data["cam_2"])
    data_timer_1 = (data["data_timer_1"])
    data_timer_2 = (data["data_timer_2"])
    data_timer_3 = (data["data_timer_3"])
    data_timer_4 = (data["data_timer_4"])
    LOG_2 = (data["LOG_2"])
    cap = cv2.VideoCapture(cam_2)
    retval, img = cap.read()
    if retval:
        strImg64 = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
    if not retval:
        with open('./database/json/abc.jpg', "rb") as f:
            strImg64 = base64.b64encode(f.read()).decode()
    # gui data
    r = requests.post(url, data=json.dumps({
        "mac_address": id +"_CAMERA2" ,
        "action_name": LOG_2,
        "timer": data_timer_2,
        "img": strImg64
    }), headers={
        'Content-type': 'application/json', 'Accept': 'text/plain'})
    code = r.status_code
    logger.info("\n Mã trạng thái HTTP server 1: %s", code)
    
    # end
    file = r.json()
    if code == 200:
        # if LOG_1 == "start":
        with open("./database/json/"+ id + ".json", "r", encoding='utf-8') as fin:
            check = json.load(fin)
        LOG_1 = (check[id]["LOG_1"])
        # LOG_2 = (check[id]["LOG_2"])
        LOG_3 = (check[id]["LOG_3"])
        LOG_4 = (check[id]["LOG_4"])
        reset = (check[id]["reset"])
        data = { id:{ "reset":0, "ip":ip,"LOG_1":LOG_1,"LOG_2": LOG_2,"LOG_3":LOG_3,"LOG_4":LOG_4}}
        with open('./database/json/' + id + '.json', 'w', encoding='utf-8') as out_file:
            json.dump(data, out_file, ensure_ascii=False, indent = 4)
        out = {"reset":reset,"LOG_1":LOG_1,"LOG_2":LOG_2,"LOG_3":LOG_3,"LOG_4":LOG_4}
        # logger.info("End: on_uv1(): DATA = {}",format(code))
        gui = {
        "mac_address": id +"_CAMERA2" ,
        "action_name": LOG_2,
        "timer": data_timer_2,
        "img": strImg64
        }
        x = requests.post(url_cico, json = gui, verify=False)
        return (out)
# Gửi thông báo khi cửa phòng UV2 được mở
def on_3():
    # print('hàm uv1')
    with open('./database/json/total_data.json', "r", encoding='utf-8') as fin:
        data = json.load(fin)
    id = (data["id"])
    ip = (data["ip"])
    check = (data["check"])
    cam_3 = (data["cam_3"])
    data_timer_1 = (data["data_timer_1"])
    data_timer_2 = (data["data_timer_2"])
    data_timer_3 = (data["data_timer_3"])
    data_timer_4 = (data["data_timer_4"])
    LOG_3 = (data["LOG_3"])
    cap = cv2.VideoCapture(cam_3)
    retval, img = cap.read()
    if retval:
        strImg64 = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
    if not retval:
        with open('./database/json/abc.jpg', "rb") as f:
            strImg64 = base64.b64encode(f.read()).decode()
    # gui data
    r = requests.post(url, data=json.dumps({
        "mac_address": id +"_CAMERA3" ,
        "action_name": LOG_3,
        "timer": data_timer_3,
        "img": strImg64
    }), headers={
        'Content-type': 'application/json', 'Accept': 'text/plain'})
    code = r.status_code
    
    # end
    file = r.json()
    if code == 200:
        # if LOG_1 == "start":
        with open("./database/json/"+ id + ".json", "r", encoding='utf-8') as fin:
            check = json.load(fin)
        LOG_1 = (check[id]["LOG_1"])
        LOG_2 = (check[id]["LOG_2"])
        # LOG_3 = (check[id]["LOG_3"])
        LOG_4 = (check[id]["LOG_4"])
        reset = (check[id]["reset"])
        data = { id:{ "reset":0, "ip":ip,"LOG_1":LOG_1,"LOG_2": LOG_2,"LOG_3":LOG_3,"LOG_4":LOG_4}}
        with open('./database/json/' + id + '.json', 'w', encoding='utf-8') as out_file:
            json.dump(data, out_file, ensure_ascii=False, indent = 4)
        out = {"reset":reset,"LOG_1":LOG_1,"LOG_2":LOG_2,"LOG_3":LOG_3,"LOG_4":LOG_4}
        # logger.info("End: on_uv1(): DATA = {}",format(code))
        gui = {
        "mac_address": id +"_CAMERA3" ,
        "action_name": LOG_3,
        "timer": data_timer_3,
        "img": strImg64
        }
        x = requests.post(url_cico, json = gui, verify=False)
        return (out)
    
##############################################################################################




def off_3():
    # print('hàm uv1')
    with open('./database/json/total_data.json', "r", encoding='utf-8') as fin:
        data = json.load(fin)
    id = (data["id"])
    ip = (data["ip"])
    check = (data["check"])
    cam_3 = (data["cam_3"])
    data_timer_1 = (data["data_timer_1"])
    data_timer_2 = (data["data_timer_2"])
    data_timer_3 = (data["data_timer_3"])
    data_timer_4 = (data["data_timer_4"])
    LOG_3 = (data["LOG_3"])
    cap = cv2.VideoCapture(cam_3)
    retval, img = cap.read()
    if retval:
        strImg64 = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
    if not retval:
        with open('./database/json/abc.jpg', "rb") as f:
            strImg64 = base64.b64encode(f.read()).decode()
    # gui data
    r = requests.post(url, data=json.dumps({
        "mac_address": id +"_CAMERA3" ,
        "action_name": LOG_3,
        "timer": data_timer_3,
        "img": strImg64
    }), headers={
        'Content-type': 'application/json', 'Accept': 'text/plain'})
    code = r.status_code
    logger.info("\n Mã trạng thái HTTP server 1: %s", code)
    
    # end
    file = r.json()
    if code == 200:
        # if LOG_1 == "start":
        with open("./database/json/"+ id + ".json", "r", encoding='utf-8') as fin:
            check = json.load(fin)
        LOG_1 = (check[id]["LOG_1"])
        LOG_2 = (check[id]["LOG_2"])
        # LOG_3 = (check[id]["LOG_3"])
        LOG_4 = (check[id]["LOG_4"])
        reset = (check[id]["reset"])
        data = { id:{ "reset":0, "ip":ip,"LOG_1":LOG_1,"LOG_2": LOG_2,"LOG_3":LOG_3,"LOG_4":LOG_4}}
        with open('./database/json/' + id + '.json', 'w', encoding='utf-8') as out_file:
            json.dump(data, out_file, ensure_ascii=False, indent = 4)
        out = {"reset":reset,"LOG_1":LOG_1,"LOG_2":LOG_2,"LOG_3":LOG_3,"LOG_4":LOG_4}
        # logger.info("End: on_uv1(): DATA = {}",format(code))
        gui = {
        "mac_address": id +"_CAMERA3" ,
        "action_name": LOG_3,
        "timer": data_timer_3,
        "img": strImg64
        }
        x = requests.post(url_cico, json = gui, verify=False)
        return (out)
    
def on_4():
    # print('hàm uv1')
    with open('./database/json/total_data.json', "r", encoding='utf-8') as fin:
        data = json.load(fin)
    id = (data["id"])
    ip = (data["ip"])
    check = (data["check"])
    cam_4 = (data["cam_4"])
    data_timer_1 = (data["data_timer_1"])
    data_timer_2 = (data["data_timer_2"])
    data_timer_3 = (data["data_timer_3"])
    data_timer_4 = (data["data_timer_4"])
    LOG_4 = (data["LOG_4"])
    cap = cv2.VideoCapture(cam_4)
    retval, img = cap.read()
    if retval:
        strImg64 = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
    if not retval:
        with open('./database/json/abc.jpg', "rb") as f:
            strImg64 = base64.b64encode(f.read()).decode()
    # gui data
    r = requests.post(url, data=json.dumps({
        "mac_address": id +"_CAMERA4" ,
        "action_name": LOG_4,
        "timer": data_timer_4,
        "img": strImg64
    }), headers={
        'Content-type': 'application/json', 'Accept': 'text/plain'})
    code = r.status_code
    logger.info("\n Mã trạng thái HTTP server 1: %s", code)
    
    # end
    file = r.json()
    if code == 200:
        # if LOG_1 == "start":
        with open("./database/json/"+ id + ".json", "r", encoding='utf-8') as fin:
            check = json.load(fin)
        LOG_1 = (check[id]["LOG_1"])
        LOG_2 = (check[id]["LOG_2"])
        LOG_3 = (check[id]["LOG_3"])
        # LOG_4 = (check[id]["LOG_4"])
        reset = (check[id]["reset"])
        data = { id:{ "reset":0, "ip":ip,"LOG_1":LOG_1,"LOG_2": LOG_2,"LOG_3":LOG_3,"LOG_4":LOG_4}}
        with open('./database/json/' + id + '.json', 'w', encoding='utf-8') as out_file:
            json.dump(data, out_file, ensure_ascii=False, indent = 4)
        out = {"reset":reset,"LOG_1":LOG_1,"LOG_2":LOG_2,"LOG_3":LOG_3,"LOG_4":LOG_4}
        # logger.info("End: on_uv1(): DATA = {}",format(code))
        gui = {
        "mac_address": id +"_CAMERA4" ,
        "action_name": LOG_4,
        "timer": data_timer_4,
        "img": strImg64
        }
        x = requests.post(url_cico, json = gui, verify=False)
        return (out)
    
##############################################################################################

def off_4():
    # print('hàm uv1')
    with open('./database/json/total_data.json', "r", encoding='utf-8') as fin:
        data = json.load(fin)
    id = (data["id"])
    ip = (data["ip"])
    check = (data["check"])
    cam_4 = (data["cam_4"])
    data_timer_1 = (data["data_timer_1"])
    data_timer_2 = (data["data_timer_2"])
    data_timer_3 = (data["data_timer_3"])
    data_timer_4 = (data["data_timer_4"])
    LOG_4 = (data["LOG_4"])
    cap = cv2.VideoCapture(cam_4)
    retval, img = cap.read()
    if retval:
        strImg64 = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
    if not retval:
        with open('./database/json/abc.jpg', "rb") as f:
            strImg64 = base64.b64encode(f.read()).decode()
    # gui data
    r = requests.post(url, data=json.dumps({
        "mac_address": id +"_CAMERA4" ,
        "action_name": LOG_4,
        "timer": data_timer_4,
        "img": strImg64
    }), headers={
        'Content-type': 'application/json', 'Accept': 'text/plain'})
    code = r.status_code
    logger.info("\n Mã trạng thái HTTP server 1: %s", code)
    
    # end
    file = r.json()
    if code == 200:
        # if LOG_1 == "start":
        with open("./database/json/"+ id + ".json", "r", encoding='utf-8') as fin:
            check = json.load(fin)
        LOG_1 = (check[id]["LOG_1"])
        LOG_2 = (check[id]["LOG_2"])
        LOG_3 = (check[id]["LOG_3"])
        # LOG_4 = (check[id]["LOG_4"])
        reset = (check[id]["reset"])
        data = { id:{ "reset":0, "ip":ip,"LOG_1":LOG_1,"LOG_2": LOG_2,"LOG_3":LOG_3,"LOG_4":LOG_4}}
        with open('./database/json/' + id + '.json', 'w', encoding='utf-8') as out_file:
            json.dump(data, out_file, ensure_ascii=False, indent = 4)
        out = {"reset":reset,"LOG_1":LOG_1,"LOG_2":LOG_2,"LOG_3":LOG_3,"LOG_4":LOG_4}
        # logger.info("End: on_uv1(): DATA = {}",format(code))
        gui = {
        "mac_address": id +"_CAMERA4" ,
        "action_name": LOG_4,
        "timer": data_timer_4,
        "img": strImg64
        }
        x = requests.post(url_cico, json = gui, verify=False)
        return (out)
