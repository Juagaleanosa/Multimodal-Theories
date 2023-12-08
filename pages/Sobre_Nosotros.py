import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

st.set_page_config(
    page_title="Sobre Nosotros",
    page_icon="📄"
)

def _max_width_(prcnt_width:int = 75):
    max_width_str = f"max-width: {prcnt_width}%;"
    st.markdown(f""" 
                <style> 
                .main .block-container{{{max_width_str}}}

                [class^="st-emotion-cache-"] column {{
                    display: flex;
                    justify-content: center;
                    text-align: center;
                }}

                [class^="st-emotion-cache-"] img {{
                    text-align: center;
                }}

                """, 
                unsafe_allow_html=True,
    )

_max_width_(75)


st.title("Sobre Nosotros")

st.write(' ')
st.write(' ')

with st.container():
    col1, col2, col3, col4 = st.columns([0.15, 0.35, 0.45, 0.05])
    with col2:
        image = Image.open('multimedia/veronica.jpg')
        st.image(image, width=280)
    with col3:
        st.markdown("""
                #### Verónica Dávila Manrique
                Licenciada en Filosofía y Letras - Universidad de Caldas <br>
                Magister en Educación - Universidad de Caldas <br>
                Especialista en Gerencia Educativa - Universidad Católica de Manizales <br>
                Candidata a Doctora en Educación - Universidad de Caldas <br>
                Joven investigadora de Colciencias (2014-2015) <br><br>
                veronica.davila@ucaldas.edu.co
                """,
                unsafe_allow_html=True,)
st.write(' ')

with st.container():
    col1, col2, col3, col4 = st.columns([0.15, 0.35, 0.45, 0.05])
    with col2:
        image = Image.open('multimedia/oscar.png')
        st.image(image, width=280)
    with col3:
        st.markdown("""
                #### Óscar Eugenio Tamayo Alzate
                Licenciado en Biología y Química - Universidad de Caldas <br>
                Magister en Desarrollo Educativo y Social - Universidad Pedagógica Nacional <br>
                Magister en Didáctica de las Ciencias Experimentales y de las Matemáticas - Universidad de Barcelona <br>
                Doctor en Didáctica de las Ciencias Experimentales y de las Matemáticas - Universidad de Barcelona <br><br>
                oscar.tamayo@ucaldas.edu.co
                """,
                unsafe_allow_html=True,)
st.write(' ')

with st.container():
    col1, col2, col3, col4 = st.columns([0.15, 0.35, 0.45, 0.05])
    with col2:
        image = Image.open('multimedia/julian.png')
        st.image(image, width=280)
    with col3:
        st.markdown("""
                #### Julian Alberto Galeano Sarmiento
                Estudiante de Ciencias Computacionales - Universidad Nacional de Colombia <br><br>
                juagaleanosa@unal.edu.co
                """,
                unsafe_allow_html=True,)