import pandas as pd
import os
from pypdf import PdfReader 
from datetime import datetime,date

path = 'paymaker/input'
files = os.listdir(path)
i=0 
j=0
all_data = []
for items in files:
    i=i+1
    print(f"({i}) -> Found {items}")
    if items.endswith('.pdf'):
        j=j+1
        fullpath = os.path.join(path,items)
        reader = PdfReader(fullpath)   
        text = reader.pages[0].extract_text()
        print(text)
        # We start partitioning the pdf into csv
        # Index
        current_row = {"Curr. Item":j}
        # File Name
        current_row["filename"] = items
        #paydate
        if "PAY DATE:" in text:
            pay_date_val = text.split("PAY DATE:")[1].split()[0].strip()
            current_row["Pay Date"] = datetime.strptime(pay_date_val, "%m/%d/%Y").date()
        #work start
        if "Period Beginning" in text:
            datei_val = text.split("Period Beginning")[1].split()[0].strip()
            current_row["Start Date"] = datetime.strptime(datei_val, "%m/%d/%Y").date()
        #work end
        if "Period Ending:" in text:
            datef_val = text.split("Period Ending:")[1].split()[0].strip()
            current_row["End Date"] = datetime.strptime(datef_val, "%m/%d/%Y").date()
        #hours worked
        if "Regular Pay" in text:
            whours_val = text.split("Regular Pay")[1].split()[0].strip().replace(',', '')
            current_row["Hours Worked"] = float(whours_val)
        #pay/h
        if "Regular Pay" in text:
            payh_val = text.split("Regular Pay")[1].split()[1].strip().replace(',', '')
            current_row["Rate/H"] = float(payh_val)
        #grosspay
        if "Regular Pay" in text:
            gross_val = text.split("Regular Pay")[1].split()[2].strip().replace('$', '').replace(',', '')
            current_row["Gross Pay"] = float(gross_val)
        #FedTax
        if "Federal Income Tax" in text:
            fed_val = text.split("Federal Income Tax")[1].split()[0].strip().replace(',', '')
            current_row["Fed. Tax"] = float(fed_val)
        #SSTax
        if "Social Security" in text:
            SS_val = text.split("Social Security")[1].split()[0].strip().replace(',', '')
            current_row["SS. Tax"] = float(SS_val)
        #MedicareTax
        if "Medicare" in text:
            Medi_val = text.split("Medicare")[1].split()[0].strip().replace(',', '')
            current_row["Medicare"] = float(Medi_val)
        #CATax
        if "CA Income Tax" in text:
            CA_val = float(text.split("CA Income Tax")[1].split()[0].strip().replace(',', ''))
            current_row["CA. Tax"] = float(CA_val)
        #CA State Disability Ins
        if "CA State Disability Ins" in text:
            CAD_val = float(text.split("CA State Disability Ins")[1].split()[0].strip().replace(',', ''))
            current_row["Dis. Ins."] = float(CAD_val)
        # Tax Total
        current_row["Tax Total"] = current_row["Dis. Ins."] + current_row["CA. Tax"] + current_row["Medicare"] +current_row["SS. Tax"] + current_row["Fed. Tax"]
        #netpay
        if "NET PAY:" in text:
            net_val = text.split("NET PAY:")[1].split()[0].strip().replace('$', '').replace(',', '')
            current_row["Net Pay"] = float(net_val)
        #add current row to the table
        all_data.append(current_row)
    else:
         print("! File is not a PDF !")

df = pd.DataFrame(all_data)
# Sorting and adding totals
df = df.sort_values("Pay Date")
df['Total Gross YTD'] = df['Gross Pay'].cumsum()
df['Total Tax YTD'] = df['Tax Total'].cumsum()
df['Total Net YTD'] = df['Net Pay'].cumsum()
print(df)
df.to_excel(f'paymaker/output/PayStub_C_{date.today()}.xlsx',index=False)