from spyre import server
import pandas as pd
import urllib.request
from datetime import datetime
import os
import matplotlib.pyplot as plt

def change_index(index):
    if index == 1:
        return 22
    elif index == 2:
        return 24
    elif index == 3:
        return 23
    elif index == 4:
        return 25
    elif index == 5:
        return 3
    elif index == 6:
        return 4
    elif index == 7:
        return 8
    elif index == 8:
        return 19
    elif index == 9:
        return 20
    elif index == 10:
        return 21
    elif index == 11:
        return 9
    elif index == 12:
        return 26
    elif index == 13:
        return 10
    elif index == 14:
        return 11
    elif index == 15:
        return 12
    elif index == 16:
        return 13
    elif index == 17:
        return 14
    elif index == 18:
        return 15
    elif index == 19:
        return 16
    elif index == 20:
        return 27
    elif index == 21:
        return 17
    elif index == 22:
        return 18
    elif index == 23:
        return 6
    elif index == 24:
        return 1
    elif index == 25:
        return 2
    elif index == 26:
        return 7
    elif index == 27:
        return 5

now = datetime.now()
date_and_time = now.strftime("%d%m%Y%H%M%S")

for i in range(1,28):
    url='https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={}&year1=1981&year2=2020&type=Mean'.format(i) 
    vhi_url = urllib.request.urlopen(url)
    text = vhi_url.read()
    out = open(str(change_index(i))+'_'+date_and_time+'.csv','wb')
    text = '\n'.join(text.decode().split("\n")[1:]).replace("<tt><pre>", '').replace("<br>", '').replace("</pre></tt>", '').replace(",", ';').encode()
    out.write(text)
    out.close()
indexes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
def get_dataframes(region_index):
    df = pd.read_csv(f'{region_index}_{date_and_time}.csv', sep=';', index_col=False)
    df.columns = df.columns.str.replace(' ', '')
    df = df.drop(df.loc[df['VHI'] == -1].index)
    return df

def year_week(df, year, week):
    return df[(df['year'] == year)&(df['week'] == week)]

def selected_date(df, params):
    year1 = params["year1"]
    year2 = params["year2"]
    week1 = params["week1"]
    week2 = params["week2"]
    first_date = year_week(df, year1, week1).index[0]
    second_date = year_week(df, year2, week2).index[0]
    return df.iloc[first_date:second_date]
    
class StockExample(server.App):
    title = "NOAA data vizualization"

    inputs = [{"type":'dropdown',
               "label": 'NOAA data dropdown',
               "options" : [ {"label": "VCI", "value":"VCI"},
                             {"label": "TCI", "value":"TCI"},
                             {"label": "VHI", "value":"VHI"}],
               "key": 'coef',
               "action_id": "update_data"},
              {"type":'dropdown',
               "label": 'Регіон',
               "options" : [ {"label": "АР Крим", "value":"4"},
                             {"label": "Вінницька", "value":"24"},
                             {"label": "Волинська", "value":"25"},
                             {"label": "Дніпропетровська", "value":"5"},
                             {"label": "Донецька", "value":"6"},
                             {"label": "Житомирська", "value":"27"},
                             {"label": "Закарпатська", "value":"23"},
                             {"label": "Запорізька", "value":"26"},
                             {"label": "Івано-Франкікська", "value":"7"},
                             {"label": "Київська", "value":"9"},
                             {"label": "Киів", "value":"12"},
                             {"label": "Кіровоградська", "value":"13"},
                             {"label": "Луганська", "value":"14"},
                             {"label": "Львівська", "value":"15"},
                             {"label": "Миколаївська", "value":"16"},
                             {"label": "Одеська", "value":"17"},
                             {"label": "Полтавська", "value":"18"},
                             {"label": "Рівненська", "value":"19"},
                             {"label": "Севастополь", "value":"20"},
                             {"label": "Сумська", "value":"21"},
                             {"label": "Тернопільська", "value":"22"},
                             {"label": "Харківська", "value":"8"},
                             {"label": "Херсонська", "value":"9"},
                             {"label": "Хмельницька", "value":"10"},
                             {"label": "Черкаська", "value":"1"},
                             {"label": "Чернівецька", "value":"3"},
                             {"label": "Чернігівська", "value":"2"}],
               "key": 'region',
               "action_id": "update_data"},
              {"type": 'slider',
               "label": 'Year 1',
               "min": 1982, "max": 2020, "value": 1982,
               "key": 'year1',
               "action_id": 'update_data'},
              {"type": 'slider',
               "label": 'Year 2',
               "min": 1982, "max": 2020, "value": 2018,
               "key": 'year2',
               "action_id": 'update_data'},
              {"type": 'slider',
               "label": 'Week 1',
               "min": 1, "max": 51, "value": 10,
               "key": 'week1',
               "action_id": 'update_data'},
              {"type": 'slider',
               "label": 'Week 2',
               "min": 1, "max": 51, "value": 35,
               "key": 'week2',
               "action_id": 'update_data'}]
                       
                      
    controls = [{"type" : "hidden",
                 "id" : "update_data"}]

    tabs = ["Plot", "Table"]

    outputs = [
        {"type": "plot",
         "id" : "plot",
         "control_id" : "update_data",
         "tab" : "Plot"},
        {"type": "table",
         "id": "table_id",
         "control_id": "update_data",
         "tab": "Table",
         "on_page_load": True}]

    

    def getData(self, params):
        df = get_dataframes(params['region'])
        return selected_date(df, params)

    def getPlot(self, params):
        df = self.getData(params)
        plt_obj = df.plot(y=params['coef'], color="g")
        plt_obj.set_title(params['coef'])
        plt_obj.set_ylabel(params['coef'])
        plt_obj.set_xlabel("weeks")
        plt_obj.grid()
        fig = plt_obj.get_figure()
        return fig

app = StockExample()
app.launch()
