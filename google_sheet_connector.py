
import pygsheets
import pandas as pd
#authorization




class GoogleSheetConnector:
    def __init__(self):
        self.sheet_name = 'Sheet1'
        self.gc = pygsheets.authorize()
        sh = self.gc.open('strasidla')
        self.wks = sh[0]

    def write_time(self, time: str, index: int):
        '''
        Will get google sheet
        :return:
        '''
        df = pd.DataFrame()
        df['time'] = [time]

        self.wks.update_value(addr=f'B{index+1}', val=time)

    def get_records(self,sheet_instance):
        records_data = sheet_instance.get_all_records()

        # view the data
        print(records_data)
        return records_data
