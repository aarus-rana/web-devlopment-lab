import sqlalchemy
from db import metadata

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("username", sqlalchemy.String, unique=True, index=True, nullable=False),
    sqlalchemy.Column("password", sqlalchemy.String, nullable=False),
)
