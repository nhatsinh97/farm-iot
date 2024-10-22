import logging
import cv2
import json
import threading
from urllib3.exceptions import *
import requests
import base64
from app import logger, uv_data
# Tắt cảnh báo liên quan đến SSL
# http = urllib3.PoolManager()
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# API chính
url        = 'http://172.17.128.50:58185/api/Farm/postbiohistory' 
url_cico   = 'https://172.17.128.50:58187/api/Farm/postbiohistory'
link = "./database/data_setup/"
file = "data_setup.json"



def process_data(data):
    logger = logging.getLogger('cico_log')  # Đảm bảo lấy cùng logger
    # Chuyển đổi từ điển thành chuỗi JSON
    api_data = json.dumps(data, ensure_ascii=False, indent=4)
    # print(api_data)

    # Đọc dữ liệu từ file JSON
    with open(link + file, "r", encoding='utf-8') as fin:
        # Chuyển dữ liệu JSON từ file thành đối tượng Python
        data_json = json.load(fin)
    # Chuyển chuỗi JSON thành từ điển
    data_dict = json.loads(api_data)
    api_value = data_dict.get("idchip")  # Lấy giá trị "idchip" từ dữ liệu API
    name = data_dict.get("name")  # Lấy giá trị "name" từ dữ liệu API
    status = data_dict.get("status")  # Lấy giá trị "status" từ dữ liệu API
    ip = data_dict.get("ip")
    version = data_dict.get("version")
    
    # Trích xuất phần dữ liệu cần so sánh
    chipid_data = data_json.get('chipid', {})
    
    # Kiểm tra xem `idchip` có trong dữ liệu mẫu không
    if api_value in chipid_data:
        # if api_value == "181134ab4c24":
        #     logger.error("Dữ liệu:\n %s", api_data)
        # Lấy dữ liệu tương ứng với `idchip`
        chip_data = chipid_data[api_value]
        # print(chip_data)
        # Lấy thông tin tương ứng với `name` từ dữ liệu mẫu
        if name in chip_data:
            name_data = chip_data[name]
            mac_address = name_data["mac_address"]
            camera = name_data["camera"]
            timer = name_data["timer"]
            print(f"Dữ liệu cho {name}: {name_data}")
            cap = cv2.VideoCapture(camera)
            retval, img = cap.read()
            if retval:
                strImg64 = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
            if not retval:
                with open('./database/json/abc.jpg', "rb") as f:
                    strImg64 = base64.b64encode(f.read()).decode()
            # Tạo data gửi server ,
            data = {
                "mac_address": mac_address ,
                "action_name": status,
                "timer": timer,
                "img": strImg64
            }
            uv_data(data)
            # with open(link + "test1.json" , 'w', encoding='utf-8') as fout:
            #     json.dump(data, fout, ensure_ascii=False, indent=4)
            #     print('Đã lưu file')

            # gui data
            r = requests.post("http://172.17.128.50:58185/api/Farm/postbiohistory", json.dumps(data), headers = {'Content-type': 'application/json', 'Accept': 'text/plain'})
            # code = r.status_code
            code = r.json()
            response_text = r.text  # Lấy nội dung trả về từ server
            # Ghi log kết quả sau khi xử lý
            data_log = {
                "mac_address": mac_address ,
                "action_name": status,
                "timer": timer
            }
            logger.critical("\n Dữ liệu process_data: %s\n Mã trạng thái HTTP server: %s, Phản hồi từ server: %s", data_log, code, response_text)
            # logger.critical("\n Dữ liệu process_data: %s\n Mã trạng thái HTTP server: %s", data_log, code)

            # Kiểm tra nếu mã phản hồi là 200 và phản hồi là hợp lệ
            if code == 203:
                # Cập nhật giá trị ip, version vào dữ liệu chính
                if 'about' in data_json['chipid'][api_value]:
                    data_json['chipid'][api_value]['about']['ip'] = ip
                    data_json['chipid'][api_value]['about']['version'] = version
                    # Lưu đối tượng dictionary thành file JSON
                    with open(link + file, 'w', encoding='utf-8') as fout:
                        json.dump(data_json, fout, ensure_ascii=False, indent=4)
                        logger.critical('Đã cập nhật dữ liệu about: %s', api_value)
                else:
                    logger.error("data api:%s data chipip: %s không tồn tại trong data_json: ", api_value, chip_data)
                    return "Lỗi api_value", 400
            
            if code != 203:
                logger.error("Lỗi từ server: %s\nResponse: %s\nPayload: data", code, response_text)
            return ("Mã trạng thái HTTP server:", code)
            
        else:
            logger.error(" \n Không tìm thấy thông tin cho ID: %s -> %s -> %s", api_value, name, status)
            return api_value, name, status
    else:
        logger.error("Dữ liệu không trùng khớp hoặc không tìm thấy.")
        return None
