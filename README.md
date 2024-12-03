Notes App Backend
Este es el repositorio del backend de la aplicación Notes App, desarrollado con Python y FastAPI, utilizando PostgreSQL y SQLAlchemy para la gestión de la base de datos.

Tabla de Contenidos
Descripción
Características
Tecnologías Utilizadas
Instalación y Configuración
Estructura del Proyecto
Endpoints de la API
Estrategia de Bloqueo Eficiente
Pruebas
Manejo de Errores
Desafíos y Soluciones
Documentación de la API
Contribuciones
Licencia
Descripción
El backend de la Notes App provee una API RESTful para manejar la autenticación de usuarios y la gestión de notas. Implementa una estrategia de bloqueo eficiente para manejar concurrencia y asegurar la consistencia de los datos en un entorno altamente paralelizado.

Características
Autenticación Segura: Registro e inicio de sesión con protección de contraseñas y emisión de JWT.
Gestión de Notas: Endpoints para crear, leer, actualizar y eliminar notas.
Estrategia de Bloqueo: Implementación de bloqueo optimista para manejar concurrencia.
Validación de Datos: Uso de modelos Pydantic para validar y serializar datos.
Documentación Automática: Swagger UI proporcionado por FastAPI.
Pruebas Unitarias: Pruebas enfocadas en concurrencia y estrategia de bloqueo.
Tecnologías Utilizadas
Python 3.8+: Lenguaje de programación principal.
FastAPI: Framework web para construir APIs.
PostgreSQL: Base de datos relacional.
SQLAlchemy: ORM para interactuar con la base de datos.
Alembic: Herramienta para migraciones de base de datos.
JWT (PyJWT): Para autenticación basada en tokens.
bcrypt: Para hashing seguro de contraseñas.
pytest y pytest-asyncio: Para pruebas unitarias y asíncronas.
Instalación y Configuración
Requisitos Previos
Python 3.8 o superior
PostgreSQL
Virtualenv (opcional pero recomendado)
Pasos de Instalación
Clonar el Repositorio

bash
Copiar código
git clone https://github.com/tu_usuario/notes-app-backend.git
cd notes-app-backend
Crear y Activar el Entorno Virtual

bash
Copiar código
python -m venv venv

# Windows

venv\Scripts\activate

# Unix/Linux

source venv/bin/activate
Instalar Dependencias

bash
Copiar código
pip install -r requirements.txt
Configurar Variables de Entorno

Renombrar .env.example a .env y configurar las variables necesarias:

env
Copiar código
DATABASE_URL=postgresql+psycopg2://usuario:contraseña@localhost:5432/notes_app_db
SECRET_KEY=tu_clave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
Configurar la Base de Datos

Crear la base de datos y el usuario en PostgreSQL.

Aplicar migraciones:

bash
Copiar código
alembic upgrade head
Iniciar el Servidor

bash
Copiar código
uvicorn main:app --reload
La API estará disponible en http://localhost:8000.

Estructura del Proyecto
main.py: Punto de entrada de la aplicación.
app/
routers/: Enrutadores para diferentes endpoints.
models/: Definiciones de modelos SQLAlchemy.
schemas/: Modelos Pydantic para validación.
services/: Lógica de negocio y funciones auxiliares.
core/: Configuraciones y utilidades centrales.
tests/: Pruebas unitarias y de integración.
Endpoints de la API
Autenticación
POST /api/auth/register: Registra un nuevo usuario.
POST /api/auth/login: Autentica al usuario y devuelve un JWT.
Notas
GET /api/notes: Obtiene todas las notas del usuario autenticado.
POST /api/notes: Crea una nueva nota.
GET /api/notes/{id}: Obtiene una nota específica.
PUT /api/notes/{id}: Actualiza una nota existente.
DELETE /api/notes/{id}: Elimina una nota.
Estrategia de Bloqueo Eficiente
Se implementó una estrategia de bloqueo optimista utilizando una marca de tiempo updated_at en el modelo de nota.

Detalles de Implementación
Al Actualizar una Nota:
El cliente envía el updated_at actual de la nota.
El backend verifica si el updated_at coincide con el de la base de datos.
Si coincide: Procede con la actualización y actualiza updated_at.
Si no coincide: Rechaza la actualización y devuelve un error de conflicto.
Justificación
Eficiencia: Evita bloqueos pesimistas que pueden convertirse en cuellos de botella.
Escalabilidad: Adecuado para entornos con alta concurrencia.
Consistencia: Asegura que no se sobrescriban cambios sin notificar al usuario.
Pruebas
Se utilizaron pytest y pytest-asyncio para escribir pruebas unitarias y asíncronas, enfocándose en:

Autenticación: Registro e inicio de sesión.
Gestión de Notas: Creación, actualización y eliminación.
Concurrencia: Simulación de actualizaciones concurrentes para probar la estrategia de bloqueo.
Ejecutar Pruebas
bash
Copiar código
pytest
Manejo de Errores
Excepciones Personalizadas: Para errores específicos como autenticación fallida o conflictos de actualización.
Manejadores de Excepciones: Para devolver códigos de estado HTTP y mensajes significativos.
Validación: Uso de Pydantic para validar entradas y proporcionar retroalimentación clara.
Desafíos y Soluciones
Concurrencia y Consistencia de Datos
Desafío: Evitar condiciones de carrera al actualizar notas desde múltiples instancias.

Solución: Implementar bloqueo optimista con verificación de updated_at para asegurar que las actualizaciones sean atómicas y consistentes.

Operaciones Asíncronas con la Base de Datos
Desafío: Manejar operaciones de base de datos de manera asíncrona.

Solución: Utilizar AsyncSession de SQLAlchemy y asyncpg como controlador de PostgreSQL compatible con asincronía.

Documentación de la API
FastAPI proporciona documentación automática disponible en:

Swagger UI: http://localhost:8000/docs
Redoc: http://localhost:8000/redo
