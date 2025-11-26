# FIBRA Content Management System

Sistema de gestión de contenido educativo para FIBRA, construido con Streamlit y PostgreSQL.

## 🚀 Características

- **Gestión de Cursos**: Crear, editar y eliminar cursos
- **Gestión de Unidades**: Administrar unidades dentro de cada curso
- **Gestión de Lecciones**: Crear y organizar lecciones por unidad
- **Gestión de Desafíos**: Crear desafíos con diferentes tipos (SELECT, ASSIST, LISTEN)
- **Opciones de Respuesta**: Administrar opciones correctas e incorrectas para cada desafío
- **Carga Masiva**: Importar contenido desde archivos CSV
- **Interfaz Intuitiva**: UI moderna y fácil de usar

## 📋 Requisitos

- Python 3.8 o superior
- PostgreSQL (Neon u otro proveedor)
- Credenciales de acceso a la base de datos

## 🔧 Instalación

1. **Navega al directorio de Streamlit:**
   ```bash
   cd streamlit
   ```

2. **Crea un entorno virtual (recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/Mac
   # o
   venv\Scripts\activate  # En Windows
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura las variables de entorno:**
   ```bash
   cp .env.example .env
   ```
   
   Edita el archivo `.env` y agrega tu cadena de conexión a la base de datos:
   ```
   DATABASE_URL=postgresql://user:password@host:port/database?sslmode=require
   ```

## ▶️ Ejecución

Para iniciar la aplicación:

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📖 Uso

### Gestión Individual

1. **Cursos**: 
   - Ve a la sección "📖 Cursos"
   - Crea un nuevo curso con título e imagen
   - Edita o elimina cursos existentes

2. **Unidades**:
   - Ve a "📑 Unidades"
   - Selecciona un curso
   - Crea unidades con título, descripción y orden

3. **Lecciones**:
   - Ve a "📝 Lecciones"
   - Selecciona curso y unidad
   - Crea lecciones con título y orden

4. **Desafíos**:
   - Ve a "🎯 Desafíos"
   - Selecciona curso, unidad y lección
   - Crea desafíos con tipo, pregunta y audio (opcional)
   - Agrega opciones de respuesta en la pestaña correspondiente

### Carga Masiva

1. Ve a "📤 Carga Masiva"
2. Descarga la plantilla CSV correspondiente
3. Llena la plantilla con tus datos
4. Sube el archivo CSV
5. Revisa la vista previa
6. Confirma la carga

## 📊 Estructura de la Base de Datos

```
courses
├── id (serial)
├── title (text)
└── image_src (text)

units
├── id (serial)
├── title (text)
├── description (text)
├── course_id (integer) → courses.id
└── order (integer)

lessons
├── id (serial)
├── title (text)
├── unit_id (integer) → units.id
└── order (integer)

challenges
├── id (serial)
├── lesson_id (integer) → lessons.id
├── type (enum: SELECT, ASSIST, LISTEN)
├── question (text)
├── order (integer)
└── audio_src (text, optional)

challenge_options
├── id (serial)
├── challenge_id (integer) → challenges.id
├── text (text)
├── correct (boolean)
├── image_src (text, optional)
└── audio_src (text, optional)
```

## 🔒 Seguridad

- **Backup**: Siempre haz un backup de tu base de datos antes de usar la carga masiva
- **Credenciales**: No compartas tu archivo `.env` con credenciales
- **Producción**: Usa credenciales con permisos limitados si es posible

## 🐛 Solución de Problemas

### Error de conexión a la base de datos
- Verifica que `DATABASE_URL` en `.env` sea correcta
- Asegúrate de que la base de datos esté accesible
- Verifica que el formato incluya `?sslmode=require` para Neon

### Error al cargar CSV
- Verifica que el formato del CSV coincida con las plantillas
- Asegúrate de que los IDs de referencia existan (ej: course_id debe existir en courses)
- Revisa que los tipos de datos sean correctos

### Columna audio_src no existe
- Ejecuta la migración SQL para agregar la columna:
  ```sql
  ALTER TABLE challenges ADD COLUMN IF NOT EXISTS audio_src TEXT;
  ```

## 📝 Formato de Plantillas CSV

### Cursos
```csv
id,title,image_src
1,Español,/es.svg
2,Francés,/fr.svg
```

### Unidades
```csv
id,title,description,course_id,order
1,Unidad 1,Aprende lo básico del español,1,1
2,Unidad 2,Conversaciones cotidianas,1,2
```

### Lecciones
```csv
id,title,unit_id,order
1,Saludos,1,1
2,Presentaciones,1,2
```

### Desafíos
```csv
id,lesson_id,type,question,order,audio_src
1,1,SELECT,¿Qué significa "Hola"?,1,
2,1,LISTEN,Escucha y selecciona,2,/audio/hello.mp3
```

### Opciones de Respuesta
```csv
id,challenge_id,text,correct,image_src,audio_src
1,1,Hello,true,,
2,1,Goodbye,false,,
3,1,Thank you,false,,
```

## 🤝 Contribuciones

Si encuentras algún error o tienes sugerencias de mejora, por favor crea un issue o pull request.

## 📄 Licencia

Este proyecto es parte de FIBRA y sigue la misma licencia del proyecto principal.
