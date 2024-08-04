# Libraries
import numpy as np
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

#biblioteca necessária
import pandas as pd
import streamlit as st
from datetime import datetime
from PIL import Image
import folium
from streamlit_folium import folium_static

st.set_page_config( page_title='Visão Empresa', page_icon='🗺️', layout='wide')

#================
#Funções
#================

def orde_by_week(df1):
    df_ax= df1.groupby('week_of_year') ['ID'].count().reset_index()
    df_ax2= df1.groupby(['week_of_year']) ['Delivery_person_ID'].nunique().reset_index()

    df_aux = pd.merge( df_ax, df_ax2, how='inner')
    df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    fig = px.line( df_aux, x='week_of_year', y='order_by_deliver')
    return fig

def traffic_order_City(df1):
    df_v = df1.groupby(['City','Road_traffic_density']) ['ID'].count().reset_index()
    df_v = df_v[df_v['City'] != 'NaN ']
    df_v = df_v[df_v['Road_traffic_density'] != 'NaN ']
    fig =px.scatter(df_v, x='City', y='Road_traffic_density', size='ID', color='City')
    return fig

def traffic_order_share(df1):
    df_aux = df1.groupby('Road_traffic_density') ['ID'].count().reset_index()
    df_aux = df_aux[df_aux['Road_traffic_density'] != 'NaN ']
    df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()
    fig = px.pie( df_aux, values= 'entregas_perc', names='Road_traffic_density')
    return fig

def order_metric(df1):
    df_aux = df1.groupby('Order_Date') ['ID'].count().reset_index()
    fig = px.bar( df_aux, x='Order_Date', y='ID')
    return fig

def clean_code(df1):
    #""" Esta funcao tem a responsabilidade de limpar o dataframe"""

    #   Tipos de limpeza:
    #    1. Remoção dos dados NaN
    #    2. Mudança do tipo da coluna de dados
    #    3. Formatação da coluna de Datas
    #    4. Limpeza da Coluna de Tempo

    #Input: Dataframe
    #Output: Dataframe

    # 1. Lidar com Valores Ausentes ('NaN') e Espaços em Branco:
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(str).str.strip()  # Converte para string e remove espaços em branco
    df1['Delivery_person_Age'] = pd.to_numeric(df1['Delivery_person_Age'], errors='coerce')  # Converte para numérico, preenchendo valores não numéricos com NaN

    # 2. Filtrar Valores NaN
    df1 = df1[df1['Delivery_person_Age'].notna()]  # Mantém apenas as linhas onde o valor não é NaN

    # 3. Converter para Inteiro (Com Segurança)
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int) 
    df1 = df1[df1['Road_traffic_density'] != 'NaN ']
    df1 = df1[df1['City'] != 'NaN ']


    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'])
    df1['Delivery_person_Ratings'] =  df1['Delivery_person_Ratings'].astype(float)
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(str).str.strip()
    df1['multiple_deliveries'] = pd.to_numeric(df1['multiple_deliveries'], errors= 'coerce')
    df1 = df1[df1['multiple_deliveries'].notna()] 
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(float)
    df1['week_of_year'] = df1['Order_Date'].dt.strftime( '%U') 

    df1['ID'] = df1['ID'].str.strip()
    df1['Road_traffic_density'] = df1['Road_traffic_density'].str.strip()

    return df1


#-------------------Inicio da Estrutura Lógica do código-------------------------
#======================
#Import dataset
#======================
df = pd.read_csv('train.csv')
df1 = df.copy()
df1 = clean_code (df1)


#VISÃO EMPRESA
df_aux = df1.groupby('Order_Date') ['ID'].count().reset_index()
px.bar( df_aux, x='Order_Date', y='ID')

#----------------------
#LAYOUT barra lateral
st.header('Visão do Cliente')

#image_path = 'logo.png'
image = Image.open('logo.png')
st.sidebar.image( image, width=120)

st.sidebar.markdown(' # Cury Company')
st.sidebar.markdown('Fest Delivery in Town')
st.sidebar.markdown('''----''')


# Controle deslizante da barra lateral
st.sidebar.markdown( '## Selecione uma data limite')
start_time = st.sidebar.slider(
    "Até qual valor?",
    value=datetime(2022, 4, 13),
    min_value=datetime(2022, 3, 19),
    max_value=datetime( 2022, 2, 16),
    format="MM/DD/YY",
)
st.sidebar.write("Start time:", start_time)
st.write(" ## Start time:", start_time)

st.sidebar.markdown("""---""")

traffic_option = st.sidebar.multiselect('Quais as condições do trânsito',['Low', 'Medium', 'High', 'Jam'],default=['Low','Medium', 'High', 'Jam'])                                      

st.sidebar.markdown("""---""")
st.sidebar.markdown( '### Powered by Fabri')

#filtro de data

df1= df1[df1['Order_Date'] < start_time]

#filtro de transito

df1 = df1[df1['Road_traffic_density'].isin(traffic_option)]
#any_match = df1['Road_traffic_density'].isin(traffic_option).

# Layout no streamlit

tab1, tab2, tab3 = st.tabs ( ['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container():
        #Orde Metric
        st.markdown('# Orders by Day')
        fig = order_metric(df1)
        st.plotly_chart(fig, use_container_width=True) 

    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            fig = traffic_order_share(df1)
            st.header('Traffic Order Share') 
            st.plotly_chart( fig, use_container_width=True)            

        with col2:
            st.header('Traffic Order City') 
            fig = traffic_order_City(df1)
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown(' # Orde_By_Week')
    fig = orde_by_week(df1)
    st.plotly_chart(fig, use_container_width=True)
   
with tab3:
    st.markdown('# Country Maps')

    # (Assumindo que você já tem o df1 criado com suas informações originais)
    df55 = df1[["City", "Road_traffic_density", "Delivery_location_latitude", "Delivery_location_longitude"]]

    # Remove linhas com valores ausentes (NaN) em "City" e "Road_traffic_density"
    df55 = df55.dropna(subset=["City", "Road_traffic_density"])

    # Calcula a mediana das coordenadas por cidade e tráfego (opcional)
    df55 = df55.groupby(["City", "Road_traffic_density"]).median().reset_index()

    # Criar mapa com foco na Índia
    mapa = folium.Map(location=[20.5937, 78.9629], zoom_start=5)  

    # Marcadores
    for index, location_info in df55.iterrows():
        folium.Marker(
            [location_info["Delivery_location_latitude"], location_info["Delivery_location_longitude"]],
            popup=f"Cidade: {location_info['City']}, Tráfego: {location_info['Road_traffic_density']}"
        ).add_to(mapa)

    # Exibir mapa no Streamlit
    #folium_static(mapa, width=1024, height=600) 
    mapa
