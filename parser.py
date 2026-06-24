"""
Excel Data Sync v1.0
Automated data retrieval using GitHub API
"""

import pandas as pd
import requests
import os
from datetime import datetime
import base64


GITHUB_TOKEN = ''  
REPO_OWNER = 't3dom1'
REPO_NAME = 'Excel_Auto_Updater'
FILE_PATH = 'Book.xlsx'
BRANCH = 'main'

LOCAL_FILE = 'Book.xlsx'


def download_file_via_api():

    try:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Downloading via GitHub API...")
        
        url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}?ref={BRANCH}'
        
        headers = {'Accept': 'application/vnd.github.v3+json'}
        if GITHUB_TOKEN:
            headers['Authorization'] = f'token {GITHUB_TOKEN}'
        
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            content = base64.b64decode(data['content'])
            
            with open(LOCAL_FILE, 'wb') as f:
                f.write(content)
            
            print(f"Downloaded: {len(content)} bytes")
            print(f"File SHA: {data.get('sha', 'N/A')[:8]}")
            return True
        elif response.status_code == 403:
            print("API limit reached. Use a token for higher limits.")
            return False
        else:
            print(f"API Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"API Error: {e}")
        return False


def download_file_raw():

    try:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Trying raw download...")
        
        url = f'https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/{FILE_PATH}'
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            with open(LOCAL_FILE, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {len(response.content)} bytes")
            return True
        else:
            print(f"Raw download failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Raw download error: {e}")
        return False


def download_file():

    
    if download_file_via_api():
        return True
    
    print("API failed, trying raw download...")
    if download_file_raw():
        return True
    
    print("All download methods failed.")
    if os.path.exists(LOCAL_FILE):
        print(f"Using existing local file: {LOCAL_FILE}")
        return True
    else:
        print(f"No local file found: {LOCAL_FILE}")
        return False


def parse_excel():
    if not os.path.exists(LOCAL_FILE):
        print("File not found")
        return None
    
    try:
        xl = pd.ExcelFile(LOCAL_FILE, engine='openpyxl')
        sheets = xl.sheet_names
        print(f"Sheets: {sheets}")
        
        data = []
        
        for sheet in sheets:
            df = pd.read_excel(LOCAL_FILE, sheet_name=sheet, header=None)
            
            for row in [7, 11, 15, 19, 23]:
                if row < len(df):
                    name = df.iloc[row, 0]
                    amount = df.iloc[row, 3]
                    people = df.iloc[row, 6]
                    
                    if pd.notna(name) and pd.notna(amount):
                        data.append({
                            'ФИО': str(name).strip(),
                            'СУММА': float(str(amount).replace(' ₽', '').replace('₽', '').replace(' ', '').replace(',', '.')),
                            'ЧЕЛ': int(people) if pd.notna(people) else 0
                        })
        
        if not data:
            print("No data found")
            return None
        
        result = pd.DataFrame(data)
        result.insert(0, '№', range(1, len(result) + 1))
        return result
    
    except Exception as e:
        print(f"Parse error: {e}")
        return None


def display_table(df):
    if df is None:
        return
    
    print("\n" + "="*50)
    print("CONSOLIDATED TABLE")
    print("="*50)
    print(df.to_string(index=False))



def main():
    print("="*50)
    print("EXCEL DATA SYNC v1.0 (GitHub API)")
    print("="*50)
    print(f"Repository: {REPO_OWNER}/{REPO_NAME}")
    print(f"File: {FILE_PATH}")
    print(f"Local file: {LOCAL_FILE}")
    print("="*50)
    
    
    if download_file():
        df = parse_excel()
        if df is not None:
            display_table(df)
        else:
            print("Failed to parse data")
    else:
        print("Failed to get file")

if __name__ == "__main__":
    main()
