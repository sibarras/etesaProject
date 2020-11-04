import calendar
# from sys import time
import datetime
import sqlite3
import pandas as pd
# print(str(datetime.datetime.now()).split()[0].split('-')[0])
# print('\n\n')
# print(datetime.datetime.now().now())

# print(type(datetime.date.today().year))
# print(calendar.month_name[11])

conn = sqlite3.connect('./database/accounts.db')
c = conn.cursor()
df = pd.read_sql_query('SELECT * FROM accounts', conn)
print(df.loc[df['UBICAC']=='SMDN']['CUENTA CONTABLE'].values[0])
conn.close()