#!/usr/local/bin/python3
#python3 report_main.py Report_google_ads/22-12-2021_04:28.csv Report_google_ads/22-12-2021_04:31.csv

import sys
import os
import pandas as pd
from collections import Counter
import re
import time

 
def readCommandLine(argv):
    try:
        repeat_files = [k for k,v in Counter(argv).items() if v > 1]
        for arg in argv:
            file = arg.replace('Report_google_ads/', '')
            dir = os.listdir('Report_google_ads')
            count = 0
            if file not in dir:
                print(f'\nФайла "{file}"" нет в папке "Report_google_ads"')
                count += 1
        if count > 0:
            print(f'\nВ следующий раз выбирайте файлы из списка: {dir}')
        if len(repeat_files) > 0:
            print('\nУ Вас есть повторяющиеся файлы', repeat_files)
            answer = input('\nВы хотите продолжить (yes/no): ')
            if answer == 'yes':
                data_consolidation(argv)
            else:
                print('\nЗавершение работы приложения!')
        elif count == 0:
            data_consolidation(argv)
    except:
        print("\nВы не правильно ввели файлы!", sys.exc_info())

def data_consolidation(list_file):
    try:
        dataframes = []
        for file_csv in list_file:
            df = pd.read_csv(file_csv)
            dataframes.append(df)

        result = pd.concat(dataframes, ignore_index=True)
        list_columns = result.columns.tolist()
        
        print(list_columns[1:])
        input_columns = input('\nВыберете название колонок и введите их через запятую: ')
        col = re.findall(r'".+?"|[\w-]+', input_columns)
        column_data = result.reindex(columns = col)
        
        now_date = time.strftime("%d-%m-%Y_%H:%M")
        dir = 'Consolidated_reports/' + str(now_date) + '.csv'
        column_data.to_csv(dir, index = False)

        print(f'\nФайл {dir} успешно создан!')

    except:
        print('\nВы не правильно указали колонки!')

if __name__ == '__main__':
    try:
        readCommandLine(sys.argv[1:])
    except:
        print("\nНе удалось объединить файлы! Попробуйте еще раз!", sys.exc_info())