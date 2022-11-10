'''module docstring'''
class Team:
    ''' A class which represents the teams '''
    #static attribute to keep track of number of created teams
    numberOfTeams = 0
    #parameterized constructor
    def __init__(self, name, short_name, loss, draw, win, position):
        '''parametrized constructor'''
        #increment the static variable to keep track of number of teams
        Team.numberOfTeams += 1
        #non-static attribute
        self.id_ = Team.numberOfTeams
        self.name = name
        self.short_name = short_name
        self.loss = loss
        self.draw = draw
        self.win = win
        self.set_played()
        self.set_point()
        self.position = position

    def set_played(self):
        ''' set play attribute with sum of win, lose and draw '''
        self.played = self.win + self.loss + self.draw

    def set_point(self):
        '''calculation of points is as follows'''
        self.point = (3 * self.win) + (1 * self.draw)
