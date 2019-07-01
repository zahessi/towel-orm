import pytest
from towel import *


class TestUpdate:

    def test_deletes(self, base, cursor, fish_fixtures):
        Fish, fishes = fish_fixtures
        fish = fishes[0]

        fish.objects().remove()

        assert not fish.as_namedtuple() in Fish.objects().get_all()

    def test_removes_multiple_without_filter(self, base, cursor, fish_fixtures):
        Fish, fix = fish_fixtures
        Fish.objects().remove()

        cursor.execute("select * from fish")

        assert len(cursor.fetchall()) == 0

    def test_updates_on_multiple_with_filter(self, base, cursor, fish_fixtures):
        Fish, fix = fish_fixtures
        Fish.objects().filter("id", "<", 10).remove()

        assert all(x.id > 10 for x in Fish.objects().get_all())
