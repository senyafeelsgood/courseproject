import numpy as np 
import pandas as pd
import gspread
import pickle
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import time

cols = ['ROA(C) before interest and depreciation before interest',
       'Operating Gross Margin', 'Realized Sales Gross Margin',
       'Operating Profit Rate', 'Pre-tax net Interest Rate',
       'After-tax net Interest Rate',
       'Non-industry income and expenditure/revenue',
       'Continuous interest rate (after tax)', 'Operating Expense Rate',
       'Research and development expense rate', 'Cash flow rate',
       'Interest-bearing debt interest rate', 'Tax rate (A)',
       'Net Value Per Share (B)', 'Persistent EPS in the Last Four Seasons',
       'Cash Flow Per Share', 'Revenue Per Share (Yuan ¥)',
       'Operating Profit Per Share (Yuan ¥)',
       'Per Share Net profit before tax (Yuan ¥)',
       'Realized Sales Gross Profit Growth Rate',
       'Operating Profit Growth Rate', 'After-tax Net Profit Growth Rate',
       'Regular Net Profit Growth Rate', 'Continuous Net Profit Growth Rate',
       'Total Asset Growth Rate', 'Net Value Growth Rate',
       'Total Asset Return Growth Rate Ratio', 'Cash Reinvestment %',
       'Current Ratio', 'Quick Ratio', 'Interest Expense Ratio',
       'Total debt/Total net worth', 'Debt ratio %', 'Net worth/Assets',
       'Long-term fund suitability ratio (A)', 'Borrowing dependency',
       'Contingent liabilities/Net worth',
       'Operating profit/Paid-in capital',
       'Net profit before tax/Paid-in capital',
       'Inventory and accounts receivable/Net value', 'Total Asset Turnover',
       'Accounts Receivable Turnover', 'Average Collection Days',
       'Inventory Turnover Rate (times)', 'Fixed Assets Turnover Frequency',
       'Net Worth Turnover Rate (times)', 'Revenue per person',
       'Operating profit per person', 'Allocation rate per person',
       'Working Capital to Total Assets', 'Quick Assets/Total Assets',
       'Current Assets/Total Assets', 'Cash/Total Assets',
       'Quick Assets/Current Liability', 'Cash/Current Liability',
       'Current Liability to Assets', 'Operating Funds to Liability',
       'Inventory/Working Capital', 'Inventory/Current Liability',
       'Current Liabilities/Liability', 'Working Capital/Equity',
       'Current Liabilities/Equity', 'Long-term Liability to Current Assets',
       'Retained Earnings to Total Assets', 'Total income/Total expense',
       'Total expense/Assets', 'Current Asset Turnover Rate',
       'Quick Asset Turnover Rate', 'Working capitcal Turnover Rate',
       'Cash Turnover Rate', 'Cash Flow to Sales', 'Fixed Assets to Assets',
       'Current Liability to Liability', 'Current Liability to Equity',
       'Equity to Long-term Liability', 'Cash Flow to Total Assets',
       'Cash Flow to Liability', 'CFO to Assets', 'Cash Flow to Equity',
       'Current Liability to Current Assets', 'Liability-Assets Flag',
       'Net Income to Total Assets', 'Total assets to GNP price',
       'No-credit Interval', 'Gross Profit to Sales',
       "Net Income to Stockholder's Equity", 'Liability to Equity',
       'Degree of Financial Leverage (DFL)',
       'Interest Coverage Ratio (Interest expense to EBIT)',
       'Net Income Flag', 'Equity to Liability']


# Senya local 
cred_path = "/Users/itsplaygroundbeats/Documents/VSCODE_PROJECTS/anomalies_coursework/service_acct.json"

def data_preprocessing(df_new_object):
        
    # vars_high_correlation = ['ROA(A) before interest and % after tax',
    #                         'ROA(B) before interest and depreciation after tax',
    #                         'Net Value Per Share (A)', ' Net Value Per Share (C)']

    # vars_low_variance = ['Net Income Flag',
    #                     'Working capitcal Turnover Rate',
    #                     'Cash Flow to Sales',
    #                     'Total Asset Return Growth Rate Ratio',
    #                     'Continuous Net Profit Growth Rate',
    #                     'Inventory/Working Capital',
    #                     'Operating Profit Growth Rate',
    #                     'Non-industry income and expenditure/revenue',
    #                     'Interest Expense Ratio',
    #                     'Working Capital/Equity',
    #                     'Realized Sales Gross Profit Growth Rate',
    #                     'Total income/Total expense',
    #                     'Contingent liabilities/Net worth',
    #                     'No-credit Interval',
    #                     'Continuous interest rate (after tax)',
    #                     'Pre-tax net Interest Rate',
    #                     'Cash Flow to Equity',
    #                     'Operating Profit Rate',
    #                     'Interest Coverage Ratio (Interest expense to EBIT)',
    #                     'Inventory and accounts receivable/Net value',
    #                     'Current Liabilities/Equity',
    #                     'Current Liability to Equity',
    #                     'After-tax net Interest Rate',
    #                     'After-tax Net Profit Growth Rate',
    #                     'Regular Net Profit Growth Rate']

    # df_new_object = df_new_object[df_new_object.columns.drop(vars_high_correlation, vars_low_variance)]

    with open('scaler.pkl', 'rb') as f:
        scaler_pickle = pickle.load(f)

    df_new_object = scaler_pickle.transform(df_new_object)

    with open('pca.pkl', 'rb') as f:
        pca_pickle = pickle.load(f)

    info_new_object = pca_pickle.transform(df_new_object)

    return info_new_object



def make_prediction(info_new_object):

    with open('logreg.pkl', 'rb') as f:
        logreg_pickle = pickle.load(f)

    pred_class =logreg_pickle.predict(info_new_object)
    
    if pred_class == 1:
        prediction = "У компании высокий риск банкротства!"
    if pred_class == 0:
        prediction = "У компании низкий риск банкротства!"

    return prediction

def create_gs():
    
    # Create a new Google Sheet
    # Auth using cred.josn 
    # Service account 
    gc = gspread.service_account(filename=cred_path)
    # Adding name to sheet
    sh = gc.create("Финансовые показатели")
    # first page
    worksheet = sh.get_worksheet(0)
    # Share the Google Sheet with anyone with the link
    sh.share(None, perm_type='anyone', role='writer', notify=False)

    for i, col in enumerate(cols, start=1):
        time.sleep(0.1)
        worksheet.update_cell(i, 1, col)

    return sh.url


def gs_to_df(url):
    
    # Set up the credentials for the service account
    creds = service_account.Credentials.from_service_account_file(cred_path, scopes=['https://www.googleapis.com/auth/spreadsheets'])
    # Set up the Google Sheets API client
    service = build('sheets', 'v4', credentials=creds)
    # Set the ID of the Google Sheets file and the range of cells to retrieve
    spreadsheet_id = url.split(sep= "/d/")[1]
    range_name = 'Sheet1!A:B'

    # Retrieve the data from the Google Sheets file
    result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,range=range_name).execute()
    df = pd.DataFrame(result['values'])

    df.set_index(df[0], inplace=True)
    df.index.name = None
    df = df.T
    df.drop(0, inplace=True)

    return df



def clear_column(spreadsheet_url, column_number):

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
            cred_path, scope)
    gc = gspread.authorize(credentials)

    spreadsheet = gc.open_by_url(spreadsheet_url)

    worksheet = spreadsheet.get_worksheet(0)  # выберите лист, который вам нужен, здесь мы выбираем первый лист 

    # получите общее количество строк в столбце
    num_rows = len(worksheet.col_values(column_number)) 

    # очистите столбец
    cell_list = worksheet.range(f'B1:B{num_rows}')  # замените 'B1:B{num_rows}' на диапазон вашего столбца

    for cell in cell_list:
        cell.value = ''
    worksheet.update_cells(cell_list)





if __name__ == "__main__":
    # print(make_prediction(data_preprocessing(gs_to_df("https://docs.google.com/spreadsheets/d/1VH56vqu7FNdHQvRwrhsUZSU61mmBJVUCWqf6pCqenhE"))))
    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1VH56vqu7FNdHQvRwrhsUZSU61mmBJVUCWqf6pCqenhE'  # замените на URL вашего листа Google Sheets
    clear_column(spreadsheet_url, 2)  # вызываете функцию, 2 означает второй столбец




