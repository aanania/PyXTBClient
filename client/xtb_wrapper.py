import sys
sys.path.append("/projects/PyXTBClient/") # go to parent dir
import client.xtb_client as xtb_client
import client.constants as xtb_constants
import yaml
from datetime import datetime
import pandas as pd

class XTBClientWrapper:
    
    def __init__(self, host='xapi.xtb.com', port=5112, stream_port=5113):
        
        self.client = xtb_client.XTBClient(host=host, port=port, stream_port=stream_port)
        self.user_id = ''
        self.password = ''
        
    def load_configuration(self, configuration_file='../configuration/config.yml'):

        with open(configuration_file) as file:
            user_yml = yaml.safe_load(file)
            self.user_id = user_yml['user_id']
            self.password = user_yml['password']
            
    def login(self):
        self.client.login(self.user_id, self.password)
        
    def get_data_symbol(self, symbol, start, end, period=xtb_constants.Period.h1):
        """Get data in Pandas format from XTB
        
        :param symbol: Symbol name
        :type symbol: String
        :param start: Start time 
        :type start: Datetime
        :param end: End time
        :type end: Datetime
        :param period: Period, defaults to constants.Period.h1
        :type period: Period from constants.Period, optional
        :return: Data for a specific symbol from Start to End
        :rtype: Dataframe
        """

        start = datetime.timestamp(start)*1000
        end = datetime.timestamp(end)*1000
        data = self.client.get_chart_range_request(symbol='US500', start=start, end=end, period=period)

        df = pd.DataFrame(columns=["open", "close", "high", "low", "datetime"])
        for i in data:
            df = df.append({'open': i.open, 'close': i.close, 'high': i.high, 'low': i.low
                        , 'datetime': i.ctm/1000.
            }, ignore_index=True)
        df['datetime'] = pd.to_datetime(df['datetime'], unit='s')
        df.set_index(keys='datetime', inplace=True)
        
        return df