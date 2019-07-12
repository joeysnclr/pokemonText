class Battle(object):

	def __init__(self, player, comp):
		self.player = player
		self.comp = comp
		self.turns = 0
		self.winner = None
		self.loser = None

	def battleMessage(self):
		print('\n' * 5)
		self.printBattleStatus()
		print('\n' * 5)
		input()
		return self

	def printBattleStatus(self):
		print('{:45s}{:45s}'.format('You', 'Opponent'))
		print('{:45s}{:45s}\n'.format(str(self.player), str(self.comp)))
		return self

	def printStartMessage(self):
		print('Go {}!!'.format(self.player.name))
		print('The Opponent is using {}'.format(self.comp.name))
		print('\n' * 5)
		self.printBattleStatus()
		print()
		return self

	def checkBattleOver(self):
		return self.player.stats['CurrHP'] == 0 or self.comp.stats['CurrHP'] == 0

	def battleOver(self):
		if self.player.stats['CurrHP'] == 0:
			self.winner = self.comp
			self.loser = self.player
		else:
			self.winner = self.player
			self.loser = self.comp
		print('{} beat {}!'.format(self.winner.name, self.loser.name))
		print('\n' * 11)
		input()
		return self

	def playerTurn(self):
		self.player.printAttacks()
		attackIndex = int(input('Enter desired attack # >> '))
		print('\n' * 5)
		chosenAttack = self.player.attacks[attackIndex]
		self.player.attackOpponent(self.comp, chosenAttack)
		return self

	def compTurn(self):
		computerAttack = self.comp.randomAttack()
		self.comp.attackOpponent(self.player, computerAttack)
		return self

	def start(self):
		self.printStartMessage()
		turns = 0
		while not self.checkBattleOver():
			turnIndex = turns % 2
			if turnIndex == 0:
				self.playerTurn()
			else:
				# computers turn
				self.compTurn()

			turns += 1

			self.battleMessage()
		self.battleOver()

class TrainerBattle2(object):

	def __init__(self, user, opponent):
		self.user = user
		self.opponent = opponent


	def isBattleOver(self):
		#fix this code

		return self.user.nextAlivePokemon() == False or self.opponent.nextAlivePokemon() == False

	def start(self):
		# while both trainers have alive pokemon
			# 
		while not self.isBattleOver():
			Battle(self.user.nextAlivePokemon(), self.opponent.nextAlivePokemon()).start()


		return self
