class Command(object):
	''' Hang on, is this how I make commands modular? '''
	def __init__(self, syntax=None, rules=None, state_changes=None, errors=None):
		self.syntax = syntax
		self.rules = rules
		self.state_changes = state_changes
		self.errors = errors

		# what else do I need here?