from __future__ import annotations

import sys
from typing import List, Optional, Tuple, List
from functools import lru_cache


def separate_plus_minus(*args: int) -> Tuple[List[int], List[int]]:
    positive = []
    negative = []
    print(args)
    for i in args:
        if i > 0:
            positive.append(i)
            negative.append(0)
        elif i < 0:
            negative.append(abs(i))
            positive.append(0)
        elif i == 0:
            negative.append(0)
            positive.append(0)
    return negative, positive


class Ingredient:
    def __init__(self, tier):
        self.tier = tier

    @classmethod
    @lru_cache()
    def tier_0(cls):
        return Ingredient(0)

    @classmethod
    @lru_cache()
    def tier_1(cls):
        return Ingredient(1)

    @classmethod
    @lru_cache()
    def tier_2(cls):
        return Ingredient(2)

    @classmethod
    @lru_cache()
    def tier_3(cls):
        return Ingredient(3)

    @classmethod
    def from_multiple(cls, tier, amount):
        return [getattr(cls, f"tier_{tier}")() for _ in range(amount)]


class IngredientInventory:
    def __init__(self, ingredients: List[Ingredient]):
        self.ingredients = ingredients

    @classmethod
    def from_input(cls, inv_0: int, inv_1: int, inv_2: int, inv_3: int):
        ingredients = []
        for tier, amount in zip(range(4), (inv_0, inv_1, inv_2, inv_3)):
            ingredients.extend(Ingredient.from_multiple(tier, amount))

        return cls(ingredients)

    def __contains__(self, ingredients: IngredientInventory):
        copy_ingredients = self.ingredients[:]
        for i in ingredients:
            if i in copy_ingredients:
                copy_ingredients.remove(i)
            else:
                return False
        return bool(ingredients.ingredients)

    def __iter__(self):
        yield from self.ingredients

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        return str([i.tier for i in self.ingredients])


class Order(IngredientInventory):
    def __init__(self, ingredients: List[Ingredient], id: int, price: int):
        self.id = id
        self.price = price
        super().__init__(ingredients)

    @classmethod
    def from_input(cls, delta_0: int, delta_1: int, delta_2: int, delta_3: int, id: int, price: int):
        return cls(
            IngredientInventory.from_input(
                delta_0, delta_1, delta_2, delta_3
            ).ingredients,
            id,
            price
        )

    def brew(self):
        print(f"BREW {self.id}")


class Spell:
    def __init__(self, price: Optional[IngredientInventory], product: IngredientInventory, id):
        self.id = id
        self.price = price
        self.product = product

    @classmethod
    def from_input(cls, delta_0: int, delta_1: int, delta_2: int, delta_3: int, id: int):
        items = []
        for neg_pos in separate_plus_minus(delta_0, delta_1, delta_2, delta_3):
            print(neg_pos)
            items.append(IngredientInventory.from_input(*neg_pos))

        return cls(*items, id)


class OrderInventory:
    def __init__(self, recipes: List[Order]):
        self.recipes = recipes

    @classmethod
    def from_input(cls):
        actions = []
        action_count = int(input())  # the number of spells and recipes in play
        for i in range(action_count):
            action_id, action_type, \
            delta_0, delta_1, delta_2, delta_3, \
            price, tome_index, tax_count, \
            castable, repeatable = input().split()

            action_id = int(action_id)
            delta_0 = int(delta_0)
            delta_1 = int(delta_1)
            delta_2 = int(delta_2)
            delta_3 = int(delta_3)
            price = int(price)
            tome_index = int(tome_index)
            tax_count = int(tax_count)
            castable = castable != "0"
            repeatable = repeatable != "0"

            if not price:
                actions.append(Order.from_input(abs(delta_0), abs(delta_1), abs(delta_2), abs(delta_3), action_id, price))
            else:
                actions.append()


        return cls(actions)

    def __iter__(self):
        yield from self.recipes


class Player(IngredientInventory):
    def __init__(self, inventory: List[Ingredient], score: int):
        super().__init__(inventory)
        self.score = score

    @classmethod
    def from_input(cls, inv_0: int, inv_1: int, inv_2: int, inv_3: int, score: int):
        return cls(
            IngredientInventory.from_input(
                inv_0, inv_1, inv_2, inv_3
            ).ingredients,
            score
        )

    def wait(self):
        print("WAIT")


class Thinker:
    def __init__(self, player1: Player, player2: Player, orders: OrderInventory):
        self.perspective = player1
        self.opponent = player2
        self.orders = orders

    @classmethod
    def from_input(cls):
        order = OrderInventory.from_input()
        players = []
        for i in range(2):
            # inv_0: tier-0 ingredients in inventory
            # score: amount of rupees
            players.append(Player.from_input(*[int(j) for j in input().split()]))
        return cls(*players, order)

    @classmethod
    def run(cls):
        while True:
            thinker = cls.from_input()
            thinker.make_order()

    def make_order(self):
        for recipe in sorted(self.orders, key=lambda x: x.price, reverse=True):
            if recipe in self.perspective:
                recipe.brew()
                return
        self.perspective.wait()


if __name__ == '__main__':
    Thinker.run()
