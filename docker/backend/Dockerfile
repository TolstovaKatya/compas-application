FROM python:3.10-slim

WORKDIR /app

COPY compas-server/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY compas-server/ .

RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "compas.compas.wsgi:application"]