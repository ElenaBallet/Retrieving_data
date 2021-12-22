# Тестовое задание: получение данных с Google ads

Функционал 1:

Вызвать консольную команду в которой передаются только даты с и по (включительно) за которые надо скачать отчет для личного аккаунта пользователя.
Отчет надо записать как CSV 

Отчет надо качать из Google Ads. В отчете должны быть следующие колонки:
date,campaign,adgroup,ad,country,spend,impressions,clicks,purchases,link_clicks,adds_to_cart,ad_network_installs,revenue


Функционал 2:

Вызвать консольную команду куда передаются названия файлов с CSV (из функционала 1).
А так же указать по каким колонкам (от 1 и более) включить сортировку.
Как результат необходимо видеть CSV файл в котором будут объединены данные из CSV файлов и отсортированы по указанным колонкам.


Требования:
 - один проект
 - python 3.9
 - без джанги
 - разработка с GIT + залить на GitHub 

# Решение тестового задания

## 1. Шаги выполнения задания
Для возможности выгрузки отчетов из Google Ads  был создан тестовый акаунт согласно [официальной документации](https://developers.google.com/google-ads/api/docs/first-call/overview). 
Шаги для запуска API приложения:
1. В процессе авторизации был получен Developer token, который в дальнейшем использовался для запуска Google Ads API приложения. 
2. Для создания приложения использовалась Google API Console. После создания приложения присваиваются OAuth2 client ID и client secret. 
3. Для получения доступа OAuth2 access и прохождения аутентификации refresh tokens использовалась [стандартная библиотека](https://github.com/googleads/googleads-python-lib/blob/master/examples/adwords/authentication/generate_refresh_token.py) и был подготовлен [google-ads.yaml](https://github.com/googleads/google-ads-python/blob/main/google-ads.yaml). Получение рефреш токена описано [здесь](Consolidated_reports/22-12-2021_12:11.csvhttps://github.com/googleads/googleads-python-lib/wiki/API-access-using-own-credentials-(installed-application-flow)).
4. Для возможности выгрузки данных с Google Ads были созданы компании, группы объявлений, объевления, геотаргет, конверсии. 
5. Тестовый аккаунт имеет ряд ограничений, что написано в [официальной документации](https://developers.google.com/google-ads/api/docs/reporting/zero-impressions), а именно 'Zero impressions in search results'. Нулевые показы всегда исключаются при сегментировании отчета, если все выбранные метрики равны нулю. Что приводит к исключению возможности использования сегментации по датам, конверсиям, геотаргену. ![]()
6. Так как API Google AdWords перестанет работать 27 апреля 2022 года при составлении API запросов использовались [библиотеки Google Ads API](https://github.com/googleads/google-ads-python) и конструктор запросов [Google Ads Query Builder](https://developers.google.com/google-ads/api/fields/v9/location_view_query_builder).

## 2. Запуск

1. Requirements: Python 3.7+, pandas, googleads, dateparser. Для установки библиотек выполните команду:

    ```python
    pip install -r requirements.txt
    ```
2. Первая часть задания - получения отчета с Google Ads, запустите команду:
    ```python
    python3 google_ads_main.py 15-12-2021 16-12-2021
    ```
    Затем необходимо будет ввести через запятую токен разработчика, id приложения, секретный ключ приложения, refresh токен, id управляющего аккаунта без тире. ![]()

    А также необходиом будет ввести id клиента без тире. ![]()

3. Вторая часть задания - объединение данных из CSV файлов, выполните команду:
    ```python
    python3 report_main.py Report_google_ads/22-12-2021_04:28.csv Report_google_ads/22-12-2021_04:31.csv
    ```   
    Из появившегося списка выберете названия колонок для которых будет сформирован отчет и введите их через запятую. ![]()

> В процессе написания кода основаня задача сводилась к правильному постоению Google Ads Query и преобразование классов [Google Ads](https://developers.google.com/google-ads/api/reference/rpc/v8/overview). Например, `class 'google.api_core.grpc_helpers._StreamingResponseIterator' `возвращает данные в таком виде:
> ```
>    ,campaign_id,ad_group_name,responsive_search_ad_headlines
>    0,155310101212,Группа объявлений 1,"[text: ""learn python""
>    asset_performance_label: PENDING
>    policy_summary_info {
>    review_status: REVIEW_IN_PROGRESS
>    }
>    , text: ""django blog""
>    asset_performance_label: PENDING
>    policy_summary_info {
>    review_status: REVIEW_IN_PROGRESS
>    }
>    , text: ""fast strat python""
>    asset_performance_label: PENDING
>    policy_summary_info {
>    review_status: REVIEW_IN_PROGRESS
>    }
>    ]"
>    1,156150125644,Ad group 1,[]
> ```
> Из этих данных необходимо было извлечь объявления: learn python/django blog/fast strat python. Также ограничевало получение данных отсутсвие сегментации по дате, конверсии и геотаргете.

## 3. Результаты
Результаты выполнения кода представлены в виде отчетов в папках Report_google_ads', 'Consolidated_reports'.

![]()