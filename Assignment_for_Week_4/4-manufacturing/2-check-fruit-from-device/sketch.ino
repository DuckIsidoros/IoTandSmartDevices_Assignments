#include <Arduino.h>
#include <ArduinoJson.h> 

const int LED_PIN = LED_BUILTIN; 

// I'll assume that this is the returned data from the API.
String mockJsonResponse = "{\"id\":\"12345\",\"project\":\"abcde\",\"iteration\":\"1\",\"created\":\"2026-04-26T00:00:00.000Z\",\"predictions\":[{\"probability\":0.98,\"tagId\":\"111\",\"tagName\":\"Unripe Mango\"},{\"probability\":0.02,\"tagId\":\"222\",\"tagName\":\"Ripe Mango\"}]}";

void setup() {
    Serial.begin(115200);
    pinMode(LED_PIN, OUTPUT);
    digitalWrite(LED_PIN, LOW); 

    while (!Serial) {
        delay(10);
    }
    
    Serial.println("\n--- BẮT ĐẦU XỬ LÝ TÍN HIỆU ---");
    
    respondToPrediction(mockJsonResponse);
}

void loop() {
}

void respondToPrediction(String jsonString) {
    // 1. I'll analyze the JSON.
    DynamicJsonDocument doc(1024);
    DeserializationError error = deserializeJson(doc, jsonString);

    if (error) {
        Serial.print("Lỗi phân tích JSON: ");
        Serial.println(error.c_str());
        return;
    }

    // I'll extract the label that has the highest probability.
    String topTag = doc["predictions"][0]["tagName"].as<String>();
    float topProb = doc["predictions"][0]["probability"].as<float>();

    Serial.print("Label: ");
    Serial.print(topTag);
    Serial.print("(Probability: ");
    Serial.print(topProb * 100);
    Serial.println("%)");

    // I'll set that the LED will be turned on if the fruit is unripe.
    // The LED will be turned off if the fruit is ripe.
    if (topTag.indexOf("Unripe") != -1) {
        Serial.println("Turn on the LED");
        digitalWrite(LED_PIN, HIGH);
    } 
    else if (topTag.indexOf("Ripe") != -1) {
        Serial.println("Turn off the LED");
        digitalWrite(LED_PIN, LOW); 
    }
}