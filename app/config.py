import os

DATABASE = {
    'name': 'mydatabase',
    'engine': 'peewee.PostgresqlDatabase',
    'user': os.getenv('POSTGRES_USER', 'username'),
    'password': os.getenv('POSTGRES_PASSWORD', 'password'),
    'host': os.getenv('POSTGRES_HOST', 'db'),
    'port': int(os.getenv('POSTGRES_PORT', 5432)),
}