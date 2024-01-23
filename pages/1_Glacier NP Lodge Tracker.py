import requests
import json
import pandas as pd
from datetime import datetime
import streamlit as st

st.set_page_config(
    page_title="Glacier NP Lodge",
    layout='wide'
)

st.write("""
# Glacier National Park Lodge Tracker - 2024         
""")


HOTEL_CODES = {"GLCC": "Cedar Creek Lodge",
               "GLLM": "Lake McDonald",
               "GLMG": "Many Glaciers",
               "GLRS": "Rising Sun",
               "GLSC": "Swiftcurrent",
               "GLVI": "Village Inn at Apgar"}

list_properties = ["GLLM", "GLMG", "GLRS", "GLSC"]
list_start_dates = ["06/01/2024", "07/01/2024", "08/01/2024", "09/01/2024", "10/01/2024"]


# function to get availability of glaciner national park lodges
def get_glacierNP_lodge_ava(starting_date, limit=31):
    """
    

    Parameters
    ----------
    starting_date : string
        mm/dd/yyyy
    limit : int, optional
        The default is 31

    Returns
    -------
    json for avai
        0 if request is not successful.

    """
    
    payload={
        "date": starting_date,
        "limit": limit,
        "is_group": False
        }
    
    url = "https://webapi.xanterra.net/v1/api/availability/hotels/glaciernationalparklodges"
    res = requests.get(url, payload)
    
    if res.status_code == 200:
        st.write(f"Request was successful for {starting_date}")
        return json.loads(res.text)["availability"]
    else:
        st.write(f"Request was not successful! for {starting_date}")
        return 0
    

def process_ava_results(ava, list_properties):
    res = []
    list_dates = list(ava.keys())
    for date in list_dates:
        for hotel in list_properties:
            if ava[date][hotel]["min"] > 0.1:
                res.append([date, HOTEL_CODES[hotel], ava[date][hotel]['min'], ava[date][hotel]['max']])
    return res
        
        

res = []
for date in list_start_dates:
    Ava = get_glacierNP_lodge_ava(date)
    if Ava != 0:
        res += process_ava_results(Ava, list_properties)

df = pd.DataFrame(res, columns=['date', 'hotel', 'min_price', 'max_price'])
df['day_of_week'] = df.apply(lambda x: datetime.strptime(x['date'], '%m/%d/%Y').strftime('%a'), 
                             axis = 1)

dfPivot = df.pivot_table(index=['date', 'day_of_week'], 
                         columns='hotel', 
                         values='min_price',
                         aggfunc='min')
dfPivot.reset_index(inplace=True)

st.write("## Availability with the Min. Price")
st.dataframe(dfPivot, hide_index=True)


link_to_book = "https://secure.glaciernationalparklodges.com/booking/lodging"
st.write("## Use this [link](%s) to book a room!" % link_to_book)