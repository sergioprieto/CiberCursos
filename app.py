import streamlit as st
import openai

def generar_curriculo(api_key, input1, input2, input3):
    openai.api_key = api_key
    context = []

    # Pregunta 1
    plantilla1 = f"¿Cuál es la descripción y los objetivos del curso de {input1}?"
    completion1 = openai.chat.completions.create(
        model="gpt-4o", messages=[{"role": "system", "content": plantilla1}]
    )
    respuesta1 = completion1.choices[0].message.content
    context.append(f"Descripción y objetivos del curso: {respuesta1}")

    # Pregunta 2
    plantilla2 = f"La duración total del curso de {input1} es de {input2} horas."
    context.append(plantilla2)

    # Pregunta 3
    plantilla3 = f"El nivel del curso de {input1} es {input3}."
    context.append(plantilla3)

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
        model="gpt-4o", messages=[{"role": "system", "content": plantilla_final}]
    )
    curriculo_markdown = completion_final.choices[0].message.content

    print(curriculo_markdown)

    return curriculo_markdown

def main():
    st.set_page_config(page_title="CiberCURSOS :books:", layout="wide")
    st.title("CiberCURSOS :books:")

    with st.sidebar:
        st.header("Configuración")
        api_key = st.text_input("Clave de API de OpenAI", type="password")
        input1 = st.text_input("Descripción y objetivos del curso")
        input2 = st.text_input("Duración total del curso (en horas)")
        input3 = st.selectbox("Nivel del curso", ("principiante", "intermedio", "avanzado"))
        generate_button = st.button("Generar Currículo")

    if generate_button:
        if api_key.strip() == "":
            st.error("Por favor, proporciona una clave de API válida.")
        elif input1.strip() == "" or input2.strip() == "":
            st.error("Por favor, completa todos los campos de entrada.")
        else:
            curriculo_markdown = generar_curriculo(api_key, input1, input2, input3)
            st.write(curriculo_markdown)

if __name__ == "__main__":
    main()