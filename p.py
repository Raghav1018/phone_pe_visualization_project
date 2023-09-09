import psycopg2
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
import requests
import json
import time

conn = psycopg2.connect(
    host="localhost",
    database="visual_phonepe",
    user="postgres",
    password="Rm071018")

conn.autocommit = True
cr= conn.cursor()


st.title(":violet[PhonePe Pulse]")
st.markdown(":violet[Welcome to the PhonePe Pulse Dashboard ,This PhonePe Pulse Data Visualization and Exploration dashboard is a user-friendly tool designed to provide insights and information about the data in the PhonePe Pulse GitHub repository. This dashboard offers a visually appealing and interactive interface for users to explore various metrics and statistics.]")

# Creating the side bars
with st.sidebar:
      selected = st.selectbox("Select a page", ["Top Performers", "Explore Data"])
if selected == "Top Performers":
    st.markdown("## :violet[Top 10 performers]")
Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
if Type == "Transactions":
        Data_segmentation = st.sidebar.selectbox("**Data segmentation**", ("State", "District", "Pincode"), key="Data segmentation_selectbox")
        col1,col2= st.columns([1,1.5],gap="large")
        with col1:
                Year = st.slider("**Select the Year**", min_value=2018, max_value=2022)
                Quarter = st.selectbox('**Select the Quarter**',('1','2','3','4'),key='qgwe2')
        with col2:
            st.write(
                """
                By accessing this pie chart, we will get to know about the top three insights in transactions like State, District and Pincode.
                """
                )

        if Data_segmentation == "State":
                cr.execute(f"""select  state, sum(transaction_count) as Total_Transactions_Count, sum(cast(transaction_amount AS NUMERIC)) AS Total_amount from agg_trans where year = {Year} and quarter = {Quarter} group by state order by Total_amount desc LIMIT 10 """)
                df = pd.DataFrame(cr.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
                title = "Top 10 Phonepe Transaction according to States"

                fig = px.pie(df, values='Transactions_Count',
                        names='State',
                        title=title,
                        color_discrete_sequence=px.colors.sequential.Magenta,
                        hover_data=['Total_Amount'],
                        labels={'Total_Amount':'Total Amount'})
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)
        if Data_segmentation == "District":
                cr.execute(f"""SELECT  district, state, sum(count) as Total_Count, sum(cast(amount as NUMERIC)) as Total_amount FROM map_trans WHERE year = {Year} AND quarter = {Quarter} GROUP BY district, state ORDER BY Total_amount DESC LIMIT 10""")
                df = pd.DataFrame(cr.fetchall(), columns=['District', 'State', 'Transactions_Count', 'Total_Amount'])

                fig = px.pie(df, values='Total_Amount',
                        names='District',
                        title='Top 10 Phonepe Transactions according to Districts',
                        color_discrete_sequence=px.colors.sequential.Magenta,
                        hover_data=['Transactions_Count'],
                        labels={'Transactions_Count': 'Transactions_Count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
        if Data_segmentation == "Pincode":
                cr.execute(f"""select  pincode, sum(transaction_count) as Total_Transactions_Count, sum(cast(transaction_amount as NUMERIC)) as Total_amount from top_trans where year = {Year} and quarter = {Quarter} group by pincode order by Total_amount desc LIMIT 10""")
                df = pd.DataFrame(cr.fetchall(), columns=['Pincode', 'Transactions_Count','Total_Amount'])
                fig = px.pie(df, values='Total_Amount',
                        names='Pincode',
                        title='Top 10 Phonepe Transactions according to Pincode',
                        color_discrete_sequence=px.colors.sequential.Magenta,
                        hover_data=['Transactions_Count'],
                        labels={'Transactions_Count':'Transactions_Count'})
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)
if Type == "Users":
        Data_segmentation = st.sidebar.selectbox("**Data segmentation**", ("Brands", "Registered_User", "Appopeners"), key="Data segmentation_selectbox")
        col1,col2= st.columns([1,1.5],gap="large")
        with col1:
            Year = st.slider("**Select the Year**", min_value=2018, max_value=2022)
            Quarter = st.selectbox('**Select the Quarter**',('1','2','3','4'),key='quat')
        with col2:
            st.write(
                """
                By accessing this donut chart, we will get to know about the top three insights in Users like Brands,Registered User, and Appopeners .
                """
                )
        if Data_segmentation == "Brands":
                cr.execute(f"""select brands, count(*) as Total_Count, avg(cast(percentage as NUMERIC))*100 as Avg_Percentage from agg_user where year = {Year} and quarter = {Quarter} group by brands order by Total_Count desc limit 10""")
                df = pd.DataFrame(cr.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
                st.write(df)
                fig = px.pie(df,
                        values='Total_Users',
                        names='Brand',
                        title='Top 10 Phonepe users according to Brands',
                        hole=0.5,
                        color='Avg_Percentage')
                st.plotly_chart(fig, use_container_width=True)

        if Data_segmentation == "Registered_User":
                cr.execute(f"""select   district, sum(registereduser) as Total_Registered_Users from map_user where year = {Year} and quarter = {Quarter} group by district order by Total_Registered_Users desc LIMIT 10""")
                df = pd.DataFrame(cr.fetchall(), columns=['District', 'Total_Registered_Users'])
                st.write(df)
                fig = px.pie(df,
                        title='Top 10 Phonepe users according to Districts',
                        values="Total_Registered_Users",
                        names="District",
                        hole = 0.5,
                        color='Total_Registered_Users')
                st.plotly_chart(fig, use_container_width=True)
        if Data_segmentation == "Appopeners":
                cr.execute(f"""SELECT  state, SUM(appopens) AS Total_Appopeners FROM map_user WHERE year = {Year} AND quarter = {Quarter} AND appopens > 0 GROUP BY state ORDER BY Total_Appopeners DESC LIMIT 10""")
                df = pd.DataFrame(cr.fetchall(), columns=['State','Total_Appopeners'])
                st.write(df)
                fig = px.pie(df, 
                        values='Total_Appopeners',
                        names='State',
                        title='Top 10 Phonepe users according to Appopeners',
                        hole=0.5,
                        color='Total_Appopeners')
                st.plotly_chart(fig, use_container_width=True)
# Exploring the data
if selected == "Explore Data":
    st.markdown("## :violet[Exploring the data]")
    Type = st.sidebar.selectbox("**Type**", ("Analysis of Transactions", "Users"))
    if Type == "Analysis of Transactions":
        col1,col2= st.columns([1,1.5],gap="large")
        with col1:
                        year_slider_key = "year_slider_" + str(hash("your_unique_identifier_here"))
                        Year = st.slider("**Select the Year**", min_value=2018, max_value=2022,key=year_slider_key)
                        quarter_key= f"quarter_{int(time.time())}"
                        Quarter = st.selectbox('**Select the Quarter**',('1','2','3','4'),key=quarter_key)
        with col2:
            st.write(
                """
                In this page , we will get to know about the insights of transactions count According To District,Transaction Types vs Total Transactions amount and Geomap visualization to show the State based data according to Transaction count and Transaction amount .
                """
                )
        st.markdown("## :violet[**Transaction Count According To District**]")
        selected_state = st.selectbox("**please select any State to visualize**",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=22,key="state_to_selectbox")
         
        cr.execute(f"""select state, district,year,quarter, sum(count) as Total_Transactions_count from map_trans where year = {Year} and quarter = {Quarter} and state = '{selected_state}' group by state, district,year,quarter order by state,district""")
        
        df1 = pd.DataFrame(cr.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions_count'])
        fig = px.bar(df1,
                     title='Transaction Count According To District' ,
                     x="District",
                     y="Total_Transactions_count",
                     orientation='v',
                     color='Total_Transactions_count',
                     color_continuous_scale=px.colors.sequential.Magenta)
        st.plotly_chart(fig,use_container_width=True)
        st.markdown("## :violet[payment type]")
        selected_state = st.selectbox("**please select any State to visualize**",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),key="state_selectbox")
        Type = st.selectbox('**Please select the values to visualize**', ('Transaction_count', 'Transaction_amount'))
        if Type == "Transaction_count":
                        cr.execute(f"""select transaction_type, sum(transaction_count) as Total_Transactions_count from agg_trans where year= {Year} and quarter = {Quarter} group by transaction_type order by Transaction_type""")
                        df = pd.DataFrame(cr.fetchall(), columns=['Transaction_type', 'Total_Transactions_count'])
                        fig = px.bar(df,
                                title='Transaction Types vs Total_Transactions_count',
                                x="Transaction_type",
                                y="Total_Transactions_count",
                                orientation='v',
                                color='Transaction_type',
                                color_continuous_scale=px.colors.sequential.Magenta)
                        st.plotly_chart(fig,use_container_width=False)
        if Type == "Transaction_amount":
                        cr.execute(f"""select transaction_type, sum(transaction_amount) as Total_Transaction_amount from agg_trans where year= {Year} and quarter = {Quarter} group by transaction_type order by Transaction_type""")
                        df = pd.DataFrame(conn.fetchall(), columns=['Transaction_type', 'Total_Transactions_amount'])
                        fig = px.bar(df,
                                title='Transaction Types vs Total_Transactions_amount',
                                x="Transaction_type",
                                y="Total_Transactions_amount",
                                orientation='v',
                                color='Transaction_type',
                                color_continuous_scale=px.colors.sequential.Magenta)
                        st.plotly_chart(fig,use_container_width=False)
       #geomap
        select1 = st.selectbox("Select a any one", ["Transaction count","Transaction amount"])
        st.markdown(":violet[This Geomap used to show the State based data according to Transaction count andTransaction amount ]")
        cr.execute(f"""select State, sum(count) as Total_Transaction_count, sum(cast(amount as NUMERIC)) as Total_Transaction_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state """)
        df1 = pd.DataFrame(cr.fetchall(), columns=['State', 'Total_Transaction_count', 'Total_Transaction_amount'])
        State_name = r"C:\Users\mahes\Desktop\STUDY\Guvi\Phone_pay\Statenames.csv"
        data= pd.read_csv(State_name)
        df1.State = data
        if select1 == "Transaction amount":
                    fig1= px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        locations='State',
                        color='Total_Transaction_amount',
                        color_continuous_scale='Aggrnyl')

                    fig1.update_geos(fitbounds="locations", visible=False)
                    st.plotly_chart(fig1,use_container_width=True)
        if select1 == "Transaction count":
                    fig2= px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        locations='State',
                        color='Total_Transaction_count',
                        color_continuous_scale='Aggrnyl')

                    fig2.update_geos(fitbounds="locations", visible=False)
                    st.plotly_chart(fig2,use_container_width=True)
             
    if Type == "Users":
        Data_segmentation = st.sidebar.selectbox("**Data segmentation**", ( "Registered Users","Analysis of country"), key="Data_selectbox")
        col1,col2= st.columns([1,1.5],gap="large")
        with col1:
            year_slider_key = "year_slider_" + str(hash("your_unique_identifier_here"))
            Year = st.slider("**Select the Year**", min_value=2018, max_value=2022,key=year_slider_key)
            Quarter = st.selectbox('**Select the Quarter**',('1234'),key='quart')
        if Data_segmentation == "Registered Users": 
                st.markdown("## :violet[Total Numbers Of Registered Users  According to Districts]")
                selected_state = st.selectbox("**Select any state to fetch the data**",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=1)
        
                cr.execute(f"""select state,year,quarter,district,sum(registereduser) as Total_Registered_Users from map_user where year = {Year} and quarter = {Quarter} and state = '{selected_state}' group by state, district,year,quarter order by state,district""")
                df = pd.DataFrame(cr.fetchall(), columns=['State','Year', 'Quarter', 'District','Total_Registered_Users'])
                fig = px.bar(df,
                     x="District",
                     y="Total_Registered_Users",
                     orientation='v',
                     color="Total_Registered_Users",
                     color_continuous_scale=px.colors.sequential.Magenta)
                st.plotly_chart(fig,use_container_width=True)

        if Data_segmentation == "Analysis of country":
                st.markdown(":violet[This Geomap used to show the State based data according to Registered users and App_Openers ]")
                cr.execute(f"""select state, sum(registereduser) as Registered_Users, sum(appopens) as App_Opens from map_user where year={Year} and quarter={Quarter} group by state""")
                df1 = pd.DataFrame(cr.fetchall(), columns=["State", "Registered_Users", "AppOpens"])
                State_name = r"C:\Users\mahes\Desktop\STUDY\Guvi\Phone_pay\Statenames.csv"
                data= pd.read_csv(State_name)
                df1.State = data
                fig = px.choropleth(df1,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey="properties.ST_NM",
                        locations="State",
                        color="Registered_Users",
                        hover_data=["State", "Registered_Users", "AppOpens"],
                        color_continuous_scale=px.colors.sequential.Magenta)
                fig.update_geos(fitbounds="locations", visible=False)
                fig.update_layout(height=600, width=800)
                st.plotly_chart(fig, use_container_width=False, key='choropleth_chart')
 


