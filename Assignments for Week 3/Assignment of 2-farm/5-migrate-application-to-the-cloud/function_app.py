import os
import azure.functions as func
import logging
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod

app = func.FunctionApp()

# Relay on Function
@app.route(route="relay_on", auth_level=func.AuthLevel.ANONYMOUS)
def TurnRelayOn(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Đã nhận yêu cầu BẬT rơ-le qua HTTP.')
    
    try:
        # Lấy chìa khóa và tên thiết bị từ cấu hình
        conn_str = os.environ["IOT_HUB_CONNECTION_STRING"]
        device_id = os.environ["TARGET_DEVICE_ID"]
        
        # Nhấc bộ đàm lên
        registry_manager = IoTHubRegistryManager(conn_str)
        
        # Đóng gói lệnh: gọi hàm "SetRelayState" trên thiết bị, truyền trạng thái "ON"
        # (Lưu ý: method_name phải khớp với code C/Python chạy trên thiết bị thật của em)
        method_payload = CloudToDeviceMethod(method_name="SetRelayState", payload="ON")
        
        # Gửi lệnh đi
        registry_manager.invoke_device_method(device_id, method_payload)
        
        return func.HttpResponse("Đã gửi lệnh BẬT xuống thiết bị thành công!", status_code=200)
    except Exception as e:
        logging.error(f"Lỗi khi gửi lệnh: {str(e)}")
        return func.HttpResponse("Gửi lệnh thất bại.", status_code=500)

# Relay Off Function
@app.route(route="relay_off", auth_level=func.AuthLevel.ANONYMOUS)
def TurnRelayOff(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Đã nhận yêu cầu TẮT rơ-le qua HTTP.')
    
    try:
        conn_str = os.environ["IOT_HUB_CONNECTION_STRING"]
        device_id = os.environ["TARGET_DEVICE_ID"]
        
        registry_manager = IoTHubRegistryManager(conn_str)
        method_payload = CloudToDeviceMethod(method_name="SetRelayState", payload="OFF")
        registry_manager.invoke_device_method(device_id, method_payload)
        
        return func.HttpResponse("Đã gửi lệnh TẮT xuống thiết bị thành công!", status_code=200)
    except Exception as e:
        logging.error(f"Lỗi khi gửi lệnh: {str(e)}")
        return func.HttpResponse("Gửi lệnh thất bại.", status_code=500)