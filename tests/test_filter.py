from towel import *
import pytest


class TestFiltered:

    def test_filters(self, base, cursor, fish_fixtures):
        fish_class, elements = fish_fixtures
        result = fish_class.objects().filter("age", "<", 10).get_all()

        assert all(x.age < 10 for x in result)

    def test_raises_on_invalid_syntax(self, base, cursor, fish_fixtures):
        fish_class, elements = fish_fixtures
        with pytest.raises(TowelAttributeError):
            fish_class.objects().filter("age", "+", 10)

    def test_raises_on_non_existing_column(self, base, cursor, fish_fixtures):
        fish_class, elements = fish_fixtures
        with pytest.raises(TowelAttributeError):
            fish_class.objects().filter("jfsdlow", "<", 10)

    def test_returns_empty_set(self, base, cursor, fish_fixtures):
        fish_class, elements = fish_fixtures
        result = fish_class.objects().filter("age", ">", 1000000000).get_all()

        assert len(result) == 0

    def test_with_mult_filters(self, base, cursor, fish_fixtures):
        fish_class, elements = fish_fixtures
        result = fish_class.objects().filter("age", "=", 3).filter("name", "=", "sam").get_all()

        assert len(result) == 1
        result = result[0]
        assert result.age == 3
        assert result.name == "sam"

    def test_filter_with_limit(self, base, cursor, fish_fixtures):
        fish_class, elements = fish_fixtures
        result = fish_class.objects().filter("age", ">", 3).get_all(limit=1)

        assert len(result) == 2
        assert result[0].age > 3
        assert result[1].age > 3
