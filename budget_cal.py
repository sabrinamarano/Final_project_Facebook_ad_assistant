#!/usr/bin/env python
# coding: utf-8
import streamlit as st
 
st.title(" FACEBOOK AD ASSISTANT")
 



#budget calculator
import pickle
loaded_model = pickle.load(open('budget.sav', 'rb'))

import pandas as pd
import numpy as np

countries_kpis= pd.read_csv('countries_kpi_def.csv')
countries_kpis=countries_kpis.drop('Unnamed: 0', axis=1)
st.write("""
### BUDGET CALCULATOR
 
""")
x = st.selectbox('Country',('Italy','Spain','Germany'))

y = st.selectbox('Industry',('gaming app',  'entertainment app', 'photo&video app',
       'shopping app', 'finance app', 'education app', 'lifestyle app',
       'books app', 'dating app', 'news&magazine app', 'food&drink app',
       'comic app', 'travel app', 'ecommerce', 'B2B'))

query = countries_kpis[(countries_kpis['country'] == x) & (countries_kpis['industry'] == y)]
cpm =query['cpm']
z= st.slider("N.people to reach", 10000,1000000,10000)
budget = ((cpm*z)/1000).round(0)
budget= budget.astype(int)
query['budget']= budget
st.write("Your budget is:", query['budget'])

df = pd.DataFrame({'Reach':z,'Spent': budget})

# In[ ]:

#predictions
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression

clicks_model = pickle.load(open('prediction_clicks.sav', 'rb'))

pred_clicks=clicks_model.predict(df)
pred_clicks= pred_clicks.astype(int)



conversions = pd.DataFrame({'Clicks':pred_clicks, 'Spent': budget})

conversion_model = pickle.load(open('prediction_conversions.sav', 'rb'))

pred_conversions=conversion_model.predict(conversions)
pred_conversions= pred_conversions.astype(int)


predictions_kpis= pd.DataFrame({'Reach':z,'Spent': budget,'Clicks':pred_clicks, 'Conversions':pred_conversions})

r= st.slider("Select your average revenue", 10,1000)
predictions_kpis['Impressions']= predictions_kpis['Reach']*2
predictions_kpis['Revenue']= predictions_kpis['Conversions']*r
predictions_kpis['ROI']=((predictions_kpis['Revenue']-predictions_kpis['Spent'])/predictions_kpis['Spent']*100)
predictions_kpis['CPC']=(predictions_kpis['Spent']/predictions_kpis['Clicks'])
predictions_kpis['CPM']=((predictions_kpis['Spent']/predictions_kpis['Impressions'])*1000)
predictions_kpis['CTR']=(predictions_kpis['Clicks']/predictions_kpis['Impressions']*100)

st.write("Based on your input you can expect:", predictions_kpis)



#campaign analysis

st.write("""
### CAMPAIGN ANALYSIS
 
""")
import streamlit as st
import sqlalchemy
import pymysql
import random

user_campaigns = pd.DataFrame({'name':"na", 'cpm': 0, 'cpc':0,'ctr':0,'roi':0,'impression':0,'conversion':0, 'clicks':0, 'revenue':0,'spent':0,'reach':0}, index=[0])
schema="marketing"
host="wbs-project3-db.cot1oigahvlu.us-east-2.rds.amazonaws.com"
user="admin"
password='mypasswordsabrina2021'
port=3306
con = f'mysql+pymysql://{user}:{password}@{host}:{port}/{schema}'
        
#user_campaigns.to_sql('user_campaigns', if_exists='append', con=con, index=False)

a = st.selectbox('Do you want analyze your campaigns?',('','yes', 'no'))
if a == "no":
    st.write(f"Never mind, maybe you want try a little bit more", key='1') 
else:
    b= st.selectbox('Do you have already use this tool?',('','yes', 'no'))
    if b == "yes":
        query=pd.read_sql(sql = """SELECT DISTINCT name, cpm, cpc, ctr, roi, impression, conversion, clicks, revenue, spent, reach
 FROM user_campaigns 
 WHERE (cpm<> 0 AND cpc <> 0 AND ctr <> 0 AND roi <> 0 AND impression <> 0 AND conversion <> 0 AND clicks <> 0 AND revenue <> 0 AND spent <> 0 AND reach <> 0 )""",con = con)
        y=[]
        x = st.text_input("Insert your name", key='1')
        y.append(x)
        if query['name'].isin(y).any():
            e= st.selectbox('Do you want to see your previous campaigns?',('','yes', 'no'))
            if e =='yes':
                user_analysis_1=query.query('name == @x')
                st.line_chart(user_analysis_1[['cpm','cpc']])
                st.line_chart(user_analysis_1['ctr'])
                st.line_chart(user_analysis_1['roi'])
                st.line_chart(user_analysis_1[['conversion','clicks']])
                st.line_chart(user_analysis_1['revenue'])
                st.write("Amazing progress")
            else:
                st.write("Let's begin to analyze")
                cpm = st.number_input('cpm', key='1')
                cpc = st.number_input('cpc', key='1')
                ctr = st.number_input('ctr', key='1')
                roi = st.number_input('roi', key='1')
                conversions = st.number_input('conversion', key='1')
                clicks = st.number_input('clicks', key='1')
                impressions = st.number_input('impression', key='1')
                revenue = st.number_input('revenue', key='1')
                spent = st.number_input('spent', key='1')
                reach = st.number_input('reach', key='1')
                user_campaigns_1 = pd.DataFrame({'name':x,'cpm': cpm, 'cpc':cpc,
                     'ctr':ctr,'roi':roi,'impression':impressions,'conversion':conversions, 'clicks':clicks, 'revenue':revenue,'spent':spent,'reach':reach}, index=[0])
                
                #append results input to sql
                user_campaigns_1.to_sql('user_campaigns', if_exists='append', con=con, index=False)
                
                #user_campaigns= user_campaigns.append(user_campaigns_1, ignore_index=True)
                #user_campaigns=user_campaigns.query('name !="na"')
                
                
                
                #prediction
                df_1 = pd.DataFrame({'Reach':reach,'Spent': spent}, index=[0])
                pred_clicks_1=clicks_model.predict(df_1)
                pred_clicks_1= pred_clicks_1.astype(int)
                conversions_1 = pd.DataFrame({'Clicks':pred_clicks_1, 'Spent': spent})
                pred_conversions_1=conversion_model.predict(conversions_1)
                pred_conversions_1= pred_conversions_1.astype(int)
                predictions_kpis= pd.DataFrame({'Reach':reach,'Spent': spent,'Clicks':pred_clicks, 'Conversions':pred_conversions}, index=[0])
                predictions_kpis['Impressions']= impressions
                predictions_kpis['Revenue']= predictions_kpis['Conversions']*r
                predictions_kpis['ROI']=((predictions_kpis['Revenue']-predictions_kpis['Spent'])/predictions_kpis['Spent']*100)
                predictions_kpis['CPC']=(predictions_kpis['Spent']/predictions_kpis['Clicks'])
                predictions_kpis['CPM']=((predictions_kpis['Spent']/predictions_kpis['Impressions'])*1000)
                predictions_kpis['CTR']=(predictions_kpis['Clicks']/predictions_kpis['Impressions']*100)
                
                #analysis
                st.write("Comparison between your data and predicted data", key='1')
            
                cpm=user_campaigns_1['cpm'].reset_index()
                cpm['CPM']=predictions_kpis['CPM']
                cpm['your cpm']= cpm['cpm']
                cpm['pred cpm']= cpm['CPM']
                st.write(cpm[['your cpm','pred cpm']])
                st.bar_chart(cpm[['your cpm','pred cpm']])
                
                
                cpc=user_campaigns_1['cpc'].reset_index()
                cpc['CPC']=predictions_kpis['CPC']
                cpc['your cpc']= cpc['cpc']
                cpc['pred cpc']= cpc['CPC']
                st.write(cpc[['your cpc','pred cpc']])
                st.bar_chart(cpc[['your cpc','pred cpc']])
                
                
                ctr=user_campaigns_1['ctr'].reset_index()
                ctr['CTR']=predictions_kpis['CTR']
                ctr['your ctr']= ctr['ctr']
                ctr['pred ctr']= ctr['CTR']
                st.write(ctr[['your ctr','pred ctr']])
                st.bar_chart(ctr[['your ctr','pred ctr']])
                
                
                roi=user_campaigns_1['roi'].reset_index()
                roi['ROI']=predictions_kpis['ROI']
                roi['your roi']= roi['roi']
                roi['pred roi']= roi['ROI']
                st.write(roi[['your roi','pred roi']])
                st.bar_chart(roi[['your roi','pred roi']])
                
                
                conv=user_campaigns_1['conversion'].reset_index()
                conv['Conversions']=predictions_kpis['Conversions']
                conv['your conversions']=conv['conversion']
                conv['pred conversions']=conv['Conversions']
                st.write(conv[['your conversions','pred conversions']])
                st.bar_chart(conv[['your conversions','pred conversions']])
                
                
                cl=user_campaigns_1['clicks'].reset_index()
                cl['Clicks']=predictions_kpis['Clicks']
                cl['your clicks']= cl['clicks']
                cl['pred clicks']= cl['Clicks']
                st.write(cl[['your clicks','pred clicks']])
                st.bar_chart(cl[['your clicks','pred clicks']])
                
                
                rev=user_campaigns_1['revenue'].reset_index()
                rev['Revenue']=predictions_kpis['Revenue']
                rev['your revenue']= rev['revenue']
                rev['pred revenue']= rev['Revenue']
                st.write(rev[['your revenue','pred revenue']])
                st.bar_chart(rev[['your revenue','pred revenue']])
                
                
                
                c =st.selectbox('Another one?',('yes', 'no'))
                if c == "yes":
                    name_1 = st.text_input("Insert your name", key='3')
                    cpm_1 = st.number_input('cpm', key='2')
                    cpc_1 = st.number_input('cpc', key='2')
                    ctr_1 = st.number_input('ctr', key='2')
                    roi_1 = st.number_input('roi', key='2')
                    conversion_1 = st.number_input('conversion', key='2')
                    clicks_1 = st.number_input('clicks', key='2')
                    impression_1 = st.number_input('impression', key='2')
                    revenue_1 = st.number_input('revenue', key='2')
                    spent_1 = st.number_input('spent', key='2')
                    reach_1 = st.number_input('reach', key='2')
                    data_1 = pd.DataFrame({'name':name_1, 'cpm': cpm_1, 'cpc':cpc_1,
                                           'ctr':ctr_1,'roi':roi_1,'impression':impression_1,'conversion':conversion_1, 'clicks':clicks_1,                                                    'revenue':revenue_1,'spent':spent_1,'reach':reach_1}, index=[0])
                    
                    #append results input to sql
                    data_1.to_sql('user_campaigns', if_exists='append', con=con, index=False)
                    
                    #user_campaigns_2= user_campaigns.append(data_1, ignore_index=True)
                    #user_campaigns_2=user_campaigns.query('name !="na"')
                    
                    
                    #prediction
                    df_2 = pd.DataFrame({'Reach':reach_1,'Spent': spent_1}, index=[0])
                    pred_clicks_2=clicks_model.predict(df_2)
                    pred_clicks_2= pred_clicks_2.astype(int)
                    conversions_2 = pd.DataFrame({'Clicks':pred_clicks_2, 'Spent': spent_1})
                    pred_conversions_2=conversion_model.predict(conversions_2)
                    pred_conversions_2= pred_conversions_2.astype(int)
                    predictions_kpis_1= pd.DataFrame({'Reach':reach_1,'Spent': spent_1,'Clicks':pred_clicks_2, 
                                                    'Conversions':pred_conversions_2}, index=[0])
                    predictions_kpis_1['Impressions']= impression_1
                    predictions_kpis_1['Revenue']= predictions_kpis_1['Conversions']*r
                    predictions_kpis_1['ROI']=((predictions_kpis_1['Revenue']-predictions_kpis_1['Spent'])/predictions_kpis_1['Spent']*100)
                    predictions_kpis_1['CPC']=(predictions_kpis_1['Spent']/predictions_kpis_1['Clicks'])
                    predictions_kpis_1['CPM']=((predictions_kpis_1['Spent']/predictions_kpis_1['Impressions'])*1000)
                    predictions_kpis_1['CTR']=(predictions_kpis_1['Clicks']/predictions_kpis_1['Impressions']*100)
                    
                    #analysis
                    st.write("Comparison between your data and predicted data", key='2')
                    cpm_1=data_1['cpm'].reset_index()
                    cpm_1['CPM']=predictions_kpis_1['CPM']
                    cpm_1['your cpm']= cpm_1['cpm']
                    cpm_1['pred cpm']= cpm_1['CPM']
                    st.write(cpm_1[['your cpm','pred cpm']])
                    st.bar_chart(cpm_1[['your cpm','pred cpm']])
                    
                    cpc_1=data_1['cpc'].reset_index()
                    cpc_1['CPC']=predictions_kpis_1['CPC']
                    cpc_1['your cpc']= cpc_1['cpc']
                    cpc_1['pred cpc']= cpc_1['CPC']
                    st.write(cpc_1[['your cpc','pred cpc']])
                    st.bar_chart(cpc_1[['your cpc','pred cpc']])
                    
                    ctr_1=data_1['ctr'].reset_index()
                    ctr_1['CTR']=predictions_kpis_1['CTR']
                    ctr_1['your ctr']= ctr_1['ctr']
                    ctr_1['pred ctr']= ctr_1['CTR']
                    st.write(ctr_1[['your ctr','pred ctr']])
                    st.bar_chart(ctr_1[['your ctr','pred ctr']])
                    
                    roi_1=data_1['roi'].reset_index()
                    roi_1['ROI']=predictions_kpis_1['ROI']
                    roi_1['your roi']= roi_1['roi']
                    roi_1['pred roi']= roi_1['ROI']
                    st.write(roi_1[['your roi','pred roi']])
                    st.bar_chart(roi_1[['your roi','pred roi']])
                    
                    conv_1=data_1['conversion'].reset_index()
                    conv_1['Conversions']=predictions_kpis_1['Conversions']
                    conv_1['your conversions']=conv_1['conversion']
                    conv_1['pred conversions']=conv_1['Conversions']
                    st.write(conv_1[['your conversions','pred conversions']])
                    st.bar_chart(conv_1[['your conversions','pred conversions']])
                    
                    cl_1=data_1['clicks'].reset_index()
                    cl_1['Clicks']=predictions_kpis_1['Clicks']
                    cl_1['your clicks']= cl_1['clicks']
                    cl_1['pred clicks']= cl_1['Clicks']
                    st.write(cl_1[['your clicks','pred clicks']])
                    st.bar_chart(cl_1[['your clicks','pred clicks']])
                    
                    rev_1=data_1['revenue'].reset_index()
                    rev_1['Revenue']=predictions_kpis_1['Revenue']
                    rev_1['your revenue']= rev_1['revenue']
                    rev_1['pred revenue']= rev_1['Revenue']
                    st.write(rev_1[['your revenue','pred revenue']])
                    st.bar_chart(rev_1[['your revenue','pred revenue']])
                    
                    
                    st.write("Come back tomorrow for other analyses")
                if c == "no":
                    st.write(f"Never mind, maybe you want try a little bit more", key='2')
        else:
            st.write(f"You have to insert your name")
    if b == "no":
        st.write("Let's begin")
        name_3 = st.text_input("Insert your name", key='4')
        cpm_2 = st.number_input('cpm', key='3')
        cpc_2 = st.number_input('cpc', key='3')
        ctr_2 = st.number_input('ctr', key='3')
        roi_2 = st.number_input('roi', key='3')
        conversion_2 = st.number_input('conversion', key='3')
        clicks_2 = st.number_input('clicks', key='3')
        impression_2 = st.number_input('impression', key='3')
        revenue_2 = st.number_input('revenue', key='3')
        spent_2 = st.number_input('spent', key='3')
        reach_2 = st.number_input('reach', key='3')
        user_campaigns_2 = pd.DataFrame({'name':name_3, 'cpm': cpm_2, 'cpc':cpc_2,
                     'ctr':ctr_2,'roi':roi_2,'impression':impression_2,'conversion':conversion_2, 'clicks':clicks_2,           'revenue':revenue_2,'spent':spent_2,'reach':reach_2}, index=[0])
        #append results to sql
        user_campaigns_2.to_sql('user_campaigns', if_exists='append', con=con, index=False)
        
        
        #user_campaigns= user_campaigns.append(user_campaigns_2, ignore_index=True)
        #user_campaigns=user_campaigns.query('name !="na"')
        #user_campaigns=user_campaigns.query('name ==@name_3')
        
        #prediction
        df_3 = pd.DataFrame({'Reach':reach_2,'Spent': spent_2}, index=[0])
        pred_clicks_2=clicks_model.predict(df_3)
        pred_clicks_2= pred_clicks_2.astype(int)
        conversions_2 = pd.DataFrame({'Clicks':pred_clicks_2, 'Spent': spent_2})
        pred_conversions_2=conversion_model.predict(conversions_2)
        pred_conversions_2= pred_conversions_2.astype(int)
        predictions_kpis_2= pd.DataFrame({'Reach':reach_2,'Spent': spent_2,'Clicks':pred_clicks_2, 'Conversions':pred_conversions_2}, index=[0])
        predictions_kpis_2['Impressions']= impression_2
        predictions_kpis_2['Revenue']= predictions_kpis_2['Conversions']*r
        predictions_kpis_2['ROI']=((predictions_kpis_2['Revenue']-predictions_kpis_2['Spent'])/predictions_kpis_2['Spent']*100)
        predictions_kpis_2['CPC']=(predictions_kpis_2['Spent']/predictions_kpis_2['Clicks'])
        predictions_kpis_2['CPM']=((predictions_kpis_2['Spent']/predictions_kpis_2['Impressions'])*1000)
        predictions_kpis_2['CTR']=(predictions_kpis_2['Clicks']/predictions_kpis_2['Impressions']*100)
        
        
        #analysis
        st.write("Comparison between your data and predicted data", key='3')
        cpm_2=user_campaigns_2['cpm'].reset_index()
        cpm_2['CPM']=predictions_kpis_2['CPM']
        cpm_2['your cpm']= cpm_2['cpm']
        cpm_2['pred cpm']= cpm_2['CPM']
        st.write(cpm_2[['your cpm','pred cpm']])
        st.bar_chart(cpm_2[['your cpm','pred cpm']])
        
        cpc_2=user_campaigns_2['cpc'].reset_index()
        cpc_2['CPC']=predictions_kpis_2['CPC']
        cpc_2['your cpc']= cpc_2['cpc']
        cpc_2['pred cpc']= cpc_2['CPC']
        st.write(cpc_2[['your cpc','pred cpc']])
        st.bar_chart(cpc_2[['your cpc','pred cpc']])
        
        ctr_2=user_campaigns_2['ctr'].reset_index()
        ctr_2['CTR']=predictions_kpis_2['CTR']
        ctr_2['your ctr']= ctr_2['ctr']
        ctr_2['pred ctr']= ctr_2['CTR']
        st.write(ctr_2[['your ctr','pred ctr']])
        st.bar_chart(ctr_2[['your ctr','pred ctr']])
        
        roi_2=user_campaigns_2['roi'].reset_index()
        roi_2['ROI']=predictions_kpis_2['ROI']
        roi_2['your roi']= roi_2['roi']
        roi_2['pred roi']= roi_2['ROI']
        st.write(roi_2[['your roi','pred roi']])
        st.bar_chart(roi_2[['your roi','pred roi']])
        
        conv_2=user_campaigns_2['conversion'].reset_index()
        conv_2['Conversions']=predictions_kpis_2['Conversions']
        conv_2['your conversions']=conv_2['conversion']
        conv_2['pred conversions']=conv_2['Conversions']
        st.write(conv_2[['your conversions','pred conversions']])
        st.bar_chart(conv_2[['your conversions','pred conversions']])
        
        cl_2=user_campaigns_2['clicks'].reset_index()
        cl_2['Clicks']=predictions_kpis_2['Clicks']
        cl_2['your clicks']= cl_2['clicks']
        cl_2['pred clicks']= cl_2['Clicks']
        st.write(cl_2[['your clicks','pred clicks']])
        st.bar_chart(cl_2[['your clicks','pred clicks']])
        
        rev_2=user_campaigns_2['revenue'].reset_index()
        rev_2['Revenue']=predictions_kpis_2['Revenue']
        rev_2['your revenue']= rev_2['revenue']
        rev_2['pred revenue']= rev_2['Revenue']
        st.write(rev_2[['your revenue','pred revenue']])
        st.bar_chart(rev_2[['your revenue','pred revenue']])
        
        
        
        d =st.selectbox('Another one?',('','yes', 'no'), key='4')
        if d == "yes":
            cpm_3 = st.number_input('cpm', key='4')
            cpc_3 = st.number_input('cpc', key='4')
            ctr_3 = st.number_input('ctr', key='4')
            roi_3 = st.number_input('roi', key='4')
            conversion_3 = st.number_input('conversion', key='4')
            clicks_3 = st.number_input('clicks', key='4')
            impression_3 = st.number_input('impression', key='4')
            revenue_3 = st.number_input('revenue', key='4')
            spent_3 = st.number_input('spent', key='4')
            reach_3 = st.number_input('reach', key='4')
            data_2 = pd.DataFrame({'name':name_3, 'cpm': cpm_3, 'cpc':cpc_3,
                      'ctr':ctr_3,'roi':roi_3,'impression':impression_3,'conversion':conversion_3, 'clicks':clicks_3, 'revenue':revenue_3,'spent':spent_3,'reach':reach_3}, index=[0])
            
            #append results input to sql
            data_2.to_sql('user_campaigns', if_exists='append', con=con, index=False)
            #user_campaigns= user_campaigns.append(data_1, ignore_index=True)
            #user_campaigns=user_campaigns.query('name !="na"')
                    
                    
            #prediction
            df_3 = pd.DataFrame({'Reach':reach_3,'Spent': spent_3}, index=[0])
            pred_clicks_3=clicks_model.predict(df_3)
            pred_clicks_3= pred_clicks_3.astype(int)
            conversions_3 = pd.DataFrame({'Clicks':pred_clicks_3, 'Spent': spent_3})
            pred_conversions_3=conversion_model.predict(conversions_3)
            pred_conversions_3= pred_conversions_3.astype(int)
            predictions_kpis_3= pd.DataFrame({'Reach':reach_3,'Spent': spent_3,'Clicks':pred_clicks_3, 
                                                    'Conversions':pred_conversions_3}, index=[0])
            predictions_kpis_3['Impressions']= impression_3
            predictions_kpis_3['Revenue']= predictions_kpis_3['Conversions']*r
            predictions_kpis_3['ROI']=((predictions_kpis_3['Revenue']-predictions_kpis_3['Spent'])/predictions_kpis_3['Spent']*100)
            predictions_kpis_3['CPC']=(predictions_kpis_3['Spent']/predictions_kpis_3['Clicks'])
            predictions_kpis_3['CPM']=((predictions_kpis_3['Spent']/predictions_kpis_3['Impressions'])*1000)
            predictions_kpis_3['CTR']=(predictions_kpis_3['Clicks']/predictions_kpis_3['Impressions']*100)
                    
             #analysis
            st.write("Comparison between your data and predicted data", key='4')
            cpm_3=data_2['cpm'].reset_index()
            cpm_3['CPM']=predictions_kpis_3['CPM']
            cpm_3['your cpm']= cpm_3['cpm']
            cpm_3['pred cpm']= cpm_3['CPM']
            st.write(cpm_3[['your cpm','pred cpm']])
            st.bar_chart(cpm_3[['your cpm','pred cpm']])
            
            
            cpc_3=data_2['cpc'].reset_index()
            cpc_3['CPC']=predictions_kpis_3['CPC']
            cpc_3['your cpc']= cpc_3['cpc']
            cpc_3['pred cpc']= cpc_3['CPC']
            st.write(cpc_3[['your cpc','pred cpc']])
            st.bar_chart(cpc_3[['your cpc','pred cpc']])
            
            
            ctr_3=data_2['ctr'].reset_index()
            ctr_3['CTR']=predictions_kpis_3['CTR']
            ctr_3['your ctr']= ctr_3['ctr']
            ctr_3['pred ctr']= ctr_3['CTR']
            st.write(ctr_3[['your ctr','pred ctr']])
            st.bar_chart(ctr_3[['your ctr','pred ctr']])
            
            
            roi_3=data_2['roi'].reset_index()
            roi_3['ROI']=predictions_kpis_3['ROI']
            roi_3['your roi']= roi_3['roi']
            roi_3['pred roi']= roi_3['ROI']
            st.write(roi_3[['your roi','pred roi']])
            st.bar_chart(roi_3[['your roi','pred roi']])
            
            
            conv_3=data_2['conversion'].reset_index()
            conv_3['Conversions']=predictions_kpis_3['Conversions']
            conv_3['your conversions']=conv_3['conversion']
            conv_3['pred conversions']=conv_3['Conversions']
            st.write(conv_3[['your conversions','pred conversions']])
            st.bar_chart(conv_3[['your conversions','pred conversions']])
            
            
            cl_3=data_2['clicks'].reset_index()
            cl_3['Clicks']=predictions_kpis_3['Clicks']
            cl_3['your clicks']= cl_3['clicks']
            cl_3['pred clicks']= cl_3['Clicks']
            st.write(cl_3[['your clicks','pred clicks']])
            st.bar_chart(cl_3[['your clicks','pred clicks']])
            
            
            rev_3=data_2['revenue'].reset_index()
            rev_3['Revenue']=predictions_kpis_3['Revenue']
            rev_3['your revenue']= rev_3['revenue']
            rev_3['pred revenue']= rev_3['Revenue']
            st.write(rev_3[['your revenue','pred revenue']])
            st.bar_chart(rev_3[['your revenue','pred revenue']])
                    
                    
            
            st.write("Come back tomorrow for other analyses")
        if d == "no":
            st.write(f"Never mind, maybe you want try a little bit more")
    


st.write("""
### CAMPAIGN RECOMMENDER
 
""")
adv= pd.read_csv('./Advertising_Data4.csv')
pd.options.display.float_format = "{:,.2f}".format
creative_adv = []
for i in range(0,884):
    creative =['video','image','carousal']
    n = random.choice(creative)
    creative_adv.append(n)
adv['Creative']=creative_adv
adv['Spent']=adv['Spent'].astype(int)
adv['Revenue']=adv['Conversion']*10
adv['ROI']=((adv['Revenue']-adv['Spent'])/adv['Spent']*100)
adv['CPC']=(adv['Spent']/adv['Clicks']).round(decimals=2)
adv['CPM']=((adv['Spent']/adv['Impressions'])*1000).round(decimals=2)
adv['CTR']=(adv['Clicks']/adv['Impressions']*100).round(decimals=2)
adv_item_based=adv.query('CPM <=10 & ROI >0')


x = st.selectbox('Do you like some recommandation based on the creative?',('video', 'image','carousal'))
rec= adv_item_based.query('Creative == @x')
rec=rec[['Impressions','Clicks','Spent','Revenue','CPM','CPC','ROI']].sample(3)
st.write(rec)