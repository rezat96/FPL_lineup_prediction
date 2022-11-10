import unittest
import mainapp

class Testmainapp(unittest.TestCase):

    def test_budget(self):
        self.assertTrue(mainapp.check_budget(mainapp.main()))

    def test_15men_list(self):
        self.assertEqual(len(mainapp.main()), 15)

    def test_team_limit(self):
        self.assertTrue(mainapp.check_team_limit(mainapp.main(),3))
        self.assertTrue(mainapp.check_team_limit(mainapp.main(),0))     # so it can handle different!??: because logically we cannot have 0 from classes!


    # def test_divide(self):
    #     self.assertEqual(mainapp.divide(10, 5), 2)
    #     self.assertEqual(mainapp.divide(-1, 1), -1)
    #     self.assertEqual(mainapp.divide(-1, -1), 1)
    #     self.assertEqual(mainapp.divide(5, 2), 2.5)

    #     with self.assertRaises(ValueError):
    #         mainapp.divide(10, 0)


if __name__ == '__main__':
    unittest.main()