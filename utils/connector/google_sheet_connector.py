
import pygsheets
import pandas as pd
#authorization




class GoogleSheetConnector:
    def __init__(self):
        self.sheet_name = 'Sheet1'
        self.gc = pygsheets.authorize()

    def write_time(self, time: str, index: int):
        '''
        Will get google sheet
        :return:
        '''
        df = pd.DataFrame()
        df['time'] = [time]
        sh = self.gc.open('strasidla')
        wks = sh[0]
        wks.update_value(addr=f'B{index}', val=time)
        wks.set_dataframe(df, (2, index))

    def get_records(self,sheet_instance):
        records_data = sheet_instance.get_all_records()

        # view the data
        print(records_data)
        return records_data

if __name__ == "__main__":
    connector = GoogleSheetConnector()
    connector.write_time('test', 1)
