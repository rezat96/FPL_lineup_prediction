'''
This module define and run the unittest class
'''
import unittest
import mainapp

class Testmainapp(unittest.TestCase):
    '''
    This class is the main testing unit, which tests 3 scenarios
    1) test_budget: checks if the final team has a total_value < 1000
    2) test_15Men: checks if the final team has exactly 15 components
    3) test_team_limit: checks the constraint that no team should have more than 3
    members from the same preimer league team
    '''

    def test_budget(self):
        '''check team budget constrain(< 1000)'''
        self.assertTrue(mainapp.check_budget(mainapp.main()))

    def test_15men_list(self):
        '''check we have a 15-Men team'''
        #check to see if the final output is a 15men
        self.assertEqual(len(mainapp.main()), 15)

    def test_team_limit(self):
        '''check team_limit constraint'''
        #check to see if it can hadle the number of  players constraint
        self.assertTrue(mainapp.check_team_limit(mainapp.main(),3))
## running the tests
if __name__ == '__main__':
    unittest.main()
