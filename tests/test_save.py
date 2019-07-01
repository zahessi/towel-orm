from collections import namedtuple
from towel import *
from psycopg2 import sql
import pytest


class TestCreateTable:

    def test_creates_table(self, base, cursor):
        class Fish(base):
            name = Column(VarChar, length=50)
            age = Column(Integer)

        a = Fish(name="lily", age=12)
        a.objects().save()

        cursor.execute(sql.SQL("SELECT to_regclass('public.{}');").format(sql.Identifier(Fish.tablename())))
        assert cursor.fetchone()[0] == Fish.tablename()

    def test_creates_row(self, base, cursor):
        class Fish(base):
            name = Column(VarChar, length=50)
            age = Column(Integer)

        a = Fish(name="lily", age=12)
        a.objects().save()
        base.db.commit()

        cursor.execute(sql.SQL("select * from {}").format(sql.Identifier(Fish.tablename())))
        result = cursor.fetchone()
        assert all(x in result for x in (a.id.value, a.name.value, a.age.value))

    def test_returns_none_on_non_existing(self, base, cursor):
        class Fish(base):
            name = Column(VarChar, length=50)
            age = Column(Integer)

        Fish.objects().create_table()
        fish = Fish.objects().get(3422)
        assert fish is None

    def test_raises_on_duplicate_id(self, base, cursor):
        class Fish(base):
            name = Column(VarChar, length=50)
            age = Column(Integer)

        Fish.objects().create_table()
        fish = Fish(name="alex", age=22)
        fish.objects().save()

        fish2 = Fish(name="samanta", age=2, id=1)

        with pytest.raises(TowelOperationalError):
            fish2.objects().save()

    def test_saves_iterator_of_namedtuples(self, base, cursor):
        class Fish(base):
            name = Column(VarChar, length=50)
            age = Column(Integer)

        fish_nt = namedtuple("fish", ("name", "age"))

        origin = [
            fish_nt("lily", 1),
            fish_nt("clark", 2)
        ]

        Fish.objects().save_from_namedtuple(origin)

        cursor.execute(sql.SQL("select * from {}").format(sql.Identifier(Fish.tablename())))
        first, second = cursor.fetchall()

        assert first.name == "lily"
        assert first.age == 1
        assert second.name == "clark"
        assert second.age == 2

    def test_raises_on_inconsistent_type(self, base, cursor):
        class Fish(base):
            name = Column(VarChar, length=50)
            age = Column(Integer)

        fish_nt = namedtuple("fish", ("name", "age"))

        origin = [
            fish_nt("lily", 1),
            dict(name="clark", age=2)
        ]

        with pytest.raises(TowelAttributeError):
            Fish.objects().save_from_namedtuple(origin)
