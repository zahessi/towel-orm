import pytest

from towel import *


class TestCreateTableWithForeignKey:

    def test_creates_and_saves(self, base, cursor, fish_and_aquarium):
        Fish, Aquarium = fish_and_aquarium

        aq = Aquarium(color="green")
        aq.objects().save()

        fish = Fish(name="lily", age=2, aquarium_id=aq.id.value)
        fish.objects().create_table()
        fish.objects().save()

        resultset = Fish.objects().get_all()[0]
        assert resultset.aquarium_id == aq.id.value

    def test_fetches(self, base, cursor, fish_and_aquarium):
        Fish, Aquarium = fish_and_aquarium

        aq = Aquarium(color="green")
        aq.objects().save()

        fish = Fish(name="lily", age=2, aquarium_id=aq.id.value)
        fish.objects().create_table()
        fish.objects().save()

        result_fish = Fish.objects().get(fish.id.value)
        assert result_fish.aquarium.id.value == aq.id.value

    def test_fetches_entity(self, base, cursor, fish_and_aquarium):
        Fish, Aquarium = fish_and_aquarium

        aq = Aquarium(color="green")
        aq.objects().save()

        fish = Fish(name="lily", age=2, aquarium_id=aq.id.value)
        fish.objects().save()

        result_fish = Fish.objects().get(fish.id.value)
        assert isinstance(result_fish.aquarium, Aquarium)

    def test_foreign_entity_exists(self, base, cursor, fish_and_aquarium):
        Fish, Aquarium = fish_and_aquarium

        assert issubclass(Fish.aquarium, Aquarium)

    def test_raises_on_invalid_foreignkey(self, base, cursor, fish_and_aquarium):
        Fish, Aquarium = fish_and_aquarium

        aq = Aquarium(color="green")
        aq.objects().save()

        with pytest.raises(TowelAttributeError):
            Fish(name="lily", age=2, aquarium_id=22222).objects().save()

    def test_filter_with_foreign(self, base, cursor, fish_and_aquarium):
        Fish, Aquarium = fish_and_aquarium

        aq = Aquarium(color="green")
        aq2 = Aquarium(color="blue")
        aq.objects().save()
        aq2.objects().save()

        fish = Fish(name="lily", age=2, aquarium_id=aq.id.value)
        fish2 = Fish(name="dodie", age=4, aquarium_id=aq.id.value)
        fish3 = Fish(name="clark", age=1, aquarium_id=aq2.id.value)
        fish.objects().save()
        fish2.objects().save()
        fish3.objects().save()

        first, second = Fish.objects().filter("aquarium_id__color", "=", "green").get_all()
        assert Aquarium.objects().get(first.aquarium_id).color.value == "green"
        assert Aquarium.objects().get(second.aquarium_id).color.value == "green"

    def test_filter_with_foreign_and_simple(self, base, cursor, fish_and_aquarium):
        Fish, Aquarium = fish_and_aquarium

        aq = Aquarium(color="green")
        aq2 = Aquarium(color="blue")
        aq.objects().save()
        aq2.objects().save()

        fish = Fish(name="lily", age=2, aquarium_id=aq.id.value)
        fish2 = Fish(name="dodie", age=4, aquarium_id=aq.id.value)
        fish3 = Fish(name="clark", age=1, aquarium_id=aq2.id.value)
        fish.objects().save()
        fish2.objects().save()
        fish3.objects().save()

        first, second = Fish.objects().filter("aquarium_id__color", "=", "green").filter("age", ">", 1).get_all()
        assert Aquarium.objects().get(first.aquarium_id).color.value == "green" and first.age > 1
        assert Aquarium.objects().get(second.aquarium_id).color.value == "green" and second.age > 1

    def test_filter_with_mult_foreign(self, base, cursor, fish_and_aquarium):
        Fish, Aquarium = fish_and_aquarium

        aq = Aquarium(color="green", price=10)
        aq2 = Aquarium(color="blue", price=12)
        aq3 = Aquarium(color="green", price=40)
        aq.objects().save()
        aq2.objects().save()
        aq3.objects().save()

        fish = Fish(name="lily", age=2, aquarium_id=aq.id.value)
        fish2 = Fish(name="dodie", age=4, aquarium_id=aq3.id.value)
        fish3 = Fish(name="clark", age=1, aquarium_id=aq2.id.value)
        fish.objects().save()
        fish2.objects().save()
        fish3.objects().save()

        first = Fish.objects().filter("aquarium_id__color", "=", "green").filter("aquarium_id__price", ">",
                                                                                 10).get_all()[0]
        received_aq = Aquarium.objects().get(first.aquarium_id)
        assert received_aq.color.value == "green" and received_aq.price.value > 10

    def test_remove_with_filter_foreign(self, base, cursor, fish_and_aquarium):
        Fish, Aquarium = fish_and_aquarium

        aq = Aquarium(color="green", price=10)
        aq2 = Aquarium(color="blue", price=12)
        aq3 = Aquarium(color="green", price=40)
        aq.objects().save()
        aq2.objects().save()
        aq3.objects().save()

        fish = Fish(name="lily", age=2, aquarium_id=aq.id.value)
        fish2 = Fish(name="dodie", age=4, aquarium_id=aq3.id.value)
        fish3 = Fish(name="clark", age=1, aquarium_id=aq2.id.value)
        fish.objects().save()
        fish2.objects().save()
        fish3.objects().save()

        Fish.objects().filter("aquarium_id__color", "=", "green").filter("aquarium_id__price", ">", 10).remove()
        new_fish = Fish.objects().get_all()
        assert len(new_fish) == 2
