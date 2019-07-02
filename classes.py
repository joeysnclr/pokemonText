import random, time, json
from math import floor, ceil, sqrt

'''
To Do
 - create moves.json
 - assign a pokemon moves based on creation

'''

class Pokedex(object):

	def __init__(self):
		with open('pokedex.json', 'r+') as file:
			self.entries = json.load(file)
		for entry in self.entries:
			entry['seen'] = False
		self.totalEntries = len(self.entries)
		self.seenEntries = 0

	def __str__(self):
		pokedexString = ''
		for entry in self.entries:
			if entry['seen']:
				seenEntryName = entry['name']['english']
			else:
				seenEntryName = ''
			entryString = '{:3} | {}\n'.format(entry['id'], seenEntryName)
			pokedexString += entryString
		totalString = 'You have seen {}/{} Pokemon.'.format(self.seenEntries, self.totalEntries)
		pokedexString += totalString
		return pokedexString

	def seenNew(self, pokedexId):
		self.entries[pokedexId - 1]['seen'] = True
		self.seenEntries += 1
		return self

	def seenAll(self):
		for i in range(len(self.entries)):
			self.seenNew(i)
		return self

	def seenPokemon(self):
		seenEntryList = []
		for entry in self.entries:
			if entry['seen']:
				seenEntryList.append(entry)
		return seenEntryList

class Trainer(object):

	def __init__(self, name, pokemon=None):
		self.name = name
		if pokemon == None:
			self.pokemon = []
		else:
			self.pokemon = pokemon
		self.pc = []
		self.money = 0
		self.pokedex = Pokedex() #maybe make pokedex a class?

	def __str__(self):
		trainerString = '{} | ${} | Pokedex: {}/{}'.format(self.name, self.money, self.pokedex.seenEntries, self.pokedex.totalEntries)
		for poke in self.pokemon:
			trainerString += '\n\t'+str(poke)
		return trainerString

	def addPokemon(self, pokemon):
		if len(self.pokemon) < 6:
			self.pokemon.append(pokemon)
		else:
			self.pc.append(pokemon)
		return self

	def nextAlivePokemon(self):
		for poke in self.pokemon:
			if poke.alive():
				return poke
		return False

class Pokemon(object):
	"""pocket monster"""
	def __init__(self, name, level=1):

		self.name = name
		self.pokedexData = self.getPokedexEntry()
		self.level = level
		self.attacks = []
		self.createMoveset()
		self.pokeTypes = self.pokedexData['type']


		self.IV = random.randint(0,15)
		self.EV = 128 # (effort value) (0-255) https://bulbapedia.bulbagarden.net/wiki/Statistic#Determination_of_stats

		self.baseStats = self.pokedexData['base']
		self.stats = self.getStats()

		# https://www.serebii.net/games/exp.shtml
		self.xp = self.level ** 3
		self.xpNeeded = ((self.level + 1) ** 3)


	def __str__(self):
		lastLevelXpNeeded = ((self.level) ** 3)
		currLvlXP = self.xp - lastLevelXpNeeded
		currLvlXPNeeded = self.xpNeeded - lastLevelXpNeeded

		pokeString = '{} | Lvl: {} | HP: {}/{} | XP: {}/{}'.format(self.name, self.level, self.stats['CurrHP'], self.stats['HP'], currLvlXP, currLvlXPNeeded)
		return pokeString

	def calcHpStat(self):

		return floor((( 2 * self.baseStats['HP'] + self.IV + floor( sqrt(self.EV / 4) ) ) * self.level) / 100) + self.level + 10

	def calcOtherStat(self, statName):

		return floor((( 2 * self.baseStats[statName] + self.IV + floor( sqrt(self.EV / 4) ) ) * self.level) / 100) + 5

	def getStats(self):
		statDict = {
			"HP": self.calcHpStat(),
			"CurrHP": self.calcHpStat(),
			"Attack": self.calcOtherStat('Attack'),
			"Defense": self.calcOtherStat('Defense'),
			"Sp. Attack": self.calcOtherStat('Sp. Attack'),
			"Sp. Defense": self.calcOtherStat('Sp. Defense'),
			"Speed": self.calcOtherStat('Speed')
			}
		return statDict

	def getPokedexEntry(self):
		with open('pokedex.json', 'r+') as file:
			pokedex = json.load(file)
		for poke in pokedex:
			if poke['name']['english'].lower() == self.name.lower():
				return poke

	def evolve(self):
		shouldEvolve = False
		for evo in self.pokedexData['evolutions']:
			if 'from' in evo:
				if evo['from'] == self.pokedexData['id']:
					if evo['trigger_lvl'] <= self.level:
						shouldEvolve = True
						newEvo = evo
						break


		if shouldEvolve:
			oldName = self.name
			print('{} is evolving!'.format(oldName))
			self.name = newEvo['name']
			self.pokedexData = self.getPokedexEntry()
			print('{} evolved into {}'.format(oldName, self.name))



		return self

	def gainXp(self, amount):
		self.xp += amount
		self.levelUp()
		return self

	def levelUp(self):
		while self.xp >= self.xpNeeded and self.level < 25:
			print('Level up!')
			# is able to level up
			self.level += 1
			self.stats = self.getStats()
			self.xpNeeded = (self.level + 1) ** 3
			self.evolve()
			print(self)
		return self

	def printAttacks(self):
		i = 0
		for a in self.attacks:
			print('[{}] - {}'.format(i, a))
			i += 1
		return self

	def teachAttack(self, attack):
		if len(self.attacks) == 4:
			print('{} wants to learn {}'.format(self.name, attack.name))
			forgetMove = input('{} already knows 4 moves. Would you like to delete one? (y/n) >>> '.format(self.name))
			if forgetMove == 'y':
				i = 0
				for a in self.attacks:
					print('{} | {}'.format(i, a))
					i += 1
				validChoice = False
				while not validChoice:
					choiceIndex = input('Which attack should be forgotten? >>> ')
					try:
						choiceIndex = int(choiceIndex)
					except ValueError:
						print('Must be a number!')
						continue
					if choiceIndex not in range(i):
						print('Must be a valid option!')
						continue
					validChoice = True
				self.attacks.pop(choiceIndex)
				self.attacks.append(attack)
				print('{} learned {}!'.format(self.name, attack.name))
			else:
				print('{} did not learn {}'.format(self.name, attack.name))
		else:
			self.attacks.append(attack)
		return self

	def createMoveset(self):
		possibleLearnedMoves = []
		for m in self.pokedexData['learnableMoves']:
			if m['level'] <= self.level:
				possibleLearnedMoves.append(m)
		if len(possibleLearnedMoves) >= 4:
			while len(self.attacks) < 4:
				atkNames = [a.name for a in self.attacks]
				atk = random.choice(possibleLearnedMoves)
				if atk['name'] not in atkNames:
					self.attacks.append(Attack(atk['name'], atk['type'], atk['pp'], atk['damage']))

		else:
			for m in possibleLearnedMoves:
				self.attacks.append(Attack(m['name'], m['type'], m['pp'], m['damage']))

		return self

	def alive(self):
		return self.stats['CurrHP'] > 0

	def randomAttack(self):

		return random.choice(self.attacks)


	def attackOpponent(self, opponent, attack):
		print('\n{} used {}!'.format(self.name, attack.name))
		attack.currPp -= 1 # subtracts 1 power point

		# https://www.serebii.net/games/damage.shtml

		typeMultiplier = attack.damageMultiplier(opponent)
		if typeMultiplier > 1:
			print('It was very effective')
		elif typeMultiplier < 1:
			print('It was not very effective')

		if attack.attackType in self.pokeTypes:
			STAB = 1.5
		else:
			STAB = 1

		damageToBeDealt = round(((((2 * self.level / 5 + 2) * self.stats['Attack'] * attack.baseDamage / opponent.stats['Defense']) / 50) + 2) * STAB * typeMultiplier * random.randint(85, 100) / 100)


		opponent.stats['CurrHP'] -= damageToBeDealt
		if opponent.stats['CurrHP'] < 0:
			opponent.stats['CurrHP'] = 0
		print()
		return self

class Attack(object):
	'''An action that a pokemon uses against another'''
	def __init__(self, name, attackType, maxPp, baseDamage):
		self.name = name
		self.attackType = attackType
		self.currPp = maxPp
		self.maxPp = maxPp
		self.baseDamage = baseDamage
		with open('types.json', 'r+') as file:
			types = json.load(file)
		self.attackInfo = types[self.attackType]

	def __str__(self):
		attackString = '{} | {} | PP: {}/{} | Dmg: {}'.format(self.name, self.attackType, self.currPp, self.maxPp, self.baseDamage)
		return attackString

	def damageMultiplier(self, opponent):
		# uses the attack type compared to the defenders types to find an damage multiplier
		damageMultiplier = 1
		for weak_type in self.attackInfo['weaknesses']:
			for pokeType in opponent.pokeTypes:
				if pokeType in weak_type:
					damageMultiplier = damageMultiplier / 2
		for strong_type in self.attackInfo['strengths']:
			for pokeType in opponent.pokeTypes:
				if pokeType in strong_type:
					damageMultiplier = damageMultiplier * 2
		return damageMultiplier

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

class TrainerBattle(object):

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














