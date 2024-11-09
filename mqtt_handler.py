import json
import logging
import paho.mqtt.client as mqtt
from queue import Queue

# Cấu hình logger cho file riêng
logger = logging.getLogger('mqtt_handler')
logger.setLevel(logging.DEBUG)

# Thông tin MQTT
BROKER_ADDRESS = "172.17.128.24"
PORT = 1883
TOPIC = "test/topic"

# Khởi tạo hàng đợi để truyền dữ liệu đến file chính
mqtt_data_queue = Queue()

# Callback khi kết nối thành công
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT Broker!")
    else:
        logger.error(f"Failed to connect, return code {rc}")

# Callback khi nhận được tin nhắn từ MQTT
def on_message(client, userdata, message):
    logger.info("Received message from MQTT")
    try:
        data = json.loads(message.payload.decode())
        mqtt_data_queue.put(data)  # Đưa dữ liệu vào hàng đợi
    except json.JSONDecodeError:
        logger.error("Lỗi giải mã JSON.")

# Hàm bắt đầu client MQTT
def start_mqtt_client():
    client = mqtt.Client("MQTT_Change_Detector")
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_ADDRESS, PORT)
    client.subscribe(TOPIC)
    client.loop_start()  # Chạy dưới nền

# Hàm để lấy dữ liệu từ hàng đợi, dành cho file chính
def get_mqtt_data():
    if not mqtt_data_queue.empty():
        return mqtt_data_queue.get()
    return None
