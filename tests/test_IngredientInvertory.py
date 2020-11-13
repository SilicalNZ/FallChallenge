import unittest

from main import IngredientInventory, Ingredient


class TestIngredientInventory(unittest.TestCase):
    def test_IngredientInventory_ingredients(self):
        val = (True, False)
        self.assertEqual(IngredientInventory(val).ingredients, val)

    def _IngredientInventory_input(self, testcases):
        result = IngredientInventory.from_input(*testcases)
        self.assertEqual(len(result.ingredients), sum(testcases))
        for item in result.ingredients:
            self.assertTrue(testcases[item.tier])

    def test_IngredientInventory_input(self):
        testcases = (
            (0, 0, 0, 0),
            (1, 0, 0, 0),
            (0, 1, 0, 0),
            (0, 0, 1, 0),
            (0, 0, 0, 1),
            (1, 1, 1, 1)
        )

        for testcase in testcases:
            self._IngredientInventory_input(testcase)

    def test_IngredientInventory_input_return(self):
        self.assertIsInstance(IngredientInventory.from_input(0, 0, 0, 0), IngredientInventory)

    def test_IngredientInventory_contains(self):
        testcases = [
            (0, 0, 0, 0),
            (1, 0, 0, 0),
            (0, 1, 0, 0),
            (0, 0, 1, 0),
            (0, 0, 0, 1),
            (1, 1, 1, 1),
            (3, 0, 0, 0)
        ]

        for x, testcase0 in enumerate(testcases, 1):
            other_testcases = testcases[:]
            other_testcases.remove(testcase0)
            for testcase1 in other_testcases:
                compare = IngredientInventory.from_input(*testcase0)
                other = IngredientInventory.from_input(*testcase1)

                if any(i >= j and j != 0 for i, j in zip(testcase0, testcase1))\
                        and all(i >= j for i, j in zip(testcase0, testcase1)):
                    self.assertTrue(other in compare)
                    self.assertFalse(other not in compare)
                else:
                    self.assertFalse(other in compare)
                    self.assertTrue(other not in compare)
