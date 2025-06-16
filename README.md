# Payments API Paypohne

💳 Microservicio de Pagos - Payphone
Este microservicio permite gestionar pagos utilizando la plataforma Payphone. Está desarrollado en Python y expone una API documentada con Swagger para facilitar su integración.

🚀 Primeros Pasos

1. Variables de entorno
Debes definir las siguientes variables en un archivo .env en la raíz del proyecto:

PAYPHONE_TOKEN: Token de autenticación Payphone.
PAYPHONE_STORE_ID: ID de la tienda Payphone.
PAYPHONE_RESPONSE_URL: URL de respuesta tras el pago.
CURRENCY: Moneda (ejemplo: USD).
TAX_AMOUNT: Monto de impuesto en centavos (ejemplo: 15).
DATABASE_URL: URL de conexión a la base de datos PostgreSQL.

🛠️ Tecnologías Utilizadas
Python 3.x
FastAPI
SQLAlchemy
Alembic
PostgreSQL
httpx
Swagger UI
Payphone SDK / API


📦 Estructura del Proyecto
main.py: Punto de entrada de la aplicación.
routers: Definición de rutas de la API.
services: Lógica de negocio y servicios externos.
models: Modelos de datos y validación.
db.py, db_models.py: Configuración y modelos de base de datos.
migrations: Migraciones de base de datos.
config.py: Configuración y carga de variables de entorno.


📝 Notas
La API permite iniciar y confirmar pagos usando el servicio de PAYPHONE.
Puedes adaptar los endpoints y la lógica según las necesidades de tu negocio.
Consulta la documentación Swagger para ejemplos de uso y pruebas.
Esto es un repositorio demo, las funciones actuales son funcionales
Se puede usar tanto local como docker
Es un proyecto independiente
