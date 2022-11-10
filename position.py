'''module docstring'''
class Position:
	''' A class which represents the positions '''
	#static attributes to keep track of number of created positions
	numberOfPositions = 0
	#parameterized constructor
	def __init__(self, singular_name, squad_min_play, squad_max_play, element_count):
		'''parametrized constructor'''
		#increment the static variable to keep track of the number of positions
		Position.numberOfPositions += 1
		#non-static attributes
		self.id_ = Position.numberOfPositions
		self.singular_name = singular_name
		self.set_plural_name()
		self.set_squad_select()
		self.squad_min_play = squad_min_play
		self.squad_max_play = squad_max_play
		self.element_count = element_count
	# plural names are obvious for each singular name
	def set_plural_name(self):
		'''set attribute called plural name'''
		if self.singular_name == 'GKP':
			self.plural_name = 'Goalkeepers'
		elif self.singular_name == 'DEF':
			self.plural_name = 'Defenders'
		elif self.singular_name == 'MID':
			self.plural_name = 'Midfielders'
		else:
			self.plural_name = 'Forwards'

	# number of select is obvious for each singular name
	def set_squad_select(self):
		'''set attribute called squad select'''
		if self.singular_name == 'GKP':
			self.squad_select = 2
		elif self.singular_name == 'DEF':
			self.squad_select = 5
		elif self.singular_name == 'MID':
			self.squad_select = 5
		else:
			self.squad_select = 3
