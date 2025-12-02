"""
FIBRA Content Management System
Streamlit application for managing educational content
"""

import streamlit as st
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))

import db_utils

# Page configuration
st.set_page_config(
    page_title="FIBRA CMS",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<div class="main-header">📚 FIBRA - Sistema de Gestión de Contenido</div>', unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navegación")
page = st.sidebar.radio(
    "Selecciona una sección:",
    ["🏠 Inicio", "📖 Cursos", "📑 Unidades", "📝 Lecciones", "🎯 Desafíos", "📋 Exámenes", "📤 Carga Masiva"]
)

# Test database connection
try:
    conn = db_utils.get_db_connection()
    conn.close()
    st.sidebar.success("✅ Conectado a la base de datos")
except Exception as e:
    st.sidebar.error(f"❌ Error de conexión: {str(e)}")
    st.error("No se puede conectar a la base de datos. Verifica tu archivo .env")
    st.stop()

# ==================== HOME PAGE ====================
if page == "🏠 Inicio":
    st.markdown("## Bienvenido al Sistema de Gestión de Contenido de FIBRA")
    
    st.markdown("""
    Esta aplicación te permite gestionar todo el contenido educativo de FIBRA:
    
    ### 📋 Funcionalidades disponibles:
    
    - **📖 Cursos**: Crear, editar y eliminar cursos
    - **📑 Unidades**: Gestionar unidades dentro de cada curso
    - **📝 Lecciones**: Administrar lecciones de cada unidad
    - **🎯 Desafíos**: Crear desafíos y sus opciones de respuesta
    - **📤 Carga Masiva**: Importar contenido desde archivos CSV
    
    ### 🚀 Cómo empezar:
    
    1. Selecciona una sección en el menú lateral
    2. Usa los formularios para crear o editar contenido
    3. Los cambios se guardan automáticamente en la base de datos
    
    ### ⚠️ Importante:
    
    - Asegúrate de tener un backup de la base de datos antes de hacer cambios masivos
    - Los cambios son permanentes y afectan la base de datos de producción
    - Verifica siempre los datos antes de guardar
    """)
    
    # Show statistics
    st.markdown("### 📊 Estadísticas del contenido")
    
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        courses = db_utils.get_courses()
        units = db_utils.get_units()
        lessons = db_utils.get_lessons()
        challenges = db_utils.get_challenges()
        
        with col1:
            st.metric("Cursos", len(courses))
        with col2:
            st.metric("Unidades", len(units))
        with col3:
            st.metric("Lecciones", len(lessons))
        with col4:
            st.metric("Desafíos", len(challenges))
    except Exception as e:
        st.error(f"Error al cargar estadísticas: {str(e)}")

# ==================== COURSES PAGE ====================
elif page == "📖 Cursos":
    st.markdown("## Gestión de Cursos")
    
    tab1, tab2 = st.tabs(["📋 Ver Cursos", "➕ Crear/Editar Curso"])
    
    with tab1:
        st.markdown("### Cursos existentes")
        try:
            courses = db_utils.get_courses()
            if courses:
                for course in courses:
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"**{course['title']}** (ID: {course['id']})")
                        st.caption(f"Imagen: {course['image_src']}")
                    with col2:
                        if st.button("✏️ Editar", key=f"edit_course_{course['id']}"):
                            st.session_state['edit_course'] = course
                            st.rerun()
                    with col3:
                        if st.button("🗑️ Eliminar", key=f"delete_course_{course['id']}"):
                            if st.session_state.get(f"confirm_delete_course_{course['id']}", False):
                                db_utils.delete_course(course['id'])
                                st.success(f"Curso '{course['title']}' eliminado")
                                st.rerun()
                            else:
                                st.session_state[f"confirm_delete_course_{course['id']}"] = True
                                st.warning("Haz clic de nuevo para confirmar")
                    st.divider()
            else:
                st.info("No hay cursos creados aún")
        except Exception as e:
            st.error(f"Error al cargar cursos: {str(e)}")
    
    with tab2:
        st.markdown("### Crear o editar curso")
        
        # Check if editing
        edit_course = st.session_state.get('edit_course', None)
        
        with st.form("course_form"):
            title = st.text_input("Título del curso", value=edit_course['title'] if edit_course else "")
            image_src = st.text_input("URL de la imagen", value=edit_course['image_src'] if edit_course else "")
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("💾 Guardar")
            with col2:
                cancel = st.form_submit_button("❌ Cancelar")
            
            if submit and title and image_src:
                try:
                    if edit_course:
                        db_utils.update_course(edit_course['id'], title, image_src)
                        st.success(f"Curso '{title}' actualizado correctamente")
                        st.session_state.pop('edit_course', None)
                    else:
                        course_id = db_utils.create_course(title, image_src)
                        st.success(f"Curso '{title}' creado con ID: {course_id}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al guardar curso: {str(e)}")
            elif submit:
                st.error("Por favor completa todos los campos")
            
            if cancel:
                st.session_state.pop('edit_course', None)
                st.rerun()

# ==================== UNITS PAGE ====================
elif page == "📑 Unidades":
    st.markdown("## Gestión de Unidades")
    
    tab1, tab2 = st.tabs(["📋 Ver Unidades", "➕ Crear/Editar Unidad"])
    
    with tab1:
        st.markdown("### Unidades existentes")
        
        # Course filter
        try:
            courses = db_utils.get_courses()
            if courses:
                course_options = {c['id']: c['title'] for c in courses}
                selected_course = st.selectbox(
                    "Filtrar por curso:",
                    options=[None] + list(course_options.keys()),
                    format_func=lambda x: "Todos los cursos" if x is None else course_options[x]
                )
                
                units = db_utils.get_units(selected_course)
                if units:
                    for unit in units:
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            st.write(f"**{unit['title']}** (ID: {unit['id']}, Orden: {unit['order']})")
                            st.caption(f"Descripción: {unit['description']}")
                            st.caption(f"Curso ID: {unit['course_id']}")
                        with col2:
                            if st.button("✏️ Editar", key=f"edit_unit_{unit['id']}"):
                                st.session_state['edit_unit'] = unit
                                st.rerun()
                        with col3:
                            if st.button("🗑️ Eliminar", key=f"delete_unit_{unit['id']}"):
                                if st.session_state.get(f"confirm_delete_unit_{unit['id']}", False):
                                    db_utils.delete_unit(unit['id'])
                                    st.success(f"Unidad '{unit['title']}' eliminada")
                                    st.rerun()
                                else:
                                    st.session_state[f"confirm_delete_unit_{unit['id']}"] = True
                                    st.warning("Haz clic de nuevo para confirmar")
                        st.divider()
                else:
                    st.info("No hay unidades para este filtro")
            else:
                st.warning("Primero debes crear cursos")
        except Exception as e:
            st.error(f"Error al cargar unidades: {str(e)}")
    
    with tab2:
        st.markdown("### Crear o editar unidad")
        
        try:
            courses = db_utils.get_courses()
            if courses:
                edit_unit = st.session_state.get('edit_unit', None)
                
                with st.form("unit_form"):
                    course_options = {c['id']: c['title'] for c in courses}
                    course_id = st.selectbox(
                        "Curso",
                        options=list(course_options.keys()),
                        format_func=lambda x: course_options[x],
                        index=list(course_options.keys()).index(edit_unit['course_id']) if edit_unit else 0
                    )
                    
                    title = st.text_input("Título de la unidad", value=edit_unit['title'] if edit_unit else "")
                    description = st.text_area("Descripción", value=edit_unit['description'] if edit_unit else "")
                    order = st.number_input("Orden", min_value=1, value=edit_unit['order'] if edit_unit else 1)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        submit = st.form_submit_button("💾 Guardar")
                    with col2:
                        cancel = st.form_submit_button("❌ Cancelar")
                    
                    if submit and title and description:
                        try:
                            if edit_unit:
                                db_utils.update_unit(edit_unit['id'], title, description, course_id, order)
                                st.success(f"Unidad '{title}' actualizada correctamente")
                                st.session_state.pop('edit_unit', None)
                            else:
                                unit_id = db_utils.create_unit(title, description, course_id, order)
                                st.success(f"Unidad '{title}' creada con ID: {unit_id}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error al guardar unidad: {str(e)}")
                    elif submit:
                        st.error("Por favor completa todos los campos")
                    
                    if cancel:
                        st.session_state.pop('edit_unit', None)
                        st.rerun()
            else:
                st.warning("Primero debes crear cursos")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# ==================== LESSONS PAGE ====================
elif page == "📝 Lecciones":
    st.markdown("## Gestión de Lecciones")
    
    tab1, tab2 = st.tabs(["📋 Ver Lecciones", "➕ Crear/Editar Lección"])
    
    with tab1:
        st.markdown("### Lecciones existentes")
        
        try:
            courses = db_utils.get_courses()
            if courses:
                course_options = {c['id']: c['title'] for c in courses}
                selected_course = st.selectbox(
                    "Filtrar por curso:",
                    options=[None] + list(course_options.keys()),
                    format_func=lambda x: "Todos los cursos" if x is None else course_options[x],
                    key="lesson_filter_course"
                )
                
                units = db_utils.get_units(selected_course)
                if units:
                    unit_options = {u['id']: u['title'] for u in units}
                    selected_unit = st.selectbox(
                        "Filtrar por unidad:",
                        options=[None] + list(unit_options.keys()),
                        format_func=lambda x: "Todas las unidades" if x is None else unit_options[x],
                        key="lesson_filter_unit"
                    )
                    
                    lessons = db_utils.get_lessons(selected_unit)
                    if lessons:
                        for lesson in lessons:
                            col1, col2, col3 = st.columns([3, 1, 1])
                            with col1:
                                st.write(f"**{lesson['title']}** (ID: {lesson['id']}, Orden: {lesson['order']})")
                                st.caption(f"Unidad ID: {lesson['unit_id']}")
                            with col2:
                                if st.button("✏️ Editar", key=f"edit_lesson_{lesson['id']}"):
                                    st.session_state['edit_lesson'] = lesson
                                    st.rerun()
                            with col3:
                                if st.button("🗑️ Eliminar", key=f"delete_lesson_{lesson['id']}"):
                                    if st.session_state.get(f"confirm_delete_lesson_{lesson['id']}", False):
                                        db_utils.delete_lesson(lesson['id'])
                                        st.success(f"Lección '{lesson['title']}' eliminada")
                                        st.rerun()
                                    else:
                                        st.session_state[f"confirm_delete_lesson_{lesson['id']}"] = True
                                        st.warning("Haz clic de nuevo para confirmar")
                            st.divider()
                    else:
                        st.info("No hay lecciones para este filtro")
                else:
                    st.info("No hay unidades para este curso")
            else:
                st.warning("Primero debes crear cursos")
        except Exception as e:
            st.error(f"Error al cargar lecciones: {str(e)}")
    
    with tab2:
        st.markdown("### Crear o editar lección")
        
        try:
            courses = db_utils.get_courses()
            if courses:
                edit_lesson = st.session_state.get('edit_lesson', None)
                
                with st.form("lesson_form"):
                    course_options = {c['id']: c['title'] for c in courses}
                    course_id = st.selectbox(
                        "Curso",
                        options=list(course_options.keys()),
                        format_func=lambda x: course_options[x],
                        key="lesson_form_course"
                    )
                    
                    units = db_utils.get_units(course_id)
                    if units:
                        unit_options = {u['id']: u['title'] for u in units}
                        unit_id = st.selectbox(
                            "Unidad",
                            options=list(unit_options.keys()),
                            format_func=lambda x: unit_options[x],
                            index=list(unit_options.keys()).index(edit_lesson['unit_id']) if edit_lesson and edit_lesson['unit_id'] in unit_options else 0
                        )
                        
                        title = st.text_input("Título de la lección", value=edit_lesson['title'] if edit_lesson else "")
                        order = st.number_input("Orden", min_value=1, value=edit_lesson['order'] if edit_lesson else 1)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            submit = st.form_submit_button("💾 Guardar")
                        with col2:
                            cancel = st.form_submit_button("❌ Cancelar")
                        
                        if submit and title:
                            try:
                                if edit_lesson:
                                    db_utils.update_lesson(edit_lesson['id'], title, unit_id, order)
                                    st.success(f"Lección '{title}' actualizada correctamente")
                                    st.session_state.pop('edit_lesson', None)
                                else:
                                    lesson_id = db_utils.create_lesson(title, unit_id, order)
                                    st.success(f"Lección '{title}' creada con ID: {lesson_id}")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error al guardar lección: {str(e)}")
                        elif submit:
                            st.error("Por favor completa todos los campos")
                        
                        if cancel:
                            st.session_state.pop('edit_lesson', None)
                            st.rerun()
                    else:
                        st.warning("No hay unidades en este curso. Crea una unidad primero.")
            else:
                st.warning("Primero debes crear cursos")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# ==================== CHALLENGES PAGE ====================
elif page == "🎯 Desafíos":
    st.markdown("## Gestión de Desafíos")
    
    tab1, tab2, tab3 = st.tabs(["📋 Ver Desafíos", "➕ Crear/Editar Desafío", "🎲 Opciones de Respuesta"])
    
    with tab1:
        st.markdown("### Desafíos existentes")
        
        try:
            courses = db_utils.get_courses()
            if courses:
                course_options = {c['id']: c['title'] for c in courses}
                selected_course = st.selectbox(
                    "Filtrar por curso:",
                    options=[None] + list(course_options.keys()),
                    format_func=lambda x: "Todos los cursos" if x is None else course_options[x],
                    key="challenge_filter_course"
                )
                
                units = db_utils.get_units(selected_course)
                if units:
                    unit_options = {u['id']: u['title'] for u in units}
                    selected_unit = st.selectbox(
                        "Filtrar por unidad:",
                        options=[None] + list(unit_options.keys()),
                        format_func=lambda x: "Todas las unidades" if x is None else unit_options[x],
                        key="challenge_filter_unit"
                    )
                    
                    lessons = db_utils.get_lessons(selected_unit)
                    if lessons:
                        lesson_options = {l['id']: l['title'] for l in lessons}
                        selected_lesson = st.selectbox(
                            "Filtrar por lección:",
                            options=[None] + list(lesson_options.keys()),
                            format_func=lambda x: "Todas las lecciones" if x is None else lesson_options[x],
                            key="challenge_filter_lesson"
                        )
                        
                        challenges = db_utils.get_challenges(selected_lesson)
                        if challenges:
                            for challenge in challenges:
                                with st.expander(f"**{challenge['question']}** (ID: {challenge['id']})"):
                                    st.write(f"**Tipo:** {challenge['type']}")
                                    st.write(f"**Orden:** {challenge['order']}")
                                    st.write(f"**Lección ID:** {challenge['lesson_id']}")
                                    if challenge['audio_src']:
                                        st.write(f"**Audio:** {challenge['audio_src']}")
                                    
                                    # Show options
                                    options = db_utils.get_challenge_options(challenge['id'])
                                    if options:
                                        st.markdown("**Opciones de respuesta:**")
                                        for opt in options:
                                            correct_icon = "✅" if opt['correct'] else "❌"
                                            st.write(f"{correct_icon} {opt['text']}")
                                    
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        if st.button("✏️ Editar", key=f"edit_challenge_{challenge['id']}"):
                                            st.session_state['edit_challenge'] = challenge
                                            st.rerun()
                                    with col2:
                                        if st.button("🗑️ Eliminar", key=f"delete_challenge_{challenge['id']}"):
                                            if st.session_state.get(f"confirm_delete_challenge_{challenge['id']}", False):
                                                db_utils.delete_challenge(challenge['id'])
                                                st.success(f"Desafío eliminado")
                                                st.rerun()
                                            else:
                                                st.session_state[f"confirm_delete_challenge_{challenge['id']}"] = True
                                                st.warning("Haz clic de nuevo para confirmar")
                        else:
                            st.info("No hay desafíos para este filtro")
                    else:
                        st.info("No hay lecciones para esta unidad")
                else:
                    st.info("No hay unidades para este curso")
            else:
                st.warning("Primero debes crear cursos")
        except Exception as e:
            st.error(f"Error al cargar desafíos: {str(e)}")
    
    with tab2:
        st.markdown("### Crear o editar desafío")
        
        try:
            courses = db_utils.get_courses()
            if courses:
                edit_challenge = st.session_state.get('edit_challenge', None)
                
                with st.form("challenge_form"):
                    course_options = {c['id']: c['title'] for c in courses}
                    course_id = st.selectbox(
                        "Curso",
                        options=list(course_options.keys()),
                        format_func=lambda x: course_options[x],
                        key="challenge_form_course"
                    )
                    
                    units = db_utils.get_units(course_id)
                    if units:
                        unit_options = {u['id']: u['title'] for u in units}
                        unit_id = st.selectbox(
                            "Unidad",
                            options=list(unit_options.keys()),
                            format_func=lambda x: unit_options[x],
                            key="challenge_form_unit"
                        )
                        
                        lessons = db_utils.get_lessons(unit_id)
                        if lessons:
                            lesson_options = {l['id']: l['title'] for l in lessons}
                            lesson_id = st.selectbox(
                                "Lección",
                                options=list(lesson_options.keys()),
                                format_func=lambda x: lesson_options[x],
                                index=list(lesson_options.keys()).index(edit_challenge['lesson_id']) if edit_challenge and edit_challenge['lesson_id'] in lesson_options else 0
                            )
                            
                            challenge_type = st.selectbox(
                                "Tipo de desafío",
                                options=["SELECT", "ASSIST", "LISTEN"],
                                index=["SELECT", "ASSIST", "LISTEN"].index(edit_challenge['type']) if edit_challenge else 0
                            )
                            
                            question = st.text_area("Pregunta", value=edit_challenge['question'] if edit_challenge else "")
                            order = st.number_input("Orden", min_value=1, value=edit_challenge['order'] if edit_challenge else 1)
                            audio_src = st.text_input("URL del audio (opcional)", value=edit_challenge.get('audio_src', '') if edit_challenge else "")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                submit = st.form_submit_button("💾 Guardar")
                            with col2:
                                cancel = st.form_submit_button("❌ Cancelar")
                            
                            if submit and question:
                                try:
                                    audio_value = audio_src if audio_src else None
                                    if edit_challenge:
                                        db_utils.update_challenge(edit_challenge['id'], lesson_id, challenge_type, question, order, audio_value)
                                        st.success(f"Desafío actualizado correctamente")
                                        st.session_state.pop('edit_challenge', None)
                                    else:
                                        challenge_id = db_utils.create_challenge(lesson_id, challenge_type, question, order, audio_value)
                                        st.success(f"Desafío creado con ID: {challenge_id}")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error al guardar desafío: {str(e)}")
                            elif submit:
                                st.error("Por favor completa todos los campos obligatorios")
                            
                            if cancel:
                                st.session_state.pop('edit_challenge', None)
                                st.rerun()
                        else:
                            st.warning("No hay lecciones en esta unidad")
                    else:
                        st.warning("No hay unidades en este curso")
            else:
                st.warning("Primero debes crear cursos")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    with tab3:
        st.markdown("### Gestionar opciones de respuesta")
        
        try:
            challenges = db_utils.get_challenges()
            if challenges:
                challenge_options_dict = {c['id']: f"{c['question'][:50]}... (ID: {c['id']})" for c in challenges}
                selected_challenge = st.selectbox(
                    "Selecciona un desafío:",
                    options=list(challenge_options_dict.keys()),
                    format_func=lambda x: challenge_options_dict[x]
                )
                
                st.markdown("#### Opciones existentes")
                options = db_utils.get_challenge_options(selected_challenge)
                if options:
                    for opt in options:
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            correct_icon = "✅" if opt['correct'] else "❌"
                            st.write(f"{correct_icon} **{opt['text']}** (ID: {opt['id']})")
                            if opt['image_src']:
                                st.caption(f"Imagen: {opt['image_src']}")
                            if opt['audio_src']:
                                st.caption(f"Audio: {opt['audio_src']}")
                        with col2:
                            if st.button("🗑️", key=f"delete_option_{opt['id']}"):
                                db_utils.delete_challenge_option(opt['id'])
                                st.success("Opción eliminada")
                                st.rerun()
                        st.divider()
                else:
                    st.info("No hay opciones para este desafío")
                
                st.markdown("#### Agregar nueva opción")
                with st.form("option_form"):
                    text = st.text_input("Texto de la opción")
                    correct = st.checkbox("¿Es la respuesta correcta?")
                    image_src = st.text_input("URL de imagen (opcional)")
                    audio_src = st.text_input("URL de audio (opcional)")
                    
                    if st.form_submit_button("➕ Agregar opción"):
                        if text:
                            try:
                                img_value = image_src if image_src else None
                                aud_value = audio_src if audio_src else None
                                option_id = db_utils.create_challenge_option(selected_challenge, text, correct, img_value, aud_value)
                                st.success(f"Opción creada con ID: {option_id}")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error al crear opción: {str(e)}")
                        else:
                            st.error("El texto de la opción es obligatorio")
            else:
                st.warning("Primero debes crear desafíos")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# ==================== EXAMS PAGE ====================
elif page == "📋 Exámenes":
    st.markdown("## Gestión de Exámenes")
    
    tab1, tab2, tab3 = st.tabs(["📋 Ver Exámenes", "➕ Crear/Editar Examen", "📝 Asignar Lecciones"])
    
    with tab1:
        st.markdown("### Exámenes existentes")
        
        try:
            courses = db_utils.get_courses()
            if courses:
                course_options = {c['id']: c['title'] for c in courses}
                selected_course = st.selectbox(
                    "Filtrar por curso:",
                    options=[None] + list(course_options.keys()),
                    format_func=lambda x: "Todos los cursos" if x is None else course_options[x],
                    key="exam_filter_course"
                )
                
                exams = db_utils.get_exams(selected_course)
                if exams:
                    for exam in exams:
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            st.write(f"**{exam['title']}** (ID: {exam['id']}, Orden: {exam['order']})")
                            st.caption(f"Descripción: {exam['description']}")
                            st.caption(f"Curso ID: {exam['course_id']}")
                            
                            # Show assigned lessons
                            exam_lessons = db_utils.get_exam_lessons(exam['id'])
                            if exam_lessons:
                                st.caption(f"📝 {len(exam_lessons)} lecciones asignadas")
                        with col2:
                            if st.button("✏️ Editar", key=f"edit_exam_{exam['id']}"):
                                st.session_state['edit_exam'] = exam
                                st.rerun()
                        with col3:
                            if st.button("🗑️ Eliminar", key=f"delete_exam_{exam['id']}"):
                                if st.session_state.get(f"confirm_delete_exam_{exam['id']}", False):
                                    db_utils.delete_exam(exam['id'])
                                    st.success(f"Examen '{exam['title']}' eliminado")
                                    st.rerun()
                                else:
                                    st.session_state[f"confirm_delete_exam_{exam['id']}"] = True
                                    st.warning("Haz clic de nuevo para confirmar")
                        st.divider()
                else:
                    st.info("No hay exámenes para este filtro")
            else:
                st.warning("Primero debes crear cursos")
        except Exception as e:
            st.error(f"Error al cargar exámenes: {str(e)}")
    
    with tab2:
        st.markdown("### Crear o editar examen")
        
        try:
            courses = db_utils.get_courses()
            if courses:
                edit_exam = st.session_state.get('edit_exam', None)
                
                with st.form("exam_form"):
                    course_options = {c['id']: c['title'] for c in courses}
                    course_id = st.selectbox(
                        "Curso",
                        options=list(course_options.keys()),
                        format_func=lambda x: course_options[x],
                        index=list(course_options.keys()).index(edit_exam['course_id']) if edit_exam else 0
                    )
                    
                    title = st.text_input("Título del examen", value=edit_exam['title'] if edit_exam else "")
                    description = st.text_area("Descripción", value=edit_exam['description'] if edit_exam else "")
                    order = st.number_input("Orden", min_value=1, value=edit_exam['order'] if edit_exam else 1)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        submit = st.form_submit_button("💾 Guardar")
                    with col2:
                        cancel = st.form_submit_button("❌ Cancelar")
                    
                    if submit and title and description:
                        try:
                            if edit_exam:
                                db_utils.update_exam(edit_exam['id'], title, description, course_id, order)
                                st.success(f"Examen '{title}' actualizado correctamente")
                                st.session_state.pop('edit_exam', None)
                            else:
                                exam_id = db_utils.create_exam(title, description, course_id, order)
                                st.success(f"Examen '{title}' creado con ID: {exam_id}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error al guardar examen: {str(e)}")
                    elif submit:
                        st.error("Por favor completa todos los campos")
                    
                    if cancel:
                        st.session_state.pop('edit_exam', None)
                        st.rerun()
            else:
                st.warning("Primero debes crear cursos")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    with tab3:
        st.markdown("### Asignar lecciones a exámenes")
        
        try:
            exams = db_utils.get_exams()
            if exams:
                exam_options = {e['id']: f"{e['title']} (ID: {e['id']})" for e in exams}
                selected_exam = st.selectbox(
                    "Selecciona un examen:",
                    options=list(exam_options.keys()),
                    format_func=lambda x: exam_options[x]
                )
                
                st.markdown("#### Lecciones asignadas")
                exam_lessons = db_utils.get_exam_lessons(selected_exam)
                if exam_lessons:
                    for el in exam_lessons:
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.write(f"**{el['lesson_title']}** (Lección ID: {el['lesson_id']}, Orden: {el['order']})")
                        with col2:
                            if st.button("🗑️", key=f"remove_lesson_{el['id']}"):
                                db_utils.remove_lesson_from_exam(el['id'])
                                st.success("Lección removida del examen")
                                st.rerun()
                        st.divider()
                else:
                    st.info("No hay lecciones asignadas a este examen")
                
                st.markdown("#### Agregar lección")
                
                # Get exam's course to filter lessons
                exam_data = next((e for e in exams if e['id'] == selected_exam), None)
                if exam_data:
                    lessons = db_utils.get_lessons()
                    # Filter lessons by the exam's course
                    units = db_utils.get_units(exam_data['course_id'])
                    unit_ids = [u['id'] for u in units]
                    available_lessons = [l for l in lessons if l['unit_id'] in unit_ids]
                    
                    if available_lessons:
                        with st.form("add_lesson_form"):
                            lesson_options = {l['id']: f"{l['title']} (ID: {l['id']})" for l in available_lessons}
                            lesson_id = st.selectbox(
                                "Selecciona una lección:",
                                options=list(lesson_options.keys()),
                                format_func=lambda x: lesson_options[x]
                            )
                            order = st.number_input("Orden en el examen", min_value=1, value=len(exam_lessons) + 1)
                            
                            if st.form_submit_button("➕ Agregar lección"):
                                try:
                                    db_utils.add_lesson_to_exam(selected_exam, lesson_id, order)
                                    st.success("Lección agregada al examen")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error al agregar lección: {str(e)}")
                    else:
                        st.warning("No hay lecciones disponibles en el curso de este examen")
            else:
                st.warning("Primero debes crear exámenes")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# ==================== BULK UPLOAD PAGE ====================
elif page == "📤 Carga Masiva":
    st.markdown("## Carga Masiva de Contenido")
    
    st.info("""
    Esta sección te permite cargar contenido en lote desde archivos CSV.
    Descarga las plantillas, llénalas con tus datos y súbelas aquí.
    """)
    
    st.markdown("### 📥 Descargar Plantillas CSV")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Plantilla de Cursos**")
        st.code("id,title,image_src\n1,Español,/es.svg", language="csv")
        
        st.markdown("**Plantilla de Unidades**")
        st.code("id,title,description,course_id,order\n1,Unidad 1,Aprende lo básico,1,1", language="csv")
    
    with col2:
        st.markdown("**Plantilla de Lecciones**")
        st.code("id,title,unit_id,order\n1,Lección 1,1,1", language="csv")
        
        st.markdown("**Plantilla de Desafíos**")
        st.code("id,lesson_id,type,question,order,audio_src\n1,1,SELECT,¿Qué es esto?,1,", language="csv")
    
    st.markdown("### 📤 Subir archivo CSV")
    
    upload_type = st.selectbox(
        "Tipo de contenido:",
        ["Cursos", "Unidades", "Lecciones", "Desafíos", "Opciones de Respuesta"]
    )
    
    uploaded_file = st.file_uploader("Selecciona un archivo CSV", type=['csv'])
    
    if uploaded_file is not None:
        try:
            import pandas as pd
            df = pd.read_csv(uploaded_file)
            
            st.markdown("### Vista previa de los datos")
            st.dataframe(df)
            
            if st.button("✅ Confirmar y cargar datos"):
                success_count = 0
                error_count = 0
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for idx, row in df.iterrows():
                    try:
                        if upload_type == "Cursos":
                            db_utils.create_course(row['title'], row['image_src'])
                        elif upload_type == "Unidades":
                            db_utils.create_unit(row['title'], row['description'], int(row['course_id']), int(row['order']))
                        elif upload_type == "Lecciones":
                            db_utils.create_lesson(row['title'], int(row['unit_id']), int(row['order']))
                        elif upload_type == "Desafíos":
                            audio = row['audio_src'] if pd.notna(row['audio_src']) else None
                            db_utils.create_challenge(int(row['lesson_id']), row['type'], row['question'], int(row['order']), audio)
                        elif upload_type == "Opciones de Respuesta":
                            img = row['image_src'] if pd.notna(row['image_src']) else None
                            audio = row['audio_src'] if pd.notna(row['audio_src']) else None
                            db_utils.create_challenge_option(int(row['challenge_id']), row['text'], bool(row['correct']), img, audio)
                        
                        success_count += 1
                    except Exception as e:
                        error_count += 1
                        st.warning(f"Error en fila {idx + 1}: {str(e)}")
                    
                    progress_bar.progress((idx + 1) / len(df))
                    status_text.text(f"Procesando: {idx + 1}/{len(df)}")
                
                st.success(f"✅ Carga completada: {success_count} exitosos, {error_count} errores")
                
        except Exception as e:
            st.error(f"Error al procesar el archivo: {str(e)}")

# Footer
st.markdown("---")
st.markdown("**FIBRA CMS** - Sistema de Gestión de Contenido Educativo")
