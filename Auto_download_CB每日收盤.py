import requests
import pandas as pd
import csv
from datetime import datetime, date
import time
from bs4 import BeautifulSoup
import os
#library for processing csv file from url
import urllib.request
#remove nontext elements from string
import re

today = date.today()
Year = str(today.year)
Month = str(today.month)

# url='https://www.tpex.org.tw/web/bond/tradeinfo/cb/CBSuspend.php?l=zh-tw'
url = 'https://www.tpex.org.tw/web/bond/tradeinfo/cb/CBDaily.php?l=zh-tw'
host_url = 'www.tpex.org.tw'
payload = {
    'inputY':Year,#'2023',
    'inputM':Month,#'1',
    }
headers = {
    'Content-Type':'application/x-www-form-urlencoded',
    'Host':'www.tpex.org.tw',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }

response = requests.get(url,headers=headers)
soup=BeautifulSoup(response.content, 'html.parser')

#print(soup.prettify())

lsts = []
results = soup.tbody.find_all("td")
for result in results:
    #Obtain Date value and format to 2023-01-30
    if len(result.text)==9:
        date = result.text.replace(result.text[0:3], str(int(result.text[0:3])+1911))
        date_formated = datetime.strptime(date, '%Y/%m/%d').strftime("%Y-%m-%d")
        #print(date_formated)
    #Obtain Link to the file
    if len(result("a")) ==1:
        link= "https://" + host_url + result.a['href']
        #print(link)
        lsts.append((date_formated, link))
#test result
#print(lsts[0][0], lsts[0][1])


#create dataframe from list / Practice access datavalue
#REF:https://sparkbyexamples.com/pandas/get-first-row-of-pandas-dataframe/
# df = pd.DataFrame(lsts, columns = ['DATE','XLS-LINK','CSV-LINK'])
# df = pd.DataFrame(lsts, columns = ['Bond Code', 'Short Name', 'Issuer', 'Issuing Date', 'Maturity Date', 'Tenor', 'Issue Amount', 'Bond Database'])
# print(df)
#print(df.iloc[0].tolist()) #test printouts
#print(df['Short_Name']) #get first row
#print(df.iloc[:1]) #get first row using range index
# print(df['DATE'].iloc[0]) #get first row value using particular coln
# print(df['DATE']).iloc[:1] #get first row value using index range
# print(df.loc[df.index[0]]) #Get first row using index
# print(df.values[:1]) #Get first row using values[]
# print(df.['DATES'].value[:1]) #Get first row of particular column
# print(df.head(1)) #Get the first row use head()
# print(df.iloc[0].tolist())  #Get the first row of DataFrame as a list
#locate first element from dataframe
#print(lsts[0][0]) #Locate Date element
#print(lsts[0][1]) #Locate xls_link element
#print(lsts[0][2]) #Locate csv_link element

#-----------------------------------------------
#Check if file with latest date exist
#if not exist, create new csv file
#if exist, exit

#Locate current file directory
#print(os.getcwd())
#print(str(today))
##print(lsts[0][0])
print(lsts[0][1])
filePath = "CB每日收盤/rsta0113_" + lsts[0][0] + '.csv'
print(os.getcwd(), filePath)

def check_File_Exist():
    if os.path.exists(filePath):
        print(filePath + " File exists. Dont Create File")
        return
    print('File not exists. create file: ' + filePath)
    #use urllib.request & csv module to read and save csv files
    #print("create file from " + lsts[0][1])
    #req = urllib.request.urlopen(lsts[0][1])
    #csv_reader = csv.reader(req.read().decode('cp950').splitlines()) #big5 doesn't work, use cp950
    # lists_of_csv = list(csv_reader)
    #print(lists_of_csv[:5])

    #create file using io module
    req = requests.get(lsts[0][1],data=payload, headers=headers)
    url_content = req.content

    csv_file = open(filePath, 'wb')
    csv_file.write(url_content)
    csv_file.close
    # print(filePath + 'Done')

    #['HEADER', '代號', '名稱', '交易', '收市', '漲跌', '開市', '最高', '最低', '筆數', '單位', '金額', '均價', '明日參價', '明日漲停', '明日跌停']
    #   0          1       2      3       4      5       6       7      8      9       10      11      12       13          14         15
    # list2df = []
    # for list_of_csv in lists_of_csv:
    #     #remove any non item blanks
    #     if len(list_of_csv) > 0:
    #         #filter out only body items
    #         if list_of_csv[0] == "BODY" :
    #             #移除 議價資料 ＋ 合計
    #             if len(list_of_csv[1]) > 4 :
    #                 #print(list_of_csv)
    #                 list2df.append((list_of_csv[1],list_of_csv[2],list_of_csv[4],list_of_csv[4],list_of_csv[5]))
#     Data_In_DF = pd.DataFrame(list2df,columns=['債券代碼', '債券簡稱', '停止轉(交)換起日', '停止轉(交)換迄日', '停止轉(交)換事由'])   
#   Data_In_DF = pd.DataFrame(df,columns=['Bond_Code', 'Short_Name','Issuer','Issuing_Date','Maturity_Date','Tenor','Issue_Amt','Bond_Database'])
    # Data_In_DF = pd.DataFrame(df)
    #print(Data_In_DF)
#     Data_In_DF.to_csv(filePath, index=False, encoding='utf-8-sig') 
    
check_File_Exist()