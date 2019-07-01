import pytest
from towel import *


class TestModelTest:

    def test_table_resets(self, base):
        name = "new"

        class Fish(base):
            __tablename__ = name

        f = Fish()
        assert f.__tablename__ == name

    def test_table_default_name(self, base):
        class Fish(base):
            pass

        f = Fish()
        assert f.__tablename__ == Fish.__name__.lower()

    def test_creates_columns(self, base):
        class Fish(base):
            name = Column(VarChar, length=50)

        name = "name"
        f = Fish(name=name)
        assert f.name.value == name

    def test_validates_on_int_happy(self, base):
        class Fish(base):
            age = Column(Integer)

        age = 31
        f = Fish(age=age)
        assert f.age.value == age

    def test_validates_on_int(self, base):
        class Fish(base):
            age = Column(Integer)

        age = "fjsk"

        with pytest.raises(TowelValueError):
            Fish(age=age)

    def test_validates_on_float_happy(self, base):
        class Fish(base):
            weight = Column(Real)

        weight = 31.3
        f = Fish(weight=weight)
        assert f.weight.value == weight

    def test_validates_on_int(self, base):
        class Fish(base):
            age = Column(Real)

        age = "fjsk"

        with pytest.raises(TowelValueError):
            Fish(age=age)
