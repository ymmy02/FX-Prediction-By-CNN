from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
import pandas as pd
from oanda_config import ACCOUNT_NUMBER, ACCESS_TOKEN

def get_exrate_as_df(instrument='EUR_USD', granularity='D',
        from_=None, to='2019-03-01', count=100):
    if from_ is None:
        params = {
                'granularity': granularity,
                'to': to,
                'count': count,
                }
    else:
        params = {
                'granularity': granularity,
                'from': from_,
                'to': to,
                }
    api = API(access_token=ACCESS_TOKEN)
    r = instruments.InstrumentsCandles(instrument=instrument, params=params)
    api.request(r)
    data = []
    for row in r.response['candles']:
        data.append([row['time'], row['mid']['o'], row['mid']['h'], row['mid']['l'], row['mid']['c'], row['volume']])
    df = pd.DataFrame(data)
    df.columns = ['time', 'open', 'high', 'low', 'close', 'volume']
    df = df.set_index('time')
    df.index = pd.to_datetime(df.index)
    df = df.astype(float)

    return df

def get_exrate_USD(pair='EUR', granularity='D',
        to='2019-03-01', count=100):
    try:
        df = get_exrate_as_df(instrument=pair+'_USD', granularity=granularity, to=to, count=count)
        return df
    except:
        df = get_exrate_as_df(instrument='USD_'+pair, granularity=granularity, to=to, count=count)
        return 1/df

