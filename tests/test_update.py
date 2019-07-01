import pytest
from towel import *


class TestUpdate:

    def test_updates_on_single(self, base, cursor, fish_fixtures):
        Fish, fix = fish_fixtures
        fish = fix[0]
        fish.objects().update(name="new name")

        cursor.execute("select * from fish where id = %s", [fish.id.value])
        result = cursor.fetchone()

        assert result.name == fish.name.value

    def test_raises_on_incompatible_type(self, base, cursor, fish_fixtures):
        Fish, fix = fish_fixtures
        fish = fix[0]

        with pytest.raises(TowelValueError):
            fish.objects().update(name=123)

    def test_updates_on_multiple_without_filter(self, base, cursor, fish_fixtures):
        Fish, fix = fish_fixtures
        Fish.objects().update(name="new name")

        cursor.execute("select * from fish")

        assert all(x.name == "new name" for x in Fish.objects().get_all())

    def test_updates_on_multiple_with_filter(self, base, cursor, fish_fixtures):
        Fish, fix = fish_fixtures
        Fish.objects().filter("id", "<", 10).update(name="new name")

        cursor.execute("select * from fish")

        assert all(x.name == "new name" for x in Fish.objects().filter("id", "<", 10).get_all())

    def test_raises_on_multiple_with_filter_illegal_type(self, base, cursor, fish_fixtures):
        Fish, fix = fish_fixtures

        with pytest.raises(TowelValueError):
            Fish.objects().filter("id", "<", 10).update(name=123)

    def test_raises_on_illegal_column(self, base, cursor, fish_fixtures):
        Fish, fix = fish_fixtures

        with pytest.raises(TowelAttributeError):
            Fish.objects().update(some="new name")
