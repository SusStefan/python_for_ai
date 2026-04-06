import os
import pandas as pd

if os.path.exists('sales-analysis/data/sales.csv'):
    print("-> Found file !")
    df = pd.read_csv('sales-analysis/data/sales.csv')
    print("-> Printing CSV Data:")
    print(df)
    print(f"\nShape: {df.shape[0]} rows, {df.shape[1]} columns")
    df['total'] = df['quantity'] * df['price']
    print("\n With Totals:")
    print(df)

    os.makedirs("sales-analysis/output",exist_ok=True)
    print("\nFiles saved:")
    df.to_json('sales-analysis/output/sales_data.json',orient='records',indent=1)
    print('sales-analysis/output/sales_data.json')
    df.to_csv('sales-analysis/output/sales_data.csv',index=False)
    print('sales-analysis/output/sales_data.csv')
    df.to_excel('sales-analysis/output/sales_data.xlsx',index=False)
    print('sales-analysis/output/sales_data.xlsx')
else:
    print("-> ERROR ! Sales file was not found !")