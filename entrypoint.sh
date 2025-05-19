#!/bin/sh
echo "Aguardando o banco de dados..."

uv run flask db upgrade

exec uv run gunicorn main:app -b 0.0.0.0:5000
