# Racionador de Comidas - Proyecto Modular

## Descripción general

Este proyecto permite calcular las cantidades ajustadas de ingredientes para preparar recetas para una cantidad variable de personas, considerando pérdidas en los insumos y precios por ración. Además, integra un generador de recetas asistido por IA (DeepSeek API) para crear nuevas recetas que se pueden guardar automáticamente en la base de datos.

---

## Estructura del proyecto

- `HTML/`: Contiene la estructura de la interfaz web (index.html).
- `CSS/`: Estilos con Bootstrap.
- `JS/`: Scripts para la interactividad del frontend.
- `db/`: Scripts SQL para la base de datos y consultas.
- `py/`: Código Python para lógica de negocio, cálculos, conexión a la base de datos y API.

---

## Flujo de trabajo

1. El usuario selecciona una receta y la cantidad de personas.
2. El frontend envía la solicitud al backend para calcular las cantidades ajustadas y precios.
3. El backend consulta la base de datos, realiza los cálculos y devuelve los resultados.
4. El usuario puede usar el generador de recetas con IA para crear nuevas recetas.
5. La receta generada puede ser guardada en la base de datos para uso futuro.

---

## Requisitos para ejecutar

- Python 3.8+
- PostgreSQL instalado y configurado
- Variables de entorno configuradas:
  - `PG_DB`, `PG_USER`, `PG_PASS`, `PG_HOST`, `PG_PORT` para la base de datos
  - `DEESEEK_API_KEY` para la API de DeepSeek

---

## Instalación y configuración de la base de datos

1. Crear la base de datos (ejemplo):

```bash
createdb racionador
psql -d racionador -f db/schema.sql
export PG_DB=racionador
export PG_USER=postgres
export PG_PASS=mlx
export PG_HOST=localhost
export PG_PORT=5432
pip install flask psycopg2-binary requests numpy
cd py
export FLASK_APP=app.py
flask run
