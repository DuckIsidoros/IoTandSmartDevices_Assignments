import azure.functions as func
import logging

# Khởi tạo Function App
app = func.FunctionApp()

# 1. Thiết lập Trigger từ Event Hub
@app.event_hub_message_trigger(
    arg_name="azeventhub", 
    event_hub_name="telementary-hub", # My even hub name inside namespace
    connection="MyEventHubConn"   # Tên biến trong local.settings.json
) 
# Set up the output
@app.blob_output(
    arg_name="outputBlob",
    path="telemetry/{rand-guid}.json", 
    connection="AzureWebJobsStorage"   # This is variable in my local.settings.json.
)
def ProcessSensorData(azeventhub: func.EventHubEvent, outputBlob: func.Out[str]):
    # Read the raw data from Evet Hub:
    body = azeventhub.get_body().decode('utf-8')
    logging.info(f"Đã nhận dữ liệu từ Event Hub: {body}")

    # Write data to Blob Storage:
    outputBlob.set(body)
    
    logging.info("Giao dịch thành công: Dữ liệu đã được lưu vào Blob Storage.")