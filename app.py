import cv2
import base64
import uuid
import random
import queue
import subprocess
import ast
import json
import time
import logging
import data_processor
import paho.mqtt.client as mqtt
from config import Config
from application.controllers.main_controller import main
from logging import Formatter, StreamHandler
from logging.handlers import TimedRotatingFileHandler
from threading import * 
from flask import Flask, make_response, render_template, redirect, send_from_directory, url_for, request, session, flash, send_file
from werkzeug.utils import secure_filename  # Thêm dòng này để xử lý tên file an toàn
from flask import jsonify
import os
from datetime import datetime, timedelta
from influxdb import InfluxDBClient

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

# Đảm bảo không có nhiều file handlers (cách tối ưu)
logger.handlers = [stream_handler, file_handler]

logger.info("Start: GF-CICO")

# Thông tin kết nối
host = 'localhost'  # hoặc địa chỉ IP của server InfluxDB
port = 8086
username = 'cico'
password = '2020@GreenFeed'  # Đặt mật khẩu của bạn ở đây
database = 'cico_iot'

# Tạo kết nối với InfluxDB
client = InfluxDBClient(host=host, port=port, username=username, password=password, database=database)

# Kiểm tra kết nối
logger.info("Danh sách các cơ sở dữ liệu:")
logger.info(client.get_list_database())

# Chuyển sang sử dụng cơ sở dữ liệu cụ thể
client.switch_database(database)

# Tạo một hàng đợi để truyền dữ liệu giữa các luồng
data_queue = queue.Queue()

app = Flask(__name__)
# Khóa bí mật để mã hóa session
app.secret_key = '4s$eJ#8dLpRtYkMnCbV2gX1fA3h'
app.config.from_object(Config)
app.register_blueprint(main)

# Thông tin MQTT
BROKER_ADDRESS = "172.17.128.24"
PORT = 1883
TOPIC = "PLC/LOGO"
# Biến lưu trữ giá trị trước đó của P1 và P2
previous_P1_value = None
previous_P2_value = None

# Biến lưu trữ số lượng request của từng 'name' theo 'idchip'
request_limit = {}
LIMIT_TIME = 60  # Thời gian giới hạn (60 giây)
MAX_REQUESTS = 3  # Số request tối đa được phép trong khoảng thời gian LIMIT_TIME
# Khởi tạo bộ đếm tổng số request của tất cả thiết bị và từng thiết bị
total_requests = 0
device_requests = {}

# Cơ sở dữ liệu người dùng lưu trong file JSON
# Đường dẫn đến file JSON chứa thông tin server
SERVER_FILE = './database/data_setup/servers.json'
DATA_FILE = './database/data_setup/data_setup.json'
# Đường dẫn tới file JSON lưu lịch sử số lượng request của các thiết bị
REQUEST_HISTORY_FILE = './database/data_setup/request_history.json'
# Đường dẫn đến file users.json
USER_FILE = os.path.join(os.getcwd(), './database/data_setup/users.json')
# Biến toàn cục lưu trữ kết quả số lượng thiết bị online, offline và tổng
device_status = {
    "online": 0,
    "offline": 0,
    "total": 0  # Thêm biến lưu tổng số thiết bị
}

# Hàm callback khi kết nối thành công
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        # print("Kết nối đến MQTT broker thành công")
        client.subscribe(TOPIC)
    else:
        logger.error(f"Lỗi kết nối với mã: {rc}")

# Hàm callback khi nhận được tin nhắn từ MQTT
def on_message(client, userdata, message):
    global previous_P1_value, previous_P2_value
    try:
        # Chuyển dữ liệu JSON từ chuỗi thành từ điển Python
        data = json.loads(message.payload.decode())
        
        # Trích xuất các giá trị từ dữ liệu
        reported = data.get("state", {}).get("reported", {})
        
        P1_desc = reported.get("P1", {}).get("desc", "N/A")
        P1_value = reported.get("P1", {}).get("value", [])[0] if reported.get("P1", {}).get("value") else None
        
        P2_desc = reported.get("P2", {}).get("desc", "N/A")
        P2_value = reported.get("P2", {}).get("value", [])[0] if reported.get("P2", {}).get("value") else None

        logotime = reported.get("$logotime", "N/A")
        
        # Kiểm tra sự thay đổi giá trị P1 và đưa vào hàng đợi nếu có thay đổi
        if P1_value is not None and P1_value != previous_P1_value:
            status = "start" if P1_value == 1 and previous_P1_value == 0 else "end"
            logger.critical(f"Giá trị của P1 đã thay đổi từ {previous_P1_value} thành {P1_value} với status: {status}")
            # Thêm sự kiện thay đổi vào hàng đợi logger.critical
            data_queue.put({
                "idchip": "9838eee342a8",
                "ip": "10.16.40.38",
                "version": "3.11",
                "name": "uv3",
                "status": status
            })
            previous_P1_value = P1_value  # Cập nhật giá trị mới vào biến lưu trữ

        # Kiểm tra sự thay đổi giá trị P2 và cập nhật status theo điều kiện
        if P2_value is not None and P2_value != previous_P2_value:
            status = "start" if P2_value == 1 and previous_P2_value == 0 else "end"
            logger.critical(f"Giá trị của P2 đã thay đổi từ {previous_P2_value} thành {P2_value} với status: {status}")
            # Thêm sự kiện thay đổi vào hàng đợi với status phù hợp logger.critical
            data_queue.put({
                "idchip": "9838eee342a8",
                "ip": "10.16.40.38",
                "version": "3.11",
                "name": "uv4",
                "status": status
            })
            previous_P2_value = P2_value  # Cập nhật giá trị mới vào biến lưu trữ

        # In ra dữ liệu để kiểm tra
        # print(f"P1 - {P1_desc}: {P1_value}")
        # print(f"P2 - {P2_desc}: {P2_value}")
        # print(f"Logotime: {logotime}")
        # print("-" * 30)
        
    except json.JSONDecodeError:
        logger.error("Lỗi giải mã JSON.")
# Khởi tạo MQTT client bên ngoài hàm
mqtt_client = mqtt.Client("Server_app")
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Hàm khởi động vòng lặp MQTT trong một luồng riêng
def start_mqtt_loop():
    try:
        print("Đang kết nối đến MQTT broker...")
        mqtt_client.connect(BROKER_ADDRESS, PORT)
        mqtt_client.loop_forever()  # Sử dụng loop_forever để giữ kết nối liên tục
    except Exception as e:
        logger.error(f"MQTT Loop Error: {e}")
        time.sleep(5)  # Chờ một chút trước khi thử lại kết nối

# Khởi động MQTT client trong một luồng riêng biệt
mqtt_thread = Thread(target=start_mqtt_loop)
mqtt_thread.daemon = True
mqtt_thread.start()

def start_ffmpeg(rtsp_url, output_path):
    ffmpeg_command = [
        "ffmpeg",
        "-i", rtsp_url,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-b:v", "1500k",
        "-maxrate", "1500k",
        "-bufsize", "3000k",
        "-f", "hls",
        "-hls_time", "2",
        "-hls_list_size", "10",
        "-hls_flags", "delete_segments",
        output_path
    ]

    # Chạy FFmpeg trong nền và không chặn ứng dụng Flask
    subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def ping_device(ip):
    """
    Ping đến địa chỉ IP, trả về True nếu online, False nếu offline.
    """
    try:
        # Sử dụng lệnh ping trên hệ điều hành (tùy hệ điều hành mà cú pháp có thể thay đổi)
        output = subprocess.check_output(["ping", "-c", "1", "-W", "1", ip], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False

def count_online_offline_devices():
    """
    Đếm số lượng thiết bị online và offline từ JSON
    """
    # Đọc dữ liệu JSON từ file hoặc từ nguồn dữ liệu nào đó
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    online = 0
    offline = 0

    # Duyệt qua tất cả các 'chipid' và các 'ip' trong JSON
    for chipid, chip_data in data['chipid'].items():
        device_ip = chip_data['about']['ip']
        if ping_device(device_ip):  # Kiểm tra xem thiết bị có online không
            online += 1
        else:
            offline += 1

    return online, offline
# Hàm để kiểm tra trạng thái thiết bị
def check_device_status_periodically():
    global device_status
    while True:
        # Kiểm tra và cập nhật trạng thái thiết bị
        online, offline = count_online_offline_devices()
        total = online + offline  # Tổng số thiết bị là tổng số thiết bị online và offline
        device_status["online"] = online
        device_status["offline"] = offline
        device_status["total"] = total  # Cập nhật tổng số thiết bị
        print(f"Checked device status: Online = {online}, Offline = {offline}, Total = {total}")
        
        # Thực hiện kiểm tra mỗi 60 giây
        time.sleep(300)
# Hàm đọc dữ liệu người dùng từ file JSON
def load_users():
    with open(USER_FILE, 'r') as f:
        return json.load(f)

def get_user_permissions(username):
    users = load_users()
    for user in users['users']:
        if user['username'] == username:
            return user['permissions']
    return []
def log_access(username):
    users = load_users()

    # Tìm người dùng theo username
    for user in users["users"]:
        if user["username"] == username:
            # Lấy địa chỉ IP của người dùng
            user_ip = request.remote_addr

            # Ghi nhận thời gian và IP truy cập
            access_record = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ip": user_ip
            }

            # Nếu chưa có lịch sử truy cập, tạo danh sách mới
            if "access_history" not in user:
                user["access_history"] = []

            # Thêm bản ghi mới vào lịch sử
            user["access_history"].append(access_record)

            # Lưu lại file JSON
            save_users(users)
            break
def update_user_permissions_in_file(users):
    with open('./database/data_setup/users.json', 'w') as f:
        json.dump(users, f, indent=4)
def update_user_permissions(username, new_permissions):
    users = load_users()
    for user in users['users']:
        if user['username'] == username:
            user['permissions'] = new_permissions
            break
    with open('./database/data_setup/users.json', 'w') as f:
        json.dump(users, f)
def save_to_file(data, filename= './database/data_setup/users.json'):
    # Mở file JSON và ghi lại danh sách người dùng đã được cập nhật
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Hàm lưu dữ liệu người dùng vào file JSON
def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f, indent=4)
    print(f"Đã lưu dữ liệu: {users}")  # In ra log để kiểm tra dữ liệu đã lưu
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # Mật khẩu đã mã hóa bằng MD5

        users = load_users()
        if any(user['username'] == username and user['password'] == password for user in users['users']):
            session['logged_in'] = True
            session['username'] = username  # Lưu username vào session
            flash('Đăng nhập thành công!')

            # Ghi nhận lịch sử truy cập
            log_access(username)

            return redirect(url_for('trangchinh'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không đúng!')
    
    return render_template('login.html')


@app.route('/manage_users')
def manage_users():
    if not session.get('logged_in'):
        return redirect(url_for('login'))  # Nếu chưa đăng nhập thì chuyển đến trang login
    
    username = session.get('username')
    
    # Gọi hàm để lấy quyền của người dùng hiện tại
    permissions = get_user_permissions(username)
    
    # Kiểm tra quyền 'manage_users'
    if 'manage_users' not in permissions:
        return "Bạn không có quyền quản lý người dùng", 403  # Nếu không có quyền
    
    # Lấy danh sách người dùng từ file JSON
    users = load_users().get('users', [])
    
    # Truyền danh sách user vào trang manage_users.html
    return render_template('manage_users.html', users=users)
def update_user_permissions(username, new_permissions):
    # Tải danh sách người dùng
    users = load_users()
    
    # Tìm người dùng cần cập nhật
    for user in users['users']:
        if user['username'] == username:
            # Cập nhật quyền
            user['permissions'] = new_permissions
            break
    
    # Ghi lại danh sách người dùng vào file JSON
    with open('path_to_your_users_file.json', 'w') as f:
        json.dump(users, f, indent=4)
@app.route('/edit_user_permissions/<username>', methods=['GET', 'POST'])
def edit_user_permissions(username):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # Kiểm tra quyền 'manage_users'
    current_user = session.get('username')
    if 'manage_users' not in get_user_permissions(current_user):
        return "Bạn không có quyền chỉnh sửa quyền", 403

    users = load_users()
    user = next((u for u in users['users'] if u['username'] == username), None)

    if not user:
        return "Người dùng không tồn tại", 404

    if request.method == 'POST':
        # Nhận danh sách quyền mới từ form (checkboxes có thể có nhiều giá trị)
        new_permissions = request.form.getlist('permissions')

        # Cập nhật quyền người dùng trong file JSON
        if new_permissions:  # Kiểm tra nếu có quyền mới
            user['permissions'] = new_permissions  # Cập nhật quyền mới cho user
            update_user_permissions_in_file(users)  # Ghi lại vào file

        flash('Đã cập nhật quyền thành công!')
        return redirect(url_for('manage_users'))

    return render_template('edit_user_permissions.html', user=user)

@app.route('/delete_user/<username>', methods=['POST'])
def delete_user(username):
    # Kiểm tra nếu người dùng đã đăng nhập
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # Kiểm tra quyền 'manage_users' của người dùng hiện tại
    current_user = session.get('username')
    if 'manage_users' not in get_user_permissions(current_user):
        return "Bạn không có quyền xóa người dùng", 403
    
    # Tải danh sách người dùng từ file JSON
    users = load_users()
    user_to_delete = next((u for u in users['users'] if u['username'] == username), None)
    
    if not user_to_delete:
        return "Người dùng không tồn tại", 404

    # Xóa người dùng khỏi danh sách
    users['users'].remove(user_to_delete)
    
    # Lưu lại danh sách người dùng vào file JSON
    save_to_file(users)  # Đã sửa lỗi ở đây
    
    flash(f'User {username} đã được xóa thành công.', 'success')
    return redirect(url_for('manage_users'))




@app.route('/admin/update_permissions', methods=['POST'])
def update_permissions():
    if session.get('username') != 'admin':
        return "Unauthorized", 403
    
    username = request.form['username']
    new_permissions = request.form.getlist('permissions')
    
    update_user_permissions(username, new_permissions)
    flash('Cập nhật quyền thành công!')
    return redirect(url_for('admin_panel'))  # Trang quản lý admin

# Route tạo tài khoản
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # Mật khẩu đã mã hóa bằng MD5

        # Kiểm tra nếu tài khoản đã tồn tại
        users = load_users()
        if any(user['username'] == username for user in users['users']):
            flash('Tên đăng nhập đã tồn tại!')
            return redirect(url_for('login'))
        # Tạo tài khoản mới với role 'user' và quyền 'view_dashboard'
        new_user = {
            "username": username,
            "password": password,
            "role": "user",
            "permissions": ["view_dashboard"]
        }
        # Thêm tài khoản mới vào file JSON
        users['users'].append(new_user)
        save_users(users)
        flash('Tài khoản đã được tạo thành công!')
        return redirect(url_for('login'))

    return render_template('register.html')

# API để lấy danh sách server
@app.route('/get_servers')
def get_servers():
    try:
        with open(SERVER_FILE, 'r') as file:
            servers = json.load(file)
    except FileNotFoundError:
        servers = []
    return jsonify(servers)
# API để lưu danh sách server
@app.route('/save_servers', methods=['POST'])
def save_servers():
    servers = request.json
    with open(SERVER_FILE, 'w') as file:
        json.dump(servers, file)
    return '', 204
@app.route('/uv')
def uv():
    return render_template('uv/uv.html')
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    username = session.get('username')
    permissions = get_user_permissions(username)
    return render_template('common/Dashboard.html', permissions=permissions)
@app.route('/testcode')
def testcode():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    username = session.get('username')
    permissions = get_user_permissions(username)
    return render_template('testcode.html', permissions=permissions)
# Trang logout để thoát
@app.route("/logout")
def logout():
    session['logged_in'] = False  # Xóa trạng thái đăng nhập
    return redirect(url_for('login'))  # Chuyển về trang login

@app.route("/")
def home():
    # Kiểm tra xem người dùng đã đăng nhập hay chưa
    if not session.get('logged_in'):
        return redirect(url_for('login'))  # Nếu chưa đăng nhập thì chuyển đến trang login
    # Lấy username từ session
    username = session.get('username')
    users = load_users()
    user = next((u for u in users['users'] if u['username'] == username), None)
    
    if not user:
        return "Người dùng không tồn tại", 404
    
    # Gọi hàm để lấy danh sách quyền của người dùng
    permissions = get_user_permissions(username)
    
    # Truyền danh sách quyền này vào template
    seo = {'title': 'Farm Tây Ninh 4 || Quản lý công việc'}
    return render_template('index.html', seo=seo, permissions=permissions, user=user) 

# Route để phục vụ nội dung mới qua AJAX
@app.route('/check_iot')
def check_iot():
    # Tạo một đối tượng dữ liệu
    data_object = {
        "NAME": "Tên máy chủ",  # Thay thế bằng giá trị thực
        "Status": "OFFLINE",  # Thay thế bằng giá trị thực
        "IP": "192.168.1.1"     # Thay thế bằng giá trị thực
    }
    return render_template('status_server.html', data_object=data_object)

# Route để phục vụ nội dung khác qua AJAX
@app.route('/view_manage_users')
def another_content():
    return render_template('on-off.html')

# Trang chính yêu cầu phải đăng nhập
@app.route("/trangchinh")
def trangchinh():
    # Kiểm tra xem người dùng đã đăng nhập hay chưa
    if not session.get('logged_in'):
        return redirect(url_for('login'))  # Nếu chưa đăng nhập thì chuyển đến trang login
    # Lấy username từ session
    username = session.get('username')
    users = load_users()
    user = next((u for u in users['users'] if u['username'] == username), None)
    
    if not user:
        return "Người dùng không tồn tại", 404
    
    # Gọi hàm để lấy danh sách quyền của người dùng
    permissions = get_user_permissions(username)
    
    # Truyền danh sách quyền này vào template
    # Truyền kết quả trạng thái thiết bị và tổng số thiết bị vào template
    seo = {'title': 'Farm Tây Ninh 4 || Quản lý công việc'}
    return render_template(
        'index.html',
        seo=seo,
        permissions=permissions,
        user=user,
        online_devices=device_status["online"],
        offline_devices=device_status["offline"],
        total_devices=device_status["total"], # Truyền thêm tổng số thiết bị
        totalRequests = total_requests
    ) 
# Đường dẫn đến link RTSP của camera
rtsp_url = "rtsp://admin:admin@2024!@10.16.40.27/cam/realmonitor?channel=1&subtype=00&authbasic=YWRtaW46QWRtaW4xMjM="
# Thời gian chờ giữa các lần lấy frame (30 phút = 1800 giây)
capture_interval = 1800  # 30 phút

# Tên file ảnh sẽ lưu
image_file = 'static/captured_frame.jpg'
@app.route('/camera/<path:filename>')
def serve_camera_file(filename):
    response = make_response(send_from_directory('static/camera', filename))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
@app.route('/camera')
def camera():
    """ Trang web chính để hiển thị ảnh lấy từ camera. """
    return render_template('camera/camera.html')

@app.route('/camera_image')
def camera_image():
    """ Route để hiển thị ảnh từ camera. """
    return send_file(image_file, mimetype='image/jpeg')


def capture_frame():
    """ Hàm để lấy frame từ link RTSP và lưu thành file ảnh. """
    global image_file
    while True:
        # Kết nối tới RTSP camera
        cap = cv2.VideoCapture(rtsp_url)
        if not cap.isOpened():
            print(f"Không thể kết nối tới camera tại {rtsp_url}")
            time.sleep(capture_interval)
            continue
        
        # Đọc frame từ video stream
        ret, frame = cap.read()
        if ret:
            # Lưu frame thành file ảnh
            cv2.imwrite(image_file, frame)
            print(f"Lấy frame và lưu vào {image_file}")
        else:
            print("Không thể lấy frame từ camera")

        # Giải phóng camera
        cap.release()

        # Chờ 30 phút trước khi lấy frame tiếp theo
        time.sleep(capture_interval)


# Hàm lưu số request của thiết bị vào file JSON
def save_request_history(idchip):
    logger.error(idchip)
    # Mở file JSON hoặc tạo mới nếu chưa có
    try:
        with open(REQUEST_HISTORY_FILE, 'r+') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    # Lấy thời gian hiện tại
    current_time = datetime.utcnow().isoformat() + 'Z'

    # Nếu idchip chưa tồn tại trong dữ liệu, tạo mới
    if idchip not in data:
        data[idchip] = []

    # Kiểm tra xem có bản ghi nào cho thời gian gần nhất không
    if data[idchip] and data[idchip][-1]["timestamp"][:16] == current_time[:16]:
        # Cùng thời gian (cùng phút), tăng request_count
        data[idchip][-1]["request_count"] += 1
    else:
        # Thêm bản ghi mới nếu là thời gian mới
        data[idchip].append({
            "timestamp": current_time,
            "request_count": 1  # Bắt đầu với 1 request
        })

    # Giữ lịch sử tối thiểu trong 24 giờ, xóa dữ liệu cũ hơn 1 ngày
    cutoff_time = datetime.utcnow() - timedelta(days=1)
    data[idchip] = [entry for entry in data[idchip] if datetime.fromisoformat(entry["timestamp"][:-1]) > cutoff_time]

    # Lưu dữ liệu vào file JSON
    with open(REQUEST_HISTORY_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


# API nhận dữ liệu từ thiết bị IoT
@app.route('/api', methods=['POST'])
def iot_request():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        try:
            global total_requests
            data = request.json
            idchip = data.get('idchip')  # Lấy 'idchip' từ request
            name = data.get('name')  # Lấy 'name' từ request
            
            if not idchip or not name:
                return jsonify({"error": "Thiếu idchip hoặc name trong dữ liệu"}), 400
            # Cập nhật bộ đếm tổng request của tất cả thiết bị
            total_requests += 1

            # Cập nhật bộ đếm request cho thiết bị tương ứng trong một ngày
            today = datetime.now().strftime("%Y-%m-%d")
            if idchip not in device_requests:
                device_requests[idchip] = {}
            
            if today not in device_requests[idchip]:
                device_requests[idchip][today] = 0
        
            device_requests[idchip][today] += 1

            # Tạo key để theo dõi từng 'name' theo 'idchip'
            key = f"{idchip}_{name}"

            # Kiểm tra xem cặp 'idchip' và 'name' này đã được lưu trong request_limit hay chưa
            if key in request_limit:
                requests_info = request_limit[key]
                request_count, last_request_time = requests_info

                # Nếu quá số request cho phép trong khoảng thời gian LIMIT_TIME
                if time.time() - last_request_time <= LIMIT_TIME:
                    if request_count >= MAX_REQUESTS:
                        logger.error(" \n Quá nhiều yêu cầu từ thiết bị: %s", key)
                        return jsonify({"error": "Quá nhiều yêu cầu từ thiết bị"}), 429
                    else:
                        request_limit[key] = (request_count + 1, last_request_time)
                else:
                    # Reset lại nếu đã qua khoảng thời gian giới hạn
                    request_limit[key] = (1, time.time())
            else:
                # Tạo mới cho thiết bị nếu chưa có trong danh sách
                request_limit[key] = (1, time.time())
            # Ghi dữ liệu vào file (nếu cần)
            with open('./database/data_setup/total_data.json', 'w', encoding='utf-8') as out_file:
                json.dump(data, out_file, ensure_ascii=False, indent=4)
            # Ghi nhận request của thiết bị vào file JSON
            save_request_history(idchip)
            # Xử lý dữ liệu như bình thường (ví dụ: đưa dữ liệu vào hàng đợi)
            data_queue.put(data)
            
            return jsonify({"message": "Request processed successfully"}), 200
        
        except json.JSONDecodeError:
            return jsonify({"error": "Lỗi phân tích JSON"}), 400
    else:
        return jsonify({"error": "Content-Type không được hỗ trợ"}), 400
    
@app.route('/total_requests', methods=['GET'])
def get_total_requests():
    return jsonify({'total_requests': total_requests})
@app.route('/top_devices', methods=['GET'])
def get_top_devices():
    today = datetime.now().strftime("%Y-%m-%d")
    # Lọc ra tất cả thiết bị và số lượng request trong ngày hôm nay
    requests_today = {
        idchip: requests.get(today, 0)
        for idchip, requests in device_requests.items()
    }
    # Sắp xếp và lấy top 5 thiết bị có số lượng request lớn nhất
    top_devices = sorted(requests_today.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return jsonify({'top_devices': top_devices})

@app.route('/device_requests', methods=['GET'])
def get_device_requests():
    idchip = request.args.get('idchip')
    today = datetime.now().strftime("%Y-%m-%d")

    if not idchip or idchip not in device_requests or today not in device_requests[idchip]:
        return jsonify({'total_requests_today': 0})

    return jsonify({'total_requests_today': device_requests[idchip][today]})

def process_data_from_queue():
    while True:
        data = data_queue.get()  # Lấy dữ liệu từ hàng đợi
        if data:
            # Gửi dữ liệu qua file phụ để xử lý
            processed_data = data_processor.process_data(data)
            # In kết quả xử lý (hoặc có thể làm gì đó khác với dữ liệu)
            print("Dữ liệu sau khi xử lý:", processed_data)
@app.route('/access_history', methods=['GET', 'POST'])
def access_history():
    users = load_users()
    history = []

    # Lấy thời gian hiện tại
    now = datetime.now()

    # Nếu là POST request, kiểm tra xem người dùng nhấn nút nào
    if request.method == 'POST':
        filter_value = request.form.get('filter')

        if filter_value == 'today':
            # Lọc dữ liệu của ngày hôm nay
            start_date = now.date().strftime("%Y-%m-%d")
            end_date = start_date
        elif filter_value == 'this_week':
            # Lọc dữ liệu của tuần này
            start_date = (now - timedelta(days=now.weekday())).strftime("%Y-%m-%d")  # Thứ hai đầu tuần
            end_date = now.date().strftime("%Y-%m-%d")
        elif filter_value == 'this_month':
            # Lọc dữ liệu của tháng này
            start_date = now.replace(day=1).strftime("%Y-%m-%d")  # Ngày đầu tiên của tháng
            end_date = now.date().strftime("%Y-%m-%d")
        else:
            # Lấy dữ liệu từ form khi người dùng nhập tay
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')

        # Lấy dữ liệu lịch sử đăng nhập từ từng người dùng
        for user in users['users']:
            if 'access_history' in user:  # Kiểm tra nếu 'access_history' tồn tại
                for record in user['access_history']:
                    record_date = record['timestamp'].split(' ')[0]  # Lấy ngày từ timestamp
                    if start_date <= record_date <= end_date:
                        history.append({
                            "username": user['username'],
                            "ip": record['ip'],
                            "timestamp": record['timestamp']
                        })
    else:
        # Lấy tất cả lịch sử nếu không có lọc theo ngày
        for user in users['users']:
            if 'access_history' in user:
                for record in user['access_history']:
                    history.append({
                        "username": user['username'],
                        "ip": record['ip'],
                        "timestamp": record['timestamp']
                    })

    # Sắp xếp lịch sử theo thứ tự thời gian giảm dần
    history.sort(key=lambda x: datetime.strptime(x['timestamp'], "%Y-%m-%d %H:%M:%S"), reverse=True)

    return render_template('access_history/access_history.html', history=history)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/profile')
def profile():
    # Lấy thông tin người dùng từ session hoặc file JSON
    username = session.get('username')
    users = load_users()

    # Tìm user hiện tại
    user = next((u for u in users['users'] if u['username'] == username), None)

    if not user:
        return "User not found", 404

    return render_template('profile.html', user=user)



@app.route('/change_avatar', methods=['POST'])
def change_avatar():
    if 'avatar' not in request.files:
        flash('Không tìm thấy file ảnh.')
        return redirect(url_for('profile'))

    file = request.files['avatar']
    if file.filename == '':
        flash('Chưa chọn file ảnh.')
        return redirect(url_for('profile'))

    if file:
        # Lưu file ảnh vào thư mục
        username = session.get('username')
        avatar_filename = f'{username}.jpg'
        avatar_path = os.path.join('./static/avatar/', avatar_filename)
        file.save(avatar_path)  # Lưu ảnh đại diện mới vào thư mục

        # Cập nhật đường dẫn ảnh đại diện vào file JSON
        users = load_users()
        user = next((u for u in users['users'] if u['username'] == username), None)
        if user:
            user['avatar'] = f'/static/avatar/{avatar_filename}'  # Cập nhật đường dẫn ảnh vào file JSON
            save_users(users)  # Lưu lại file JSON với đường dẫn mới

        flash('Thay đổi ảnh đại diện thành công.')
    
    return redirect(url_for('profile'))


@app.route('/change_password', methods=['POST'])
def change_password():
    old_password = request.form['old_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    
    username = session.get('username')
    users = load_users()
    user = next((u for u in users['users'] if u['username'] == username), None)

    if user and user['password'] == old_password:
        if new_password == confirm_password:
            user['password'] = new_password  # Cập nhật mật khẩu mới
            save_users(users)  # Lưu lại file JSON
            flash('Đổi mật khẩu thành công!')
        else:
            flash('Mật khẩu mới không khớp.')
    else:
        flash('Mật khẩu cũ không đúng.')

    return redirect(url_for('profile'))
@app.route('/api/get_device_realtime_data')
def get_device_realtime_data():
    # Giả lập dữ liệu real-time cho các thiết bị
    data = {
        'device1': random.randint(30, 80),  # Giá trị request ngẫu nhiên cho thiết bị 1
        'device2': random.randint(30, 80),  # Giá trị request ngẫu nhiên cho thiết bị 2
        'device3': random.randint(30, 80)   # Giá trị request ngẫu nhiên cho thiết bị 3
    }
    return jsonify(data)

# API để lấy dữ liệu lịch sử request từ file JSON
@app.route('/get-request-history')
def get_request_history():
    timeframe = request.args.get('timeframe', 'live')

    # Đọc dữ liệu từ file JSON
    with open(REQUEST_HISTORY_FILE, 'r') as file:
        data = json.load(file)

    # Tính toán thời gian cắt (cutoff) dựa trên 'timeframe'
    now = datetime.utcnow()
    if timeframe == '1h':
        cutoff = now - timedelta(hours=1)
    elif timeframe == '6h':
        cutoff = now - timedelta(hours=6)
    elif timeframe == '1d':
        cutoff = now - timedelta(days=1)
    elif timeframe == '1w':
        cutoff = now - timedelta(weeks=1)
    elif timeframe == '1M':
        cutoff = now - timedelta(days=30)
    elif timeframe == '3M':
        cutoff = now - timedelta(days=90)
    else:  # Live mode
        cutoff = now - timedelta(minutes=5)  # 5 phút gần nhất cho chế độ live

    # Lọc dữ liệu dựa trên thời gian cắt (cutoff)
    filtered_data = {}
    for idchip, entries in data.items():
        filtered_data[idchip] = [entry for entry in entries if datetime.fromisoformat(entry['timestamp'][:-1]) > cutoff]

    return jsonify(filtered_data)

@app.route('/get-chart-data', methods=['GET'])
def get_chart_data():
    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)

        chart_data = {
            "labels": [],
            "datasets": []
        }

        # Duyệt qua từng thiết bị (idchip)
        for chipid, chip_data in data['chipid'].items():
            device_requests = chip_data.get("requests", [])
            timestamps = [req['timestamp'] for req in device_requests]
            values = [req['value'] for req in device_requests]

            if len(chart_data['labels']) == 0:
                chart_data['labels'] = timestamps  # Lấy nhãn thời gian từ thiết bị đầu tiên

            # Tạo dữ liệu cho từng idchip
            chart_data['datasets'].append({
                "label": chipid,
                "data": values,
                "borderColor": get_random_color(),
                "fill": False
            })

        return jsonify(chart_data)
    except Exception as e:
        return jsonify({"error": str(e)})

# Hàm tạo màu ngẫu nhiên cho biểu đồ
def get_random_color():
    import random
    letters = '0123456789ABCDEF'
    color = '#'
    for i in range(6):
        color += random.choice(letters)
    return color

def query_device_data_from_db():
    client = InfluxDBClient(host=host, port=port, username=username, password=password, database=database)
    query = 'SELECT * FROM iot_tickets'
    result = client.query(query)

    device_events = []
    for point in result.get_points():
        event = {
            "device_name": point.get('mac_address', ''),
            "mac_address": point.get('mac_address', ''),
            "start_time": point.get('start_time', ''),
            "end_time": point.get('end_time', ''),
            "status": point.get('status', ''),
            "start_image": point.get('start_img', ''),
            "end_image": point.get('end_img', '')
        }
        device_events.append(event)
    
    return device_events

@app.route('/api/get_device_data', methods=['GET'])
def get_device_data():
    # Lấy dữ liệu từ InfluxDB hoặc cơ sở dữ liệu
    data = query_device_data_from_db()  # Hàm lấy dữ liệu từ cơ sở dữ liệu
    
    if data:
        return jsonify(data), 200
    else:
        return jsonify({"error": "No data found"}), 404
def uv_data(data):
    # Lưu hình ảnh trước
    image_path = save_image(data['img'], data['mac_address'], data['action_name'])
    # Cập nhật ticket vào InfluxDB
    data['img'] = image_path  # Thay thế base64 bằng đường dẫn ảnh
    # update_ticket_in_db(data)  # Cập nhật ticket
    return
def generate_ticket_id():
    # Tạo ra một ID duy nhất bằng cách sử dụng UUID4
    return str(uuid.uuid4())
def generate_unique_filename(mac_address, action_name):
    # Sử dụng UUID4 để tạo ra tên file duy nhất
    unique_id = str(uuid.uuid4())  # Tạo ra một ID duy nhất
    return f'{mac_address}_{action_name}_{unique_id}.jpg'

def save_image(base64_img, mac_address, action_name):
    try:
        # Giải mã hình ảnh từ base64
        img_data = base64.b64decode(base64_img)

        # Tạo đường dẫn thư mục nếu chưa tồn tại
        directory = './static/data_uv/images/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Tạo tên file với ID duy nhất
        file_name = generate_unique_filename(mac_address, action_name)
        file_path = os.path.join(directory, file_name)

        # Lưu file vào hệ thống
        with open(file_path, 'wb') as f:
            f.write(img_data)

        print(f"Image saved successfully: {file_path}")
        return file_path  # Trả về đường dẫn file để lưu vào cơ sở dữ liệu
    except Exception as e:
        print(f"Error saving image: {e}")
        return None
    
def find_in_progress_ticket(mac_address):
    # Kết nối với InfluxDB
    client = InfluxDBClient(host=host, port=port, username=username, password=password, database=database)
    
    # Truy vấn dữ liệu từ cơ sở dữ liệu với action_name = 'start' và chưa có hành động kết thúc (action_name = 'end')
    query = f"SELECT * FROM iot_tickets WHERE mac_address = '{mac_address}' AND action_name = 'start' ORDER BY time DESC LIMIT 1"
    
    try:
        result = client.query(query)
        points = list(result.get_points())
        
        if points:
            # Trả về phiếu đầu tiên (vì đã sắp xếp theo thời gian giảm dần)
            return points[0]
        else:
            return None
    except Exception as e:
        print(f"Error querying in_progress ticket: {e}")
        return None
    finally:
        client.close()
def process_start(mac_address, timer, img):
    start_time = datetime.utcnow().isoformat() + 'Z'  # Thời gian bắt đầu
    # Giải mã Base64 hình ảnh
    decoded_img = base64.b64decode(img)
    # save_image(decoded_img, f"{mac_address}_start_{start_time}.jpg")
    
    # Tạo phiếu mới
    ticket = {
        "id": generate_ticket_id(),  # Hàm sinh ID duy nhất cho phiếu
        "mac_address": mac_address,
        "start_time": start_time,
        "start_img": f"{mac_address}_start_{start_time}.jpg",
        "timer": timer,
        "status": "in_progress"
    }
    # Lưu phiếu vào cơ sở dữ liệu (InfluxDB hoặc MongoDB tùy chọn)
    # save_ticket_to_db(ticket)

def process_end(mac_address, img):
    end_time = datetime.utcnow().isoformat() + 'Z'
    decoded_img = base64.b64decode(img)
    # save_image(decoded_img, f"{mac_address}_end_{end_time}.jpg")
    
    # Tìm phiếu đang hoạt động theo mac_address
    ticket = find_in_progress_ticket(mac_address)
    if ticket:
        ticket['end_time'] = end_time
        ticket['end_img'] = f"{mac_address}_end_{end_time}.jpg"
        ticket['status'] = 'completed'
        # Cập nhật phiếu
        # update_ticket_in_db(ticket)
    else:
        raise Exception("Không tìm thấy phiếu đang hoạt động.")
def update_ticket_in_db(data):
    # Kết nối với InfluxDB
    client = InfluxDBClient(host=host, port=port, username=username, password=password, database=database)

    # Chuẩn bị dữ liệu để ghi vào InfluxDB
    json_body = [
        {
            "measurement": "iot_tickets",
            "tags": {
                "mac_address": data['mac_address'],
                "action_name": data['action_name']  # Giữ lại thông tin hành động (start hoặc end)
            },
            "time": datetime.utcnow().isoformat() + 'Z',  # Sử dụng timestamp hiện tại
            "fields": {
                "status": data['action_name'],  # Cập nhật trạng thái
                "timer": data.get('timer', 0),  # Lưu lại giá trị timer nếu có
                "img": data['img']  # Lưu hình ảnh base64
            }
        }
    ]

    try:
        # Ghi dữ liệu vào InfluxDB
        client.write_points(json_body)
        print("Ticket updated successfully.")
    except Exception as e:
        print(f"Error updating ticket in InfluxDB: {e}")
    finally:
        client.close()
    
def save_ticket_to_db(ticket_id, mac_address, action_name, timer, img):
    # Kết nối với cơ sở dữ liệu InfluxDB
    client = InfluxDBClient(host=host, port=port, username=username, password=password, database=database)
    
    # Tạo điểm dữ liệu để lưu vào InfluxDB
    json_body = [
        {
            "measurement": "iot_tickets",
            "tags": {
                "mac_address": mac_address,
                "ticket_id": ticket_id
            },
            "fields": {
                "action_name": action_name,
                "timer": int(timer),
                "img": img  # Đây là hình ảnh base64 được truyền vào
            },
            "time": datetime.utcnow().isoformat()  # Lưu timestamp hiện tại
        }
    ]

    # Ghi dữ liệu vào InfluxDB
    try:
        client.write_points(json_body)
        print(f"Ticket {ticket_id} saved successfully.")
    except Exception as e:
        print(f"Error saving ticket {ticket_id}: {e}")
    finally:
        client.close()  # Đảm bảo kết nối được đóng sau khi lưu xong
@app.route('/api/get_device_events', methods=['GET'])
def get_device_events():
    try:
        # Kết nối với InfluxDB để lấy dữ liệu sự kiện của các thiết bị IoT
        client = InfluxDBClient(host='localhost', port=8086, username='cico', password='your_password', database='cico_iot')
        query = 'SELECT * FROM iot_tickets ORDER BY time DESC LIMIT 50'  # Lấy 50 sự kiện gần nhất
        result = client.query(query)
        events = list(result.get_points())

        # Chuyển đổi dữ liệu thành danh sách JSON
        event_list = []
        for event in events:
            event_list.append({
                'name': event['mac_address'],
                'mac_address': event['mac_address'],
                'start_time': event['start_time'],
                'end_time': event.get('end_time', None),
                'status': event['status'],
                'start_img': event['start_img'],
                'end_img': event.get('end_img', None)
            })

        return jsonify(event_list)
    except Exception as e:
        return jsonify({"error": str(e)})

def start_ffmpeg(rtsp_url, output_path):
    ffmpeg_command = [
        "ffmpeg",
        "-i", rtsp_url,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-b:v", "1500k",
        "-maxrate", "1500k",
        "-bufsize", "3000k",
        "-f", "hls",
        "-hls_time", "2",
        "-hls_list_size", "10",
        "-hls_flags", "delete_segments+append_list",
        output_path
    ]

    # Chạy FFmpeg trong nền và không chặn ứng dụng Flask
    subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def clean_old_ts_files(directory, max_files=20):
    ts_files = [f for f in os.listdir(directory) if f.endswith(".ts")]
    ts_files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)))

    if len(ts_files) > max_files:
        for file in ts_files[:-max_files]:
            os.remove(os.path.join(directory, file))
            print(f"Đã xóa tệp: {file}")


if __name__ == '__main__':
    try:
        # Tạo và khởi động luồng để kiểm tra trạng thái thiết bị định kỳ
        device_check_thread = Thread(target=check_device_status_periodically)
        device_check_thread.daemon = True
        device_check_thread.start()

        # Tạo và khởi động luồng để xử lý dữ liệu từ hàng đợi
        processing_thread = Thread(target=process_data_from_queue)
        processing_thread.daemon = True
        processing_thread.start()

        # Khởi động Flask trong luồng chính
        app.run(host='0.0.0.0', port=58888, debug=False)
    except Exception as e:
        # Ghi mã lỗi vào logging
        logger.error("Đã xảy ra lỗi: \n %s", e)