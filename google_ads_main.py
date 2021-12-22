#!/usr/bin/python3
#python3 google_ads_main.py 15-12-2021 16-12-2021

import sys
import json
import dateparser
from google_ads_authentication import*
from get_google_ads_data import *


#Class for data validation
class DataValidation:
    def __init__(self):
        if len(sys.argv) == 3:
            self.start = str(sys.argv[1])
            self.end = str(sys.argv[2])
        elif len(sys.argv) != 3:
            dates = input('Введите даты начала и окончания отчетного периода в формате DD-MM-YYYY: ').split()
            if len(dates) == 2:
                self.start = dates[0]
                self.end = dates[1]
            elif len(dates) != 2:
                print('Вы ввели не две даты!')
                
    #Function for date validation
    def date_validation(self):
        global start
        global end
        try:
            date1 = dateparser.parse(self.start,  settings={'TIMEZONE': 'US/Eastern'}).date()
            date2 = dateparser.parse(self.end,  settings={'TIMEZONE': 'US/Eastern'}).date()
            if date2 >= date1:
                start = date1
                end = date2
            elif date2 < date1:
                print('Дата начала должна быть больше или равна дате окончания!')
        except Exception:
            print('Вы ввели некорректные даты!')

    #Function for data authetication validation
    def authetication(self, answer=None):
        cred_file = "google_ads_cred.json"
        cred_file = open(cred_file, 'r+')
        cred_json = json.load(cred_file)
        self.answer = answer
        try:
            if self.answer == 'yes':
                secret_data = input('Введите через запятую токен разработчика, id приложения, секретный ключ приложения, refresh токен, id управляющего аккаунта без тире: ').split(', ')
                cred_json.pop('use_proto_plus')
                if len(secret_data) == 5:
                    i = 0
                    for key in cred_json.keys():
                        cred_json[key] = secret_data[i]
                        i += 1
                    cred_json['use_proto_plus'] = 'True'
                    with open('google_ads_cred.json', 'w') as f:
                        json.dump(cred_json, f)
                    return cred_json
                elif len(secret_data) != 5:
                    input_ans = input('Вы ввели не пять секретных данных! Хотите продолжить (yes/no): ')
                    read_command_line.authetication(input_ans)
            elif self.answer != 'yes':
                if cred_json['login_customer_id'] == "":
                    input_ans = input('Файл с Вашими данными аутификации пуст. Хотите продолжить (yes/no): ')
                    if input_ans == 'yes':
                        read_command_line.authetication(input_ans)
                    elif input_ans != 'yes':
                        print('Не правильно заполнены секретные данные!')
                elif cred_json['login_customer_id'] != "":
                    return cred_json
        except Exception:
            print('Вы ввели неверные значения секретных данных!')

    #Function for save customer id
    def save_customer_id(self):
        answer = input('Вы не вводили ID клиента или хотите изменить его (yes/no): ')
        customer_file = "google_ads_customer_id.json"
        customer_file = open(customer_file, 'r+')
        customer_json = json.load(customer_file)
        try:
            if answer == 'yes':
                customer = input("Введите ID клиента без тире: ")
                for key in customer_json.keys():
                    customer_json[key] = customer
                with open('google_ads_customer_id.json', 'w') as f:
                    json.dump(customer_json, f)
                    return customer        
            if customer_json['customer_id'] != "":
                return customer_json['customer_id']
            elif answer != 'yes':
                print('Не правильно введен customer_id!') 
        except Exception:
            print('Вы ввели неверные значения customer_id!')

if __name__ == "__main__":

    #getting the command line parameter
    read_command_line = DataValidation()
    try:
        read_command_line.date_validation()
        input_answer = input('Вы первый раз проходите аутентификацию или хотите изменить данные (yes/no): ')
        google_ads_cred_json = read_command_line.authetication(input_answer)
        
        customer_id = read_command_line.save_customer_id()

        api_client = google_ads_authentication(google_ads_cred_json)

        campaign_report = unload_report_gads(api_client, customer_id, start, end)
 
    except Exception:
            print('Отчет не выгружен! Попробуйте всё заново!')