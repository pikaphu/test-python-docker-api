from flask import Flask
import pandas as pd 
from datetime import datetime
import re

app = Flask(__name__)
# FLASK_APP = program.py # if file name is program.py
@app.route("/")
def home():
    return "Hello, Flask! 5000 Hot Reload"

@app.route("/hello/<name>/<no>/<yes>")
def hello_there(name,no,yes):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")
    match_object = re.match("[a-zA-Z]+", name)
    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"
    content = "Hello there, " + no + yes + clean_name + "! It's " + formatted_now
    return content
    
@app.route("/price/<origin>/<destin>/<truck>")
def price_analyse(origin,destin,truck):
    file_name = "OrderReport360.xlsx"
    df = pd.read_excel("OrderReport360.xlsx")
    pd.set_option('display.max_rows', df.shape[0]+1)

    data_list = []
    data_id = []
    data_order_id = []
    data_confirm = []
    data_status = []
    data_origin = []
    data_destination = []
    data_distance = []
    data_truck_type = []
    data_price = []

    for i in range(len(df)):
        if df.loc[i,"Confirm"] == "คอนเฟิร์มแล้ว" and df.loc[i,"Status"] != "งานถูกยกเลิก":
            data_id.append(i)
            data_order_id.append(df.loc[i,"OrderID"])
            data_confirm.append(df.loc[i,"Confirm"])
            data_status.append(df.loc[i,"Status"])
            data_origin.append(df.loc[i,"OriginShortName"])
            data_destination.append(df.loc[i,"DestinationShortName"])
            data_distance.append(df.loc[i,"Distance"])
            data_truck_type.append(df.loc[i,"TruckTypeName"])
            data_price.append(df.loc[i,"ShipperPrice"])

    data = {
        "ID": data_id,
        "OrderID": data_order_id,
        "Confirm": data_confirm,
        "Status": data_status,
        "Origin": data_origin,
        "Destination": data_destination,
        "Distance": data_distance,
        "TruckType": data_truck_type,
        "Price": data_price
    }

    dummy_list = []
    clean_origin = []
    for pv in data["Origin"]:
        if "." in pv:
            dummy_list = pv.split(".")
            clean_origin.append(dummy_list[-1])
        elif " " in pv:
            dummy_list = pv.split(" ")
            clean_origin.append(dummy_list[-1])
        elif "," in pv:
            dummy_list = pv.split(",")
            clean_origin.append(dummy_list[-1])
        else:
            clean_origin.append(pv)

    data["Origin"] = clean_origin

    clean_des = []
    for pv in data["Destination"]:
        if "." in pv:
            dummy_list = pv.split(".")
            clean_des.append(dummy_list[-1])
        elif " " in pv:
            dummy_list = pv.split(" ")
            clean_des.append(dummy_list[-1])
        elif "," in pv:
            dummy_list = pv.split(",")
            clean_des.append(dummy_list[-1])
        else:
            clean_des.append(pv)

    data["Destination"] = clean_des

    data_frame = pd.DataFrame(data, columns=["ID","OrderID","Confirm","Status","Origin","Destination","Distance","TruckType","Price"])

    origin_group = data_frame["Origin"].value_counts()

    destination_group = data_frame["Destination"].value_counts()

    truck_group = data_frame["TruckType"].value_counts()

    price_group = data_frame["Price"].value_counts()
    df_uq = data_frame.drop_duplicates("OrderID")

    # input_origin = "ชุมพร"
    # input_des = "กรุงเทพมหานคร"
    # input_truck = "4 ล้อ ตู้ทึบ"

    origin_row = []
    # def my_func(a_ori,a_des,a_truck):
    #     origin_row = df_uq[df_uq.Origin == a_ori]
    #     des_row = origin_row[origin_row.Destination == a_des]
    #     truck_row = des_row[des_row.TruckType == a_truck]
    #     return (truck_row['Price'].describe())
    # print(df_uq.groupby(['Origin', 'Destination','TruckType'])['Price'].count())
    # print(df_uq.groupby(['Origin', 'Destination','TruckType'])['Price'].min())
    # print(df_uq.groupby(['Origin', 'Destination','TruckType'])['Price'].max())
    # print(df_uq.groupby(['Origin', 'Destination','TruckType'])['Price'].mean())
    # print(df_uq.groupby(['Origin', 'Destination','TruckType'])['Price'].describe())

        # def my_func(a_ori,a_des,a_truck):
    origin_row = df_uq[df_uq.Origin == origin]
    des_row = origin_row[origin_row.Destination == destin]
    truck_row = des_row[des_row.TruckType == truck]
    maxx = truck_row['Price'].max()
    # return ("ราคา" + truck_row['Price'].describe())
    # return str(truck_row['Price'].mean())
    return str(maxx)
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int("5000")) # remember to set debug to False