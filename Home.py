import streamlit as st
from PIL import Image

st.set_page_config(page_title='Home', page_icon='Sal')

#image_path = '/Users/fabri/Desktop/codigo/'
image = Image.open( 'logo.png')
st.sidebar.image( image, width=120) 

st.sidebar.markdown(' # Cury Company')
st.sidebar.markdown('Fest Delivery in Town')
st.sidebar.markdown('''----''')

st.write("# Painel de Crescimento da Curry Company")

st.markdown(
    """
### Painel de Crescimento

O Painel de Crescimento foi criado para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.

**Como utilizar o Painel de Crescimento**

*   **Visão da Empresa:**
    *   Visão Gerencial: Métricas gerais de desempenho.
    *   Visão Tática: Indicadores gerais de desempenho.
    *   Visão Geográfica: Insights de geolocalização.

*   **Visão do Entregador:**
    *   Acompanhamento dos indicadores semanais de crescimento.

---

**Precisa de Ajuda?**

*   Entre em contato com a Equipe de Ciência de Dados pelo e-mail: f.freitassilva.br@gmail.com
"""
)
