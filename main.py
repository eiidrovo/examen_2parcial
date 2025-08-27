import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import pandas as pd
import plotly.express as px


def production_plots(file):

    if file is not None:
        Well_Data = pd.read_excel(file, sheet_name='Monthly Production Data', skiprows=[1])
        st.success("File Loaded!")
    else:
        st.success('Waiting For File')
        st.stop()

    Well_Data['date'] = pd.to_datetime(Well_Data[['Year', 'Month']].assign(day=1))

    Selected_Well = st.selectbox(
        'Choose Well',
        options=Well_Data['Wellbore name'].unique()
    )
    fig = px.line(
        Well_Data[Well_Data['Wellbore name'] == Selected_Well],
        x='date',
        y=['Oil', 'Water', 'Gas'],
        labels={'value': 'Production', 'date': 'Time'},
        title='Productivity'
    )
    fig.update_layout(legend_title_text='Production [Sm3]')
    st.plotly_chart(fig, use_container_width=True)

    totals = Well_Data.groupby("Wellbore name")[
        ['Oil', 'Water', 'Gas']
    ].sum().reset_index()
    Selected_barplot = st.selectbox(
        'Choose Barplot to show',
        ['Oil', 'Water', 'Gas'],
    )

    fig = px.bar(
        totals,
        x="Wellbore name",
        y=f"{Selected_barplot}",
        title="Total Production by Well",
        labels={"value": "Volume", "variable": "Type"},
        barmode="group"
    )

    # Display in Streamlit
    st.subheader(f"📊 Total Production of {Selected_barplot} by Well")
    st.plotly_chart(fig)

icon= Image.open('Resources/Logo.png')
st.set_page_config(page_title="Proyecto", page_icon=icon)
FIMCM_Logo = Image.open('Resources/FIMCM_logo.png')
FICT_Logo = Image.open('Resources/FICT_logo.png')


with st.sidebar:
    seleccion = option_menu(
        "Main Menu",
        ["Home","Data", "Plots"],
        icons=["house", "bar-chart-line-fill", "graph-up-arrow","option"],
        menu_icon="list",
        default_index=0
    )
st.title(seleccion)

st.title("📊 Historial de producción del campo Volve -  Examen 2do parcial")
st.write("""
         El siguiente programa fue desarrollado por Esaú Idrovo, estudiante de la carrera
         de Ingeniería Naval en FIMCM-ESPOL para la materia de Softwares en Ingeniería de
         Petróleo PETG1029 en FICT-ESPOL.
""")
st.image(FIMCM_Logo)
st.caption("FIMC - Facultad de Ing. Marítima y Ciencias del Mar")
st.image(FICT_Logo)
st.caption("FICT - Facultad de Ing. en Ciencias de la Tierra")

st.markdown('''
A continuación se presentará el historial de produccion del campo volve y las cantidades de petroleo gas y agua producidos en total.
''')
file=None
if seleccion=='Data':
    file = st.file_uploader("Upload data to plot", type=["xlsx"])
elif seleccion=='Plots':
    file = st.file_uploader("Upload data to plot", type=["xlsx"])
    production_plots(file)
