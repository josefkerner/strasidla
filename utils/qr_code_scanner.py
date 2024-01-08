import streamlit as st
from utils.connector.google_sheet_connector import GoogleSheetConnector
from datetime import datetime
import cv2
import os, re

import streamlit as st

class QRCodeScanner:
    def __init__(self):
        self.sheet_connector = GoogleSheetConnector()
        #self.qreader = QReader()

    def write_time(self, data):
        try:
            if not str(data).startswith("StrasidlaHlidka:"):
                st.write("Naskenovany kod neni spravny, zkus to znovu")
                return
            index = str(data).replace("StrasidlaHlidka:", "")
            # keep only number in index - use regex /d
            regex = re.compile(r'\d+')
            index = regex.findall(index)[0]

            current_time = datetime.now().strftime("%H:%M:%S")
            self.sheet_connector.write_time(current_time, int(index))
            st.write(f"Cas dobehnuti: {current_time}")
        except Exception as e:
            st.write("Neco se pokazilo, zkus to znovu")
            st.write(e)


    def set_screener(self):
        # Create a QReader instance
        image = st.camera_input("Show QR code")

        cap = cv2.VideoCapture(0)
        decoder = cv2.QRCodeDetector()

        while True:
            _, img = cap.read()
            data, bbox, _ = decoder.detectAndDecode(img)
            # check if there is a QRCode in the image
            if data:

                '''
                bytes_data = image.getvalue()
                #save image
                with open('image.png', 'wb') as f:
                    f.write(bytes_data)
                image = cv2.cvtColor(cv2.imread("image.png"), cv2.COLOR_BGR2RGB)
                data = self.qreader.detect_and_decode(image=image)
                
                #cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
                #detector = cv2.QRCodeDetector()
                #data, bbox, straight_qrcode = detector.detectAndDecode(cv2_img)
                '''
                st.write("Naskenovaná hlídka:")
                #remove image


                st.write(data)
                self.write_time(data)

                #os.remove("image.png")
    def run_scanner(self):
        placeholder = st.empty()

        with placeholder.container():
            qr_code = self.set_screener()

        if qr_code is not None:
            print('QR code scanned')
            print(qr_code)
            st.write(qr_code)
            patrol = self.check_qr_code(qr_code=str(qr_code))
            if patrol is not None:
                patrol.end_time = datetime.now()
                self.session.commit()
            #reset streamlit screen
            placeholder.empty()


if __name__ == "__main__":
    QRCodeScanner().run_scanner()