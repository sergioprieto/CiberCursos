import streamlit as st
import openai

def generar_curriculo(api_key, descripcion, objetivos, duracion, nivel, temperature):
    openai.api_key = api_key
    context = []

    # UPDATE - V2
    # Pregunta 1
    plantilla1 = f"Descripción del curso: {descripcion}"
    context.append(plantilla1)

    # Pregunta 2
    plantilla2 = f"Objetivos del curso: {objetivos}"
    context.append(plantilla2)

    # Pregunta 3
    plantilla3 = f"La duración total del curso es de {duracion} horas."
    context.append(plantilla3)

    # Pregunta 4
    plantilla4 = f"El nivel del curso es {nivel}."
    context.append(plantilla4)

    # Generar currículo basado en el contexto completo
    plantilla_final = f"""
    Como especialista en el desarrollo de currículos, debes crear un esquema preliminar de un curso basado en la siguiente información: 
    {context}
    Sugiere una lista de capítulos preliminares junto con los temas que se cubrirán en cada capítulo. 
    Distribuye la duración total del curso entre los capítulos de manera no necesariamente equitativa, 
    pero asegurándote de que la suma de las horas de todos los temas sea igual a la duración total del curso. 
    Estos capítulos y temas estarán diseñados para cumplir con los objetivos del curso y se adaptarán al nivel especificado.
    Sugiere competencias, tareas y laboratorios para cada tema.
    Proporciona el resultado en formato Markdown, utilizando encabezados para los capítulos y viñetas para los temas, competencias, 
    tareas y laboratorios. Incluye la duración de cada capítulo y tema.
    """
    completion_final = openai.chat.completions.create(
        model="gpt-4o", messages=[{"role": "system", "content": plantilla_final}], temperature=temperature  # UPDATE - V2
    )
    curriculo_markdown = completion_final.choices[0].message.content

    # UPDATE - V2
    # Generar título del curso y descripción general
    plantilla_titulo = f"Sugiere un título apropiado para un curso con la siguiente descripción: {descripcion}"
    completion_titulo = openai.chat.completions.create(
        model="gpt-4o", messages=[{"role": "system", "content": plantilla_titulo}], temperature=temperature
    )
    titulo_curso = completion_titulo.choices[0].message.content

    plantilla_descripcion_general = f"Proporciona una descripción general concisa para un curso con la siguiente descripción: {descripcion}"
    completion_descripcion_general = openai.chat.completions.create(
        model="gpt-4o", messages=[{"role": "system", "content": plantilla_descripcion_general}], temperature=temperature
    )
    descripcion_general = completion_descripcion_general.choices[0].message.content

    # UPDATE - V2
    # Generar bibliografía sugerida
    plantilla_bibliografia = f"Sugiere una lista de 5 recursos bibliográficos relevantes para un curso con la siguiente descripción: {descripcion}"
    completion_bibliografia = openai.chat.completions.create(
        model="gpt-4o", messages=[{"role": "system", "content": plantilla_bibliografia}], temperature=temperature
    )
    bibliografia_sugerida = completion_bibliografia.choices[0].message.content

    return titulo_curso, descripcion_general, curriculo_markdown, bibliografia_sugerida

def main():
    st.set_page_config(page_title="CiberCURSOS :books:", layout="wide")
    st.title("CiberCURSOS :books:")

    with st.sidebar:
        st.header("Configuración")
        api_key = st.text_input("Clave de API de OpenAI", type="password")
        
        # UPDATE - V2
        descripcion = st.text_area("Descripción del Curso")
        objetivos = st.text_area("Objetivos del Curso")
        duracion = st.text_input("Duración del Curso (en horas)")
        nivel = st.selectbox("Nivel del Curso", ("principiante", "intermedio", "avanzado"))
        temperature = st.slider("Temperatura del LLM", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
        
        generate_button = st.button("Generar Currículo")

    if generate_button:
        if api_key.strip() == "":
            st.error("Por favor, proporciona una clave de API válida.")
        elif descripcion.strip() == "" or objetivos.strip() == "" or duracion.strip() == "":
            st.error("Por favor, completa todos los campos de entrada.")
        else:
            titulo_curso, descripcion_general, curriculo_markdown, bibliografia_sugerida = generar_curriculo(api_key, descripcion, objetivos, duracion, nivel, temperature)
            
            # UPDATE - V2
            st.header("Título del Curso")
            st.write(titulo_curso)
            
            st.header("Descripción General del Curso")
            st.write(descripcion_general)
            
            st.header("Currículo del Curso")
            st.write(curriculo_markdown)
            
            st.header("Bibliografía Sugerida")
            st.write(bibliografia_sugerida)

if __name__ == "__main__":
    main()