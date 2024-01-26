import streamlit as st 
import requests
import datetime
import pandas as pd
import json

st.set_page_config(
    page_title="WA State Park Camping",
    layout='wide'
)

st.write("""
# WA State Park Camp Site Availabilities    
""")

with open("src/WA_State_Park_MapId.json") as f:
    dict_map_ids = json.loads(f.read())

st.write("## Going to request for the state parks below: ")
st.write(list(dict_map_ids.values()))

def request_camp_site(map_id, start_date):
    url = "https://washington.goingtocamp.com/api/availability/map"
    j = {
        "mapId" : map_id,
        "bookingCategoryId": 0,
        "equipmentCategoryId":-32768,
        "subEquipmentCategoryId":-32766,
        "startDate":start_date.strftime("%Y-%m-%d"),
        "endDate":(start_date + datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
        "getDailyAvailability":"false",
        "isReserving":"true",
        "numEquipment":1,
        "partySize": 6
    }
    res = requests.get(url, data=j)
    if res.status_code != 200:
        st.write(f"😤 request for {dict_map_ids[map_id]} and {start_date} failed")
    else:
        st.write(f"😋 request for {dict_map_ids[map_id]} and {start_date} succeeded")
    return res



# get dates in a month
cur_date = datetime.datetime.now().date()
cur_weekday = cur_date.strftime('%a')

list_dates = []
list_weekdays = []

new_date = cur_date + datetime.timedelta(days=1)
while new_date <= cur_date + datetime.timedelta(days=14):
    new_weekday = new_date.strftime('%a')
    if new_weekday in ['Fri', 'Sat']:
        list_dates.append(new_date)
        list_weekdays.append(new_weekday)
    new_date += datetime.timedelta(days=1)

st.write("## Going to request for the dates below: ")
st.write(list_dates)
# st.write(list_weekdays)

# request the availability for the list of dates and the selected state parks
list_ava = []
st.write("## Requests started:")
for date in list_dates:
    for key in dict_map_ids.keys():
        res = request_camp_site(map_id=key, start_date=date)
        res_j = json.loads(res.text)
        if 0 in res_j["mapAvailabilities"]:
            list_ava.append([date.strftime("%Y-%m-%d"), date.strftime("%a"), dict_map_ids[key]])


if len(list_ava) > 0:
    st.write("## Found some availabilities! 🥳")
    df_ava = pd.DataFrame(list_ava, columns=["date", "weekday", "park"])
    st.write(df_ava)
else:
    st.write("## Didn't find any availability! 😢")