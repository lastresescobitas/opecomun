#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import json
import random

# Cargar las preguntas desde el archivo JSON
with open('preguntas.json', 'r', encoding='utf-8') as f:
    preguntas_dict = json.load(f)

def get_random_question():
    key = random.choice(list(preguntas_dict.keys()))
    pregunta = preguntas_dict[key]
    return key, pregunta

# Inicializar el estado de la sesión si no está ya inicializado
if 'current_question' not in st.session_state:
    st.session_state.current_question = get_random_question()
    st.session_state.show_answer = False
    st.session_state.selected_option = None

key, pregunta = st.session_state.current_question

st.title("Aplicación de Preguntas Tipo Test")

# Mostrar la pregunta con markdown y tamaño de letra uniforme
st.markdown(f"<div style='font-size: 20px'>{pregunta['pregunta']}</div>", unsafe_allow_html=True)

# Crear una lista de opciones que combine las claves con sus textos
opciones = [f"{opcion}) {texto}" for opcion, texto in pregunta['opciones'].items()]

# Mostrar las opciones en el radio button
st.session_state.selected_option = st.radio("Selecciona una opción:", opciones, index=opciones.index(st.session_state.selected_option) if st.session_state.selected_option else 0)

# Verificar respuesta
if st.button("Comprobar respuesta"):
    respuesta_correcta = pregunta['respuesta_correcta']
    respuesta_correcta_texto = f"{respuesta_correcta}) {pregunta['opciones'][respuesta_correcta]}"
    
    if st.session_state.selected_option == respuesta_correcta_texto:
        st.success("¡Correcto!")
    else:
        st.error(f"Incorrecto. La respuesta correcta es: {respuesta_correcta_texto}")
    
    st.session_state.show_answer = True

# Mostrar siempre el botón "Siguiente pregunta"
if st.button("Siguiente pregunta"):
    st.session_state.current_question = get_random_question()
    st.session_state.show_answer = False
    st.session_state.selected_option = None
    st.rerun()  # Usar experimental_rerun para actualizar la interfaz

# Mostrar la información de la pregunta
if st.button("Mostrar información"):
    st.info(f"ID de la pregunta: {key}")

# Mostrar feedback basado en el estado de show_answer
if st.session_state.show_answer:
    st.write("Respuesta mostrada")
else:
    st.write("Responda la pregunta")

