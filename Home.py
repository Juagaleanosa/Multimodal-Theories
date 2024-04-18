import streamlit as st
import pandas as pd
import time
import streamlit.components.v1 as components
import mpld3
from utils import procesar_caso, obtener_casos, graf_2d, scatter_2d, scatter_3d

st.set_page_config(
    page_title="Home",
    page_icon="🏚️",
)

st.title('Philo Data Grapher')

# Agrega una caja con el texto deseado
st.markdown("""
    <div style="background-color: #D2A8FF; padding: 10px; border-radius: 10px;">
        <p style="text-align: center; color: #3A3B46;">
           <big><strong>Para citar esta aplicación: </strong></big> Dávila, M. V., Tamayo, A. Ó. E., Galeano, S. J. A. (2024). Philodatagrapher (versión 1) [Aplicación móvil].Streamlit.app.<ahttps://philodatagrapher.streamlit.app>https://philodatagrapher.streamlit.app</a>.
        </p>
    </div>
""", unsafe_allow_html=True)

def _max_width_(prcnt_width:int = 75):
    max_width_str = f"max-width: {prcnt_width}%;"
    st.markdown(f""" 
                <style> 
                .main .block-container{{
                    {max_width_str}
                }}
                """, 
                unsafe_allow_html=True,
    )

def _scripts():
    components.html(""" 
                <script>
                    let iframes = document.getElementsByTagName('iframe');

                    for (const iframe of iframes) {
                        iframe.setAttribute('sandbox', 'allow-forms allow-popups allow-same-origin');
                    }

                    for (const iFrame of iframes) {
                        let content = iFrame.contentDocument;
                        let body = content.body;
                        body.style.textAlign = 'center';
                    }

                    document.addEventListener("DOMContentLoaded", (event) => {
                        let iframes = document.getElementsByTagName('iframe');
                        for (const iFrame of iframes) {
                            let content = iFrame.contentDocument;
                            let body = content.body;
                            body.style.textAlign = 'center';
                        }
                    });
                </script>
                """
    )

_max_width_(90)

if "desactivar_select" not in st.session_state:
    st.session_state.desactivar_select = False

def update_caso_select():
    st.session_state.desactivar_select = not st.session_state.desactivar_select

def update_caso_select_2():
    if st.session_state.desactivar_select:
        st.session_state.desactivar_select = False

csv_cargado = False
caso_elegido = False


# Sidebar
add_title = st.sidebar.title("Sube tu archivo")

uploaded_file = st.sidebar.file_uploader("Elija un archivo", type=['csv'], on_change=update_caso_select_2)
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    csv_cargado = True
    casos = obtener_casos(df)

add_title = st.sidebar.title("Casos")
if (csv_cargado):
    caso_select = st.sidebar.selectbox(
        label="Elija un caso",
        options=casos,
        index=0,
        disabled=st.session_state.desactivar_select
    )
    st.sidebar.write(' ')
    st.sidebar.write(' ')
    button = st.sidebar.button("Generar gráficos", type="primary", on_click=update_caso_select)
    if button:
        caso_elegido = True
else:
    caso_select_oculto = st.sidebar.selectbox(
        label="Elija un caso",
        options=("Caso 1", "Caso 2"),
        index=0,
        disabled=True
    )
    st.sidebar.write(' ')
    st.sidebar.write(' ')
    button = st.sidebar.button("Generar gráficos", type="primary", disabled=True)
    button_2 = st.sidebar.button("Limpiar", disabled=True)
    


# Main screen
if (csv_cargado == False):
    while (csv_cargado == False):
        i = 10
        with st.spinner('Esperando archivo CSV...'):
            time.sleep(i)
else:
    succes_1 = st.success("Archivo CSV cargado exitosamente")
    if (caso_elegido == False):
        while (caso_elegido == False):
            i = 10
            with st.spinner('Esperando elección de caso y generar gráficos...'):
                time.sleep(i)
    else:
        if caso_elegido:
            succes_2 = st.success(f"{caso_select} seleccionado")
        time.sleep(1)

if button:
    succes_1.empty()
    succes_2.empty()

    progress_text = "Generando gráficos. Por favor espere."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.03)
        my_bar.progress(percent_complete + 1, text=progress_text)

    time.sleep(1)
    my_bar.empty()

    st.markdown(f'''#### :chart_with_upwards_trend: Has elegido el {caso_select}''')

    tab1, tab2, tab3, tab4 = st.tabs(["Todas", "Especialización", "Onda Semántica", "Especialización vs Semántica"])

    with tab1:
        # Parte 1
        with st.container():
            archivos_anims, df_filtrado_C, df_filtrado = procesar_caso(df, caso_select)
            nombres_vars_anims_esp = {}
            cols = st.columns(len(archivos_anims))
            if cols!= 1:
                for num, anim in enumerate(archivos_anims):
                    with cols[num]:
                        nombres_vars_anims_esp[num] = components.html(anim.to_jshtml(), width=590, height=490)
            else:
                anim = archivos_anims[0]
                components.html(anim.to_jshtml(), width=590, height=490)

        # Parte 2
        with st.container():
            fig_matplotlib = graf_2d(df_filtrado_C, caso_select)
            #st.pyplot(fig=fig_matplotlib, clear_figure=True, use_container_width=True)
            fig_html = mpld3.fig_to_html(fig_matplotlib)
            components.html(fig_html, height=600)

        col1_plotly, col2_plotly = st.columns(2)
        with st.container():
            with col1_plotly:
                # Parte 3
                fig_plotly_1 = scatter_2d(df_filtrado, df, caso_select)
                st.plotly_chart(fig_plotly_1, use_container_width=True, theme='streamlit', sharing="streamlit")
            
            with col2_plotly:
                # Parte 4
                fig_plotly_2 = scatter_3d(df_filtrado, df, caso_select)
                st.plotly_chart(fig_plotly_2, use_container_width=True, theme='streamlit', sharing="streamlit")
    
       with tab2:
            # Parte 1
            with st.container():
                archivos_anims, df_filtrado_C, df_filtrado = procesar_caso(df, caso_select)
                nombres_vars_anims_esp = {}
                cols = st.columns(len(archivos_anims))
                for num, anim in enumerate(archivos_anims):
                    with cols[num]:
                        nombres_vars_anims_esp[num] = components.html(anim.to_jshtml(), width=590, height=490)

    with tab3:
        # Parte 2
        with st.container():
            fig_matplotlib = graf_2d(df_filtrado_C, caso_select)
            #st.pyplot(fig=fig_matplotlib, clear_figure=True, use_container_width=True)
            fig_html = mpld3.fig_to_html(fig_matplotlib)
            components.html(fig_html, height=580)

    with tab4:
        col1_plotly, col2_plotly = st.columns(2) 
        with st.container():
            with col1_plotly:
                # Parte 3
                fig_plotly_1 = scatter_2d(df_filtrado, df, caso_select)
                st.plotly_chart(fig_plotly_1, use_container_width=True, theme='streamlit', sharing="streamlit")
            
            with col2_plotly:
                # Parte 4
                fig_plotly_2 = scatter_3d(df_filtrado, df, caso_select)
                st.plotly_chart(fig_plotly_2, use_container_width=True, theme='streamlit', sharing="streamlit")


if caso_elegido:
    placeholder = st.empty()
    with placeholder.container():
        st.sidebar.markdown(''':bulb: :red[Da click en Limpiar para gráficar otro caso]''')
    
    button_2 = st.sidebar.button("Limpiar", on_click=update_caso_select)

    if button_2:
        placeholder.empty()
        button_2 = st.sidebar.button("Limpiar", disabled=True)
        for num, anim in enumerate(archivos_anims):
            nombres_vars_anims_esp[num].empty()

#_scripts()
