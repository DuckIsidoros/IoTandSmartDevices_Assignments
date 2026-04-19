import azure.functions as func
import logging
import json
import os
import requests

app = func.FunctionApp()

@app.function_name(name="GeofenceTrigger")
@app.event_hub_message_trigger(arg_name="events", 
                               event_hub_name="telementary-hub",
                               connection="IoTHubConnectionString",
                               consumer_group="geofence",
                               cardinality="many")
@app.twilio_sms_output(arg_name="sendSms",
                       account_sid_setting="TwilioAccountSid",
                       auth_token_setting="TwilioAuthToken",
                       from_number="%TwilioPhoneNumber%")
def main(events: list[func.EventHubEvent], sendSms: func.Out[str]):
    maps_key = os.environ.get('MAPS_KEY')
    geofence_udid = os.environ.get('GEOFENCE_UDID')
    my_phone = os.environ.get('MyPhoneNumber')
    
    url = 'https://atlas.microsoft.com/spatial/geofence/json'

    for event in events:
        try:
            body = json.loads(event.get_body().decode('utf-8'))
            if 'gps' not in body: 
                continue 

            lat = body['gps']['lat']
            lon = body['gps']['lon']

            params = {
                'api-version': '1.0',
                'deviceId': 'gps-sensor',
                'subscription-key': maps_key,
                'udid': geofence_udid,
                'lat': lat,
                'lon': lon
            }

            # Call API Azure Maps.
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                distance = result['geometries'][0]['distance']
                
                if distance <= 0:
                    sms_payload = {
                        "body": f"The vehicle has entered the geofence! (Dist: {distance}m)", 
                        "to": my_phone
                    }
                    sendSms.set(json.dumps(sms_payload))
                    logging.info(f"SMS Sent for device inside geofence.")
            else:
                logging.warning(f"Azure Maps API returned status: {response.status_code}")
            
        except requests.exceptions.Timeout:
            logging.error("Request to Azure Maps API timed out.")
        except Exception as e:
            logging.error(f"Error processing event: {e}")