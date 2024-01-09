import os

from streamlit_webrtc import webrtc_streamer
from google_sheet_connector import GoogleSheetConnector
import cv2
import numpy as np
import re
from datetime import datetime
import streamlit as st
import av
decoder = cv2.QRCodeDetector()
sheet_connector = GoogleSheetConnector()
from PIL import Image
from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = st.secrets['TWILIO_ACCOUNT_SID']
# Your Auth Token from twilio.com/console
auth_token = st.secrets['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)
token= client.tokens.create()



def scan_qr_code(img):
    data, bbox, straight_qrcode = decoder.detectAndDecode(img)
    return data, bbox

def write_time(data):
    try:
        if not str(data).startswith("StrasidlaHlidka:"):
            print("Naskenovany kod neni spravny, zkus to znovu")
            return False
        index = str(data).replace("StrasidlaHlidka:", "")
        # keep only number in index - use regex /d
        regex = re.compile(r'\d+')
        index = regex.findall(index)[0]

        current_time = datetime.now().strftime("%H:%M:%S")
        sheet_connector.write_time(current_time, int(index))
        return True
        #st.write(f"Cas dobehnuti: {current_time}")
    except Exception as e:
        return False

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    new_image = Image.fromarray(img)

    # make image green
    new_image = np.array(new_image)

    if img is not None:
        print(img.shape)

        data, bbox = scan_qr_code(img)
        if data:


            print("[+] QR Code detected, data:", data)

            if write_time(data):
                new_image[:, :, 1] = 255
                #write black text on image
                cv2.putText(new_image, f"{data}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    return av.VideoFrame.from_ndarray(new_image, format="bgr24")



rtc_configuration={  # Add this config
        "iceServers": token.ice_servers
}

webrtc_streamer(key="example", rtc_configuration=rtc_configuration,
            video_frame_callback=video_frame_callback,
                media_stream_constraints={"video": True, "audio": False}
                )