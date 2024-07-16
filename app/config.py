import os

DATABASE = {
    'name': os.getenv('DB_NAME'),
    'engine': 'peewee.PostgresqlDatabase',
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 5432)),
}