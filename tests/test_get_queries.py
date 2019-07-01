from towel import *


class TestCreateTable:

    def test_queries(self, base, cursor):
        class Fish(base):
            name = Column(VarChar, length=50)
            age = Column(Integer)

        Fish.objects().create_table()
        obj = Fish(name="lily", age=2)
        obj2 = Fish(name="sam", age=3)

        obj.objects().save()
        obj2.objects().save()

        base.db.commit()
        result = Fish.objects().get_all()

        assert all(x in result[0] for x in (obj.id.value, obj.name.value, obj.age.value))
        assert all(x in result[1] for x in (obj2.id.value, obj2.name.value, obj2.age.value))

    def test_queries_on_empty_set(self, base, cursor):
        class Fish(base):
            name = Column(VarChar, length=50)
            age = Column(Integer)

        Fish.objects().create_table()

        result = Fish.objects().get_all()
        assert len(result) == 0

    def test_limit(self, base, cursor, fish_fixtures):
        Fish, fixes = fish_fixtures
        result = Fish.objects().get_all(limit=2)
        assert len(result) == 2
