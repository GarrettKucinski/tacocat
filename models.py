from peewee import *

db = SqliteDatabase('tacocat.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    email = CharField(unique=True)
    password = CharField(max_length=10)

    @classmethod
    def create_user(cls, email, password):
        try:
            with db.transaction():
                cls.create(email=email,
                           password=generate_password_hash(password))
        except IntegrityError:
            raise ValueError("User already exists!")


class Taco(BaseModel):
    protein = CharField()
    shell = CharField()
    cheese = BooleanField()
    extras = TextField()


def initialize():
    db.connect()
    db.create_tables([User, Taco], safe=True)
    db.close()
