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
#from streamlit_folium import folium_static


st.set_page_config( page_title='Visão Entregador', page_icon='🛵', layout='wide')

##------------------------------------
##=============Funções================
##------------------------------------


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


#Import dataset
df = pd.read_csv('train.csv')
df1 = df.copy()
#Clean Dataset
df1 = clean_code(df1)

# =====================
## LAYOUT barra lateral
# =====================
st.header('Visão do Entregador')

#image_path = 'logo.png'
image = Image.open('logo.png')
st.sidebar.image( image, width=120)

st.sidebar.markdown(' # Cury Company')
st.sidebar.markdown('Fest Delivery in Town')
st.sidebar.markdown('''----''')

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
#date_slider = st.sidebar.slider( 'Ate qual Valor?', value=pd.to_datetime(2022, 4, 13), min_value=pd.to_datetime(2022, 2, 11), max_value=pd.to_datetime(2022, 4, 6),format= '%d-%m-%Y')


# Controle deslizante da barra lateral
#date_slider = st.sidebar.slider(
   ## max_value=pd.to_datetime("2022-03-25"),  # Valor máximo ajustado
   # format="%d-%m-%Y"


# Exibir data selecionada
#st.header(date_slider.strftime("%d-%m-%Y"))
st.sidebar.markdown("""---""")

traffic_option = st.sidebar.multiselect('Quais as condições do trânsito',['Low', 'Medium', 'High', 'Jam'],default=['Low','Medium', 'High', 'Jam'])                                      

st.sidebar.markdown("""---""")
st.sidebar.markdown( '### Powered by Fabri')

#filtro de data

df1= df1[df1['Order_Date'] < start_time]

#filtro de transito

df1 = df1[df1['Road_traffic_density'].isin(traffic_option)]
#any_match = df1['Road_traffic_density'].isin(traffic_option).


#==========================
# Layout no streamlit
#==========================

tab1, tab2, tab3 = st.tabs ( ['Visão Gerencial', '_', '_'])

with tab1:
    with st.container():
        st.title( ' Overrall Metrics')
        col1, col2, col3, col4 = st.columns(4, gap='large')
        with col1:
            
            idade = df1['Delivery_person_Age'].max()
            col1.metric('Maior de idade', idade)
        
        with col2:
            
            idade_menor = df1['Delivery_person_Age'].min()
            col2.metric('Menor idade', idade_menor)


        with col3:
              
            veiculo_m= df1['Vehicle_condition'].max()
            col3.metric('Melhor Condição', veiculo_m)

        with col4:
              
            veiculo_p= df1['Vehicle_condition'].min()
            col4.metric('Melhor Condição', veiculo_p) 

    with st.container():
        st.markdown( """---""")
        st.title('Avaliações')

        col1, col2 =st.columns(2)
        with col1:
            st.markdown('<h3 style="font-size:18px;">Avaliação médias por Entregador</h3>', unsafe_allow_html=True)
            novo_df= df1[['Delivery_person_Ratings', 'Delivery_person_ID']]
            novo_df.groupby('Delivery_person_ID') ['Delivery_person_Ratings'].mean().reset_index()
            st.dataframe( novo_df)

        with col2:
            st.markdown('<h3 style="font-size:18px;">Avaliação média por Trânsito</h3>', unsafe_allow_html=True)
            df_des = df1[['Delivery_person_Ratings', 'Road_traffic_density' ]].groupby('Road_traffic_density').agg(['mean', 'std']).reset_index()
            st.dataframe(df_des)

            st.markdown('<h3 style="font-size:18px;">Avaliação média por Clima</h3>', unsafe_allow_html=True)
            df_clima=df1[['Delivery_person_Ratings', 'Weatherconditions']].groupby('Weatherconditions').agg(['mean', 'std']).reset_index()
            st.dataframe(df_clima)

    with st.container(): 
        st.markdown('''---''')
        st.title( ' Velocidade de Entrega')  

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('##### Top Entregadores Mais Rapidos')
            df2 = df1.groupby(['City', 'Delivery_person_ID' ]) ['Time_taken(min)'].min().reset_index().sort_values(['City', 'Time_taken(min)'])
            df2.groupby('City').head(10).reset_index()
            st.dataframe(df2)
        with col2:
            st.markdown('##### Top Entregadores mais lentos')
    


            df2 = df1.groupby(['City', 'Delivery_person_ID' ]) ['Time_taken(min)'].min().reset_index().sort_values(['City', 'Time_taken(min)'],ascending= False)
            df2.groupby('City').head(10).reset_index()
            st.dataframe(df2)


