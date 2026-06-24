"""
Excel Data Sync
"""

import pandas as pd
import requests
import os
from datetime import datetime
import urllib3
import warnings

warnings.filterwarnings('ignore')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FILE_URL = 'https://raw.githubusercontent.com/t3dom1/Excel-Auto-Updater/main/Book.xlsx'
LOCAL_FILE = 'Book.xlsx'

def download_file():
    methods = [
        {'verify': False, 'timeout': 30},
        {'verify': True, 'timeout': 30},
        {'verify': False, 'timeout': 60},
        {'verify': True, 'timeout': 60}
    ]
    
    for i, params in enumerate(methods, 1):
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Попытка {i}...")
            response = requests.get(FILE_URL, **params)
            
            if response.status_code == 200:
                with open(LOCAL_FILE, 'wb') as f:
                    f.write(response.content)
                print(f"Загружено: {len(response.content)} байт")
                return True
        except:
            continue
    
    print("Все попытки загрузки не удались")
    return False

def parse_excel():
    if not os.path.exists(LOCAL_FILE):
        print("Файл не найден")
        return None
    
    try:
        xl = pd.ExcelFile(LOCAL_FILE, engine='openpyxl')
        sheets = xl.sheet_names
        print(f"Найдены листы: {sheets}")
        
        all_data = []
        
        for sheet in sheets:
            df = pd.read_excel(LOCAL_FILE, sheet_name=sheet, header=None)
            
            for row in [7, 11, 15, 19, 23]:
                if row < len(df):
                    name = df.iloc[row, 0]
                    amount = df.iloc[row, 3]
                    people = df.iloc[row, 6]
                    
                    if pd.notna(name) and pd.notna(amount):
                        all_data.append({
                            'ФИО': str(name).strip(),
                            'СУММА': float(str(amount).replace(' ₽', '').replace('₽', '').replace(' ', '').replace(',', '.')),
                            'ЧЕЛ': int(people) if pd.notna(people) else 0
                        })
        
        if not all_data:
            print("Данные не найдены")
            return None
            
        df_result = pd.DataFrame(all_data)
        df_result.insert(0, '№', range(1, len(df_result) + 1))
        return df_result
        
    except Exception as e:
        print(f"Ошибка парсинга: {e}")
        return None

def display_table(df):
    if df is None:
        return
    
    print("\n" + "="*50)
    print("ОБЩАЯ ТАБЛИЦА")
    print("="*50)
    print(df.to_string(index=False))
    

def main():
    print("="*50)
    print("EXCEL DATA SYNC")
    print("="*50)
    
    
    success = download_file()
    
    if not success:
        print("Использован локальный файл")

    
    df = parse_excel()
    
    if df is not None:
        display_table(df)
    else:
        print("Не удалось обработать данные")

if __name__ == "__main__":
    main()
