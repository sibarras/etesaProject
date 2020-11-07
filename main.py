from extra_hours_handler import ExtraHours
import distribution_handler
import pandas as pd
import sqlite3

works = {
'place':['SPANAMA', 'SPANAMA2', 'SPANAMA'],
'day':[2, 7, 8],
'init':['3:30', '6:00', '3:30'],
'end':['6:45', '7:00', '4:30'],
'equip':['CT', 'TX', 'PT'],
'name':['11A3', 'T-3', 'PT-34']
}

db_name = './database/accounts.db'
conn = sqlite3.connect(db_name)
accounts_data = pd.read_sql_query('SELECT * FROM accounts', conn, index_col='index')
conn.close()
del conn, db_name

results_path = './Excel Books/results/'
pdf_path = 'C:\\Users\\Samuel\\Desktop\\Projects\\etesaProject\\Excel Books\\results\\'

if __name__ == "__main__":
    
    db_colabs = './database/colaborators.db'
    conn = sqlite3.connect(db_colabs)
    colabs_data = pd.read_sql_query('SELECT * FROM colaborators', conn, index_col='index')
    personal_data = colabs_data.loc[colabs_data['cedula']=='8-892-2460']
    conn.close()
    del conn, db_colabs, colabs_data

    wb = ExtraHours()
    wb.write_personal_data(personal_data)
    wb.write_time_data()
    wb.write_works(works, accounts_data)
    wb.write_non_worked_days()

    folder_name = wb.make_folder(wb.suggested_output_filename)
    wb.save_document(wb.suggested_output_filename, results_path+folder_name)
    wb.excel_to_pdf(wb.suggested_output_filename, pdf_path+folder_name)
