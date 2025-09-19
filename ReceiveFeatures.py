import paho.mqtt.client as mqtt
import json
import time

import cv2
import numpy as np


class ReceiveFeatures:
    def __init__(self, broker="localhost", port=1884, topic="tomass/save_features"):

        self.topic = topic
        self.queue = []  # stores (track_id, bbox, timestamp, image_np)
        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.connected = False


        self.client.connect(broker, port, 60)
        self.client.loop_start()  # non-blocking

        self.queue = []  # stores (track_id, features)

        # Wait until connection is established
        timeout = time.time() + 5  # max 5 seconds wait
        while not self.connected:
            if time.time() > timeout:
                raise TimeoutError("MQTT connection timed out.")
            time.sleep(0.5)
        

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("[MQTT] Connected successfully")
            client.subscribe(self.topic)  # ← THIS WAS MISSING
            self.connected = True
        else:
            print(f"[MQTT] Connection failed with code {rc}\n")

    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode('utf-8'))
            image_np = self._decode_crop_np(payload["image"])
            self.queue.append({
                "track_id": payload["track_id"],
                "image": image_np,
                "cam_id": payload["cam_id"],
                "features": payload["features"]
            })

            print(f"[MQTT] Received {payload['track_id']} \n")
            return payload
        except Exception as e:
            print(f"[ERROR] Failed to process message: {e}\n")
            return None
        
    # this functionality stays during testing, remove during production
    def _decode_crop_np(self, encoded_crop):
        crop_bytes = bytes.fromhex(encoded_crop)
        np_arr = np.frombuffer(crop_bytes, dtype=np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Failed to decode image from base64")
        return image
        
    def get_pending_vectors(self):
        """Retrieve and clear the queue of received crops"""
        data = self.queue[:]
        self.queue.clear()
        return data




    