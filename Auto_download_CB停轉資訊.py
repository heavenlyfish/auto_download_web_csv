import requests
import pandas as pd
import csv
from datetime import datetime, date
from bs4 import BeautifulSoup
import os
#library for processing csv file from url
import urllib.request

url='https://www.tpex.org.tw/web/bond/tradeinfo/cb/CBSuspend.php?l=zh-tw'
host_url = 'www.tpex.org.tw'
payload = {
    'inputY':'2023',
    'inputM':'1',
    }
headers = {
    'Content-Type':'application/x-www-form-urlencoded',
    'Host':'www.tpex.org.tw',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }

response = requests.post(url,data=payload,headers=headers)
soup=BeautifulSoup(response.content, 'html.parser')

#print(soup.prettify())

lsts = []
results = soup.tbody.find_all("tr")
for result in results:
    #print(result)
    date = result.td.text.replace((result.td.text[0:3]),str(int(result.td.text[0:3])+1911))
    date_formated = datetime.strptime(date, '%Y/%m/%d').strftime("%Y-%m-%d")
    xls_link = "https://" + host_url + result.find("a",{'class':'btn btn-xls'})['href']
    csv_link = "https://" + host_url + result.find("a",{'class':'btn btn-csv'})['href']
    lsts.append((date_formated, xls_link, csv_link))

#create dataframe from list / Practice access datavalue
#REF:https://sparkbyexamples.com/pandas/get-first-row-of-pandas-dataframe/
df = pd.DataFrame(lsts, columns = ['DATE','XLS-LINK','CSV-LINK'])
#print(df.iloc[0]) #get first row
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

filePath = "CB????????????/CB????????????-" + df['DATE'].iloc[0] + '.csv'
print(filePath)

def check_File_Exist():
    if os.path.exists(filePath):
        print(filePath + " File exists.Dont Create File")
        return
    
    print('File not exists. create file: ' + filePath)
    #print(df['CSV-LINK'].iloc[0])
    #use urllib.request & csv module to read and save csv files
    req = urllib.request.urlopen(df['CSV-LINK'].iloc[0])
    csv_reader = csv.reader(req.read().decode('big5').splitlines())
    lists_of_csv = list(csv_reader)

    #['HEADER', '????????????', '????????????', '?????????(???)?????????', '?????????(???)?????????', '?????????(???)?????????']
    list2df = []
    for list_of_csv in lists_of_csv:
        if len(list_of_csv) > 0:
            if list_of_csv[0] == "BODY" :
                #print(list_of_csv)
                list2df.append((list_of_csv[1],list_of_csv[2],list_of_csv[3],list_of_csv[4],list_of_csv[5]))
    
    Data_In_DF = pd.DataFrame(list2df,columns=['????????????', '????????????', '?????????(???)?????????', '?????????(???)?????????', '?????????(???)?????????'])
    #print(Data_In_DF)

    Data_In_DF.to_csv(filePath, index=False, encoding='big5') 
    

check_File_Exist()