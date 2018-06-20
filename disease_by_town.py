import pyodbc
import pandas as pd
import arcpy
import csv
import os
import numpy
import string
from pandas import DataFrame

####use pyodbc to access tF45DFhe sql server
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=UMWWSCDRDB01;DATABASE=rdcDT20160401001_Build86Final;UID=cdr;PWD=cdr001*')
cursor = cnxn.cursor()
icd1 = open("D:\QimingShi\csv_files\mockicd9.txt","r")
city = open("D:\QimingShi\csv_files\city.txt","r")
diseaselist = []
citylist = []
for city in city.readlines():
    citylist.append(city[:-1])
for line in icd1.readlines():
    diseaselist.append(line[:-1])

####creat the dataframe
df = pd.DataFrame(index = citylist, columns = diseaselist)

for element in citylist:

    for ele in diseaselist:
        # print ele[:-1]
        ###Sql query part
        cursor.execute("SELECT count(distinct r.[ptid])\
        ,r.[icd9] as icd9\
        ,t.[city] as city\
          FROM [rdcDT20160401001_Build86Final].[dbo].[dtfactproblems] as r\
          inner join [rdcDT20160401001_Build86Final].[dbo].[DTPatients] as t\
          on r.ptid = t.ptid\
          where icd9 =\'"+ ele +"\'and city = \'"+ element +"\' and t.add1 NOT like '%BAD ADDRESS%'\
            group by city,icd9")
        rows = cursor.fetchall()
        if len(rows) > 0:
            df.set_value(element, ele, rows[0][0])
        else:
            df.set_value(element, ele, 0)
        # for row in rows:
        #     df.set_value(element,ele,row[0])

df.to_csv("D:\QimingShi\csv_files\panda_final.csv",sep="," )







        ###use package csv to write the csv file
    # with open('D:\QimingShi\csv_files\eggs.csv', 'wb') as csvfile:
    #     a = csv.writer(csvfile, delimiter=',')
    #     a.writerow(['ptid', 'icd9', 'streetaddress', 'city', 'zip', 'state'])
    #     for row in rows:
    #         a.writerow(row)












icd1.close()