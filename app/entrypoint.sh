#!/bin/sh
set -e

echo "⏳ Esperando a que la base de datos esté lista..."

until pg_isready -h db -p 5432 -U postgres > /dev/null 2>&1; do
  echo "⏱️  Esperando..."
  sleep 1
done

echo "🚀 Base de datos disponible. Aplicando migraciones..."

alembic upgrade head

echo "✅ Migraciones aplicadas. Iniciando servidor..."

exec uvicorn main:app --host 0.0.0.0 --port 8000 ${DEV_MODE:+--reload}
