import pytest
from towel import *


class TestSQLParser:

    def test_returns_valid(self, base):
        class Fish(base):
            name = Column(VarChar, length=30)
            age = Column(Integer)

        sql = SQL.create_table(Fish).as_string(base.db.connection)

        assert sql.lower() == 'create table "fish" (id serial primary key, age int, name varchar(30))'

    def test_returns_valid_on_empty(self, base):
        class Fish(base):
            pass

        sql = SQL.create_table(Fish).as_string(base.db.connection)

        assert sql.lower() == 'create table "fish" (id serial primary key)'


class TestColumnSQL:

    def test_integer_column(self):
        column = Column(Integer)
        column.column_name = "age"
        column.value = 123

        assert column.sql == "age int"

    def test_varchar_column(self):
        column = Column(VarChar, length=30)
        column.column_name = "name"

        assert column.sql == "name varchar({})".format(30)
