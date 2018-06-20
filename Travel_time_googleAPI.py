import googlemaps
import pandas as pd
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyDXd0xY7sgxkj5Mn-z7Tyi5whj3C8zgWIo')
xl = pd.ExcelFile("C:\Users\shiq\Desktop\patients_add.xlsx")
df = xl.parse("Sheet1")

time = []
distance = []

i=0
for row in range(len(df['latlong'])):
    now = datetime.now()
    i=i+1
    directions_result = gmaps.directions(df.at[row,'latlong'],
                                        "42.273064, -71.791284",
                                        mode="driving",
                                        avoid="ferries",
                                        departure_time=now
                                        )


    time.append(directions_result[0]['legs'][0]['duration']['text'])
    distance.append(directions_result[0]['legs'][0]['distance']['text'])
    print i

df['TIME'] = pd.Series(time, index=df.index)
df['DISTANCE'] = pd.Series(distance, index=df.index)
writer = pd.ExcelWriter('C:\Users\shiq\Desktop\output_distance1.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()
print time, distance, df
