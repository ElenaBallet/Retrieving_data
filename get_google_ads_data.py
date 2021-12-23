#!/usr/bin/python3

import pandas as pd
import os
import time


def unload_report_gads(client, customer_id, start, end):
  try:
      ga_service = client.get_service("GoogleAdsService")
      search_request = client.get_type("SearchGoogleAdsStreamRequest")
      search_request.customer_id = customer_id 

      # get campaign data
      query_campaign = """ 
      SELECT
        campaign.id,
        campaign.name,
        metrics.cost_micros, 
        metrics.clicks, 
        metrics.ctr, 
        metrics.impressions,
        campaign.target_roas.target_roas
      FROM campaign
      WHERE segments.date BETWEEN '"""+str(start)+"""' AND '"""+str(end)+"""'
        AND campaign.status != 'REMOVED'
      """

      search_request.query = query_campaign
      stream_campaign = ga_service.search_stream(search_request)

      list_campaign = []

      for batch in stream_campaign:
        for row in batch.results:
          campaign = row.campaign
          metrics = row.metrics
    
          dict_campaign = {}

          dict_campaign['data'] = str(start) + ' ' + str(end)
          dict_campaign['campaign'] = campaign.name
          dict_campaign['campaign_id'] = campaign.id
          dict_campaign['spend'] = metrics.cost_micros/1000000
          dict_campaign['impressions'] = metrics.impressions
          dict_campaign['clicks'] = metrics.clicks
          dict_campaign['links_clicks'] = metrics.ctr
          dict_campaign['revenue'] = campaign.target_roas.target_roas
          list_campaign.append(dict_campaign)

      df_campaign = pd.DataFrame(list_campaign)

      # get ad data
      query_ad = """ 
      SELECT
        campaign.id,
        ad_group.name, 
        ad_group_ad.ad.responsive_search_ad.headlines
      FROM ad_group_ad
      WHERE segments.date BETWEEN '"""+str(start)+"""' AND '"""+str(end)+"""'
      """

      search_request.query = query_ad
      stream_ad = ga_service.search_stream(search_request) 
      
      dict_headlines = {}
      dict_ad_group = {}
      
      for batch in stream_ad:
        for row in batch.results:

          campaign_id = row.campaign.id
          dict_ad_group[campaign_id] = row.ad_group.name
          ad = row.ad_group_ad.ad.responsive_search_ad.headlines

          dict_ad = {'ad': list(ad)}

          df_ad = pd.DataFrame(dict_ad)

          for column in df_ad:
            col = df_ad[column].astype(str).str.split('"\n').str[0]
            col_headline = col.str.lstrip('text: "')
            df_ad[column] = col_headline

          if not df_ad.empty:
            headline = ('/'.join(df_ad['ad']))
            dict_headlines[campaign_id] = headline
          else:
            dict_headlines[campaign_id] = ''

      df_campaign['ad_group'] = df_campaign['campaign_id'].map(dict_ad_group)
      df_campaign['ad'] = df_campaign['campaign_id'].map(dict_headlines)
      

      # get location data
      query_location = """ 
      SELECT 
        campaign.id,
        campaign_criterion.proximity.address.city_name
        FROM location_view
        WHERE segments.date BETWEEN '"""+str(start)+"""' AND '"""+str(end)+"""'
      """

      search_request.query = query_location
      stream_location = ga_service.search_stream(search_request)

      dict_location = {}

      for batch in stream_location:
        for row in batch.results:
          dict_location[campaign.id] = row.campaign_criterion.proximity.address.city_name

      df_campaign['country'] = df_campaign['campaign_id'].map(dict_location)

      # get conversion data
      query_conversion = """ 
      SELECT 
      conversion_action.name
      FROM conversion_action
      """

      search_request.query = query_conversion
      stream_conversion = ga_service.search_stream(search_request)

      for batch in stream_conversion:
        for row in batch.results:

          conversion_name = row.conversion_action.name
          metrics_conversions = row.metrics.all_conversions

          pd_conversion = pd.Series(conversion_name)

          if conversion_name == 'Добавление в корзину':
            df_campaign.insert(7, "adds_to_cart", metrics_conversions, False)
          if conversion_name == 'Покупка':
            df_campaign.insert(7, "purchases", metrics_conversions, False)
          if pd_conversion.str.startswith('Установки приложения').bool() == True:
            df_campaign.insert(7, "ad_network_installs", metrics_conversions, False)

      df = df_campaign.drop(columns = 'campaign_id')
      col = df.columns.tolist()
      col = col[ : 2] + col[ (len(col) - 3) : ] + col[ 2 : (len(col) - 3) ]
      col = col[ : 8] + col[10:11] + col[8 : 9] + col[11 : 12] + col[9 : 10] + col[12 :]
      df = df[col]

      now_date = time.strftime("%d-%m-%Y_%H:%M")
      file_csv = 'Report_google_ads/' + str(now_date) + '.csv'

      if os.path.isfile(str(now_date) + '.csv') not in os.listdir('Report_google_ads'):
        pd.DataFrame.to_csv(df, file_csv)
        print(f'\nОтчет успешно выгружен в папку {file_csv}')
      else:
        print('\nОшибка при создании файла!')
      
  except:
    print("\nОтчет с Google Ads не выгружен! Попробуйте еще раз!")