import os
import azure.functions as func
import logging
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod

app = func.FunctionApp()

# Relay on Function
@app.route(route="relay_on", auth_level=func.AuthLevel.ANONYMOUS)
def TurnRelayOn(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Successfully receive! Request to TURN ON relay via HTTP.')
    
    try:
        conn_str = os.environ["IOT_HUB_CONNECTION_STRING"]
        device_id = os.environ["TARGET_DEVICE_ID"]
        
        registry_manager = IoTHubRegistryManager(conn_str)
        
        method_payload = CloudToDeviceMethod(method_name="SetRelayState", payload="ON")
        
        # Send the command
        registry_manager.invoke_device_method(device_id, method_payload)
        
        return func.HttpResponse("Successfully sent command to turn ON relay!", status_code=200)
    except Exception as e:
        logging.error(f"Error occurred while sending command: {str(e)}")
        return func.HttpResponse("Failed to send command.", status_code=500)

# Relay Off Function
@app.route(route="relay_off", auth_level=func.AuthLevel.ANONYMOUS)
def TurnRelayOff(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Successfully received request to TURN OFF relay via HTTP.')
    
    try:
        conn_str = os.environ["IOT_HUB_CONNECTION_STRING"]
        device_id = os.environ["TARGET_DEVICE_ID"]
        
        registry_manager = IoTHubRegistryManager(conn_str)
        method_payload = CloudToDeviceMethod(method_name="SetRelayState", payload="OFF")
        registry_manager.invoke_device_method(device_id, method_payload)
        
        return func.HttpResponse("Successfully sent command to turn OFF relay!", status_code=200)
    except Exception as e:
        logging.error(f"Error occurred while sending command: {str(e)}")
        return func.HttpResponse("Failed to send command.", status_code=500)