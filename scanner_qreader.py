from google_sheet_connector import GoogleSheetConnector
from datetime import datetime
#import timedelta
from datetime import timedelta
from jke_reader import QReader
import re
import os
import cv2
import numpy as np
import streamlit as st
import time
import random
class QRCodeScanner:
    def __init__(self):
        self.sheet_connector = GoogleSheetConnector()
        self.qreader = QReader(model_size='n')

    def write_time(self, data):
        try:
            if not str(data).startswith("StrasidlaHlidka:"):
                st.write("Naskenovany kod neni spravny, zkus to znovu")
                return False
            st.write(data)
            index = str(data).replace("StrasidlaHlidka:", "")
            # keep only number in index - use regex /d
            regex = re.compile(r'\d+')
            index = regex.findall(index)[0]

            #get local time
            current_time = datetime.utcnow()
            current_time = current_time + timedelta(hours=1)
            current_time = current_time.strftime("%H:%M:%S")

            current_time = datetime.now().strftime("%H:%M:%S")
            self.sheet_connector.write_time(current_time, int(index))
            st.write(f"Cas dobehnuti: {current_time}")
        except Exception as e:
            st.write("Neco se pokazilo, zkus to znovu")
            st.write(e)


    def scan_qr_photo(self):
        #sleep(5)
        time.sleep(5)
        #generate random number with four digits

        number = str(random.randint(1000, 9999))


        image = st.camera_input("Show QR code")
        if image is not None:


            bytes_data = image.getvalue()

            #save image
            with open(f"image_{number}.png", 'wb') as f:
                f.write(bytes_data)
            img = cv2.cvtColor(cv2.imread(f"image_{number}.png"), cv2.COLOR_BGR2RGB)
            data = self.qreader.detect_and_decode(image=img)

            data = data[0]
            if data !="" or data is not None:

                print(f"code:{data}.code")
                st.write("Naskenovaná hlídka:")
                #remove image

                st.write(data)
                self.write_time(data)

            os.remove(f"image_{number}.png")
    def run_scanner(self):

        self.scan_qr_photo()




if __name__ == "__main__":
    QRCodeScanner().run_scanner()