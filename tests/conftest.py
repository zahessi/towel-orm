import psycopg2.extras
import pytest

from towel import *

CONFIG = {"database": "zahessi",
          "host": "localhost",
          "user": "zahessi",
          "password": ""}


@pytest.fixture()
def cursor(postgresql):
    with postgresql.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as c:
        yield c


@pytest.fixture()
def base(postgresql):
    data = Database(postgresql)

    class Base(AbstractBaseModel):
        db = data

    yield Base
    data.kill()


@pytest.fixture(scope="function")
def fish_fixtures(base):
    class Fish(base):
        name = Column(VarChar, length=50)
        age = Column(Integer)

    Fish.objects().create_table()
    obj = Fish(name="lily", age=2)
    obj2 = Fish(name="sam", age=3)
    obj3 = Fish(name="dody clark", age=432)
    obj4 = Fish(name="alexdwop", age=123)

    obj.objects().save()
    obj2.objects().save()
    obj3.objects().save()
    obj4.objects().save()
    return Fish, [obj, obj2, obj3, obj4]


@pytest.fixture
def fish_and_aquarium(base):
    class Aquarium(base):
        color = Column(VarChar, length=50)
        price = Column(Integer)

    class Fish(base):
        name = Column(VarChar, length=50)
        age = Column(Integer)
        aquarium_id = Column(ForeignKey, table=Aquarium, entity_name="aquarium")

    return Fish, Aquarium
