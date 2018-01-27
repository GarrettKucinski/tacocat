from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
from peewee import *

db = SqliteDatabase('tacocat.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(UserMixin, BaseModel):
    email = CharField(unique=True)
    password = CharField(max_length=10)

    def get_tacos(self):
        return Taco.select().where(Taco.user == self)

    @classmethod
    def create_user(cls, email, password):
        try:
            with db.transaction():
                cls.create(email=email,
                           password=generate_password_hash(password))
        except IntegrityError:
            raise ValueError("User already exists!")


class Taco(BaseModel):
    user = ForeignKeyField(
        rel_model=User,
        related_name="tacos"
    )
    protein = CharField(default='')
    shell = CharField(default='')
    cheese = BooleanField(default=False)
    extras = TextField()


def initialize():
    db.connect()
    db.create_tables([User, Taco], safe=True)
    db.close()
