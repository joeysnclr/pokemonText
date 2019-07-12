import random, time, json
from math import floor, ceil, sqrt
from tools import *


class Pokedex(object):

	def __init__(self):
		with open('pokedex.json', 'r+') as file:
			self.entries = json.load(file)
		for entry in self.entries:
			entry['seen'] = False
		self.totalEntries = len(self.entries)

	def __str__(self):
		pokedexString = ''
		for entry in self.entries:
			if entry['seen']:
				seenEntryName = entry['name']['english']
			else:
				seenEntryName = ''
			entryString = '{:3} | {:15} | {}\n'.format(entry['id'], seenEntryName, entry['type'])
			pokedexString += entryString
		totalString = 'You have seen {}/{} Pokemon.'.format(self.seenEntries(), self.totalEntries)
		pokedexString += totalString
		return pokedexString

	def seenEntries(self):
		count = 0
		for p in self.entries:
			if p['seen']:
				count += 1
		return count


	def seenNew(self, pokedexId):
		self.entries[pokedexId - 1]['seen'] = True
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

	def __init__(self, name, pokemon=None, mainPlayer=False, gymLeader=False):
		self.name = name
		self.mainPlayer = mainPlayer
		self.gymLeader = gymLeader
		if pokemon == None:
			self.pokemon = []
		else:
			self.pokemon = pokemon
		self.pc = []
		self.bag = Bag()
		self.money = 0
		self.pokedex = Pokedex() #maybe make pokedex a class?
		self.location = 'Laupel City'
		self.gymBadges = [1,2,3]
		self.activePoke = None
		self.blackout = False
		self.defeated = False

	def __str__(self):
		trainerString = '{} | ${}\nPokedex: {}/{}\nGym Badges: {}'.format(self.name, self.money, self.pokedex.seenEntries(), self.pokedex.totalEntries, len(self.gymBadges))
		return trainerString

	def gainMoney(self, amount):
		self.money += amount
		if amount > 0:
			input('You have gained ${}'.format(amount))
		else:
			input('You have lost ${}'.format(abs(amount)))
		return self


	def heal(self):
		for p in self.pokemon:
			p.stats['CurrHP'] = p.stats['HP']
			for a in p.attacks:
				a.currPp = a.maxPp
		return self

	def wager(self):
		base = random.randint(75,125)
		totalLvl = 0
		for p in self.pokemon:
			totalLvl += p.level

		return base * totalLvl

	def addPokemon(self, pokemon):
		if len(self.pokemon) < 6:
			self.pokemon.append(pokemon)
		else:
			input('{} has been transferred to your PC.'.format(pokemon.name))
			self.pc.append(pokemon)
		self.pokedex.seenNew(pokemon.pokedexData['id'])
		return self

	def switchActivePoke(self):
		alivePoke = []
		for p in self.pokemon:
			if p.alive():
				alivePoke.append(p)
		alivePoke.append('Exit')
		pokeIndex = userChoice(alivePoke, 'Choose a Pokemon to switch in')
		choice = alivePoke[pokeIndex]
		if choice == 'Exit':
			return False
		else:
			self.activePoke = alivePoke[pokeIndex]
			return True

	def changePartyLeader(self):
		choices = []
		for p in self.pokemon:
			choices.append(p.name)
		choices.append('Exit')

		choiceIndex = userChoice(choices, 'Which pokemon should be the party leader?')
		choice = choices[choiceIndex]
		if choice == 'Exit':
			return self
		else:
			self.pokemon.insert(0, self.pokemon.pop(choiceIndex))
		return self


	def nextAlivePokemon(self):
		for poke in self.pokemon:
			if poke.alive():
				return poke
		return None

class Bag(object):

	def __init__(self):
		self.items = {}

	def __str__(self):
		returnStr = 'Your Bag\n'
		for item in self.items:
			returnStr += '{}x | {}\n'.format(self.items[item], item)
		return returnStr


	def addItem(self, aItemName):
		if aItemName in self.items:
			self.items[aItemName] += 1
		else:
			self.items[aItemName] = 1
		return self

	def deleteItem(self, dItemName):
		# deletes one of the item that should be deleted
		self.items[dItemName] -= 1
		if self.items[dItemName] == 0:
			self.items.pop(dItemName, None)

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
			input('{} is evolving!'.format(oldName))
			self.name = newEvo['name']
			self.pokedexData = self.getPokedexEntry()
			input('{} evolved into {}'.format(oldName, self.name))



		return self

	def gainXp(self, amount):
		self.xp += amount
		input('{} has gained {} XP'.format(self.name, amount))
		self.levelUp()
		return self

	def checkNewMoves(self):
		for move in self.pokedexData['learnableMoves']:
			if move['level'] == self.level:
				self.teachAttack(Attack(move['name'], move['type'], move['pp'], move['damage']))
		return self

	def levelUp(self):
		while self.xp >= self.xpNeeded and self.level < 25:
			input('Level up!')
			# is able to level up
			currHp = self.stats['CurrHP']
			maxHp = self.stats['HP']
			self.level += 1
			self.stats = self.getStats()
			HpIncrease = self.stats['HP'] - maxHp # keeps the current HP the same when leveling up only w/ the hp increase
			self.stats['CurrHP'] = currHp + HpIncrease


			self.xpNeeded = (self.level + 1) ** 3
			self.evolve()
			self.checkNewMoves()
			input(self)
		return self

	def teachAttack(self, attack):
		if len(self.attacks) == 4:
			input('{} wants to learn {}'.format(self.name, attack.name))
			input(attack)
			input('{} already knows 4 moves!'.format(self.name))
			choices = ['Yes', 'No']
			choiceIndex = userChoice(choices, 'Would you like to make {} forget a move?'.format(self.name))
			choice = choices[choiceIndex]
			if choice == 'Yes':
				choices = []
				for a in self.attacks:
					choices.append(a)
				choiceIndex = userChoice(choices, 'What move should be forgotten?')
				self.attacks.pop(choiceIndex)
				self.attacks.append(attack)
				input('{} forgot {}....'.format(self.name, choices[choiceIndex].name))
				input('{} learned {}!'.format(self.name, attack.name))
			else:
				input('{} did not learn {}'.format(self.name, attack.name))
		else:
			input('{} learned {}!'.format(self.name, attack.name))
			self.attacks.append(attack)
		return self

	def createMoveset(self):
		possibleLearnedMoves = []
		for m in self.pokedexData['learnableMoves']:
			if m['level'] <= self.level:
				possibleLearnedMoves.append(m)
		if len(possibleLearnedMoves) >= 4:
			# adds 4 random attacks to moveset
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

	def usableAttacks(self):
		struggle = Attack('Struggle', 'Normal', 100, 10)
		usable = []
		for a in self.attacks:
			if a.currPp > 0:
				usable.append(a)
		if len(usable) == 0:
			usable.append(struggle)
		return usable

	def randomAttack(self):

		return random.choice(self.usableAttacks())

	def attackOpponent(self, opponent, attack):
		input('{} used {}!'.format(self.name, attack.name))
		attack.currPp -= 1 # subtracts 1 power point

		# https://www.serebii.net/games/damage.shtml

		typeMultiplier = attack.damageMultiplier(opponent)
		if typeMultiplier > 1:
			input('It was very effective')
		elif typeMultiplier < 1:
			input('It was not very effective')


		if attack.attackType in self.pokeTypes:
			STAB = 1.5
		else:
			STAB = 1

		damageToBeDealt = round(((((2 * self.level / 5 + 2) * self.stats['Attack'] * attack.baseDamage / opponent.stats['Defense']) / 50) + 2) * STAB * typeMultiplier * random.randint(85, 100) / 100)


		opponent.stats['CurrHP'] -= damageToBeDealt
		if opponent.stats['CurrHP'] <= 0:
			input('{} has fainted.'.format(opponent.name))
			opponent.stats['CurrHP'] = 0
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

class TrainerBattle(object):

	def __init__(self, user, opp):
		self.user = user
		self.opp = opp
		self.turns = 0
		self.runAway = False
		self.pokemonCaught = False
		self.user.activePoke = self.user.nextAlivePokemon()
		self.opp.activePoke = self.opp.nextAlivePokemon()
		if self.opp.name == 'Wild':
			self.wildBattle = True
		else:
			self.wildBattle = False
		if self.wildBattle:
			self.userChoices = ['Attack', 'Bag', 'Pokemon', 'Run']
		else:
			self.userChoices = ['Attack', 'Bag', 'Pokemon']


	def battleStatus(self):
		you = 'You ({})'.format(len(self.user.pokemon))
		opp = 'Opponent ({})'.format(len(self.opp.pokemon))
		print('{:45s}{:45s}'.format(you, opp))
		print('{:45s}{:45s}\n'.format(str(self.user.activePoke), str(self.opp.activePoke)))
		return self


	def checkBattleOver(self):
		# battle is over if one of the trainers has 0 pokemon alive or when nextAlivePokemon == None
		over = self.user.nextAlivePokemon() == None or self.opp.nextAlivePokemon() == None
		return over
		
	def battleOver(self):
		amount = self.opp.wager()
		if self.user.nextAlivePokemon() == None: # the opponent won, user blacks out
			self.user.heal()
			self.user.blackout = True
			amount = -1 * amount
		else:
			if not self.wildBattle:
				self.opp.defeated = True
				print('You have defeated {}'.format(self.opp.name))

		if not self.wildBattle: # money is gained or lost in a trainer battle
			self.user.gainMoney(amount)


		# if it is not a wild battle
			# if user lost, heal their pokemon and set self.blackout to True. This tells the main game function that the user should retreat from the route they are on

		# add/subtract money from user
		return self

	def giveXP(self):
		if self.wildBattle:
			trainerMultiplier = 1
		else:
			trainerMultiplier = 1.5
		pokeXpStat = 62 # (gotten from fainted pokemon) THIS SHOULD BE A STAT FOR EACH POKEMON. FETCH FROM HERE https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_effort_value_yield
		
		amount = round((trainerMultiplier * pokeXpStat * self.opp.activePoke.level) / 7)
		self.user.activePoke.gainXp(amount)

	def userAttack(self):
		# returns True if user attacked, False if exited
		attackChoices = self.user.activePoke.usableAttacks()
		attackChoices.append('Exit')
		attackIndex = userChoice(attackChoices, 'Choose an attack')
		chosenAttack = attackChoices[attackIndex]
		if chosenAttack == 'Exit': # the user chose to exit
			return False
		else: #The user chose an attack
			self.user.activePoke.attackOpponent(self.opp.activePoke, chosenAttack)
			return True

	def userBag(self):
		itemStrList = []
		itemNameList = []
		for item in self.user.bag.items:
			itemStr = '{}x | {}'.format(self.user.bag.items[item], item)
			itemStrList.append(itemStr)
			itemNameList.append(item)
		itemStrList.append('Exit')
		choiceIndex = userChoice(itemStrList, 'What item would you like to use?')
		choice = itemStrList[choiceIndex]
		if choice == 'Exit':
			return False
		else:
			item = itemNameList[choiceIndex]
			if 'Ball' in item:
				if self.wildBattle:
					pokemonCaught = PokeBall(item).catchPokemon(self.user, self.opp.activePoke)
					self.pokemonCaught = pokemonCaught
				else:
					input("You can only use Poke Balls in the wild!")
					return False
			elif 'Potion' in item:
				Potion(item).healPokemon(self.user.activePoke)
			else:
				print('This item is not recognized')
				return False
			self.user.bag.deleteItem(item)
			return True

		return False

	def userRun(self):
		if self.user.activePoke.level >= self.opp.activePoke.level:
			input('Got away safely!')
			self.runAway = True
		else:
			input('Could not escape!')
		return True

	def userTurn(self):
		completeTurn = False
		while not completeTurn:
			choiceIndex = userChoice(self.userChoices, 'What will you do?')
			choice = self.userChoices[choiceIndex]
			if choice == 'Attack':
				completeTurn = self.userAttack()
			elif choice == 'Bag':
				completeTurn = self.userBag()
			elif choice == 'Pokemon':
				completeTurn = self.user.switchActivePoke()
			elif choice == 'Run':
				completeTurn = self.userRun()

	def oppTurn(self):
		# the opponent chooses a random attack
		chosenAttack = self.opp.activePoke.randomAttack()
		self.opp.activePoke.attackOpponent(self.user.activePoke, chosenAttack)
		return self


	def start(self):
		if self.opp.defeated:
			return
		if self.wildBattle:
			input('{} appeared from the wild'.format(self.opp.activePoke.name))
		else:
			input('You have encountered {}'.format(self.opp.name))
			input('{} sent out {}'.format(self.opp.name, self.opp.activePoke.name))
		input('You sent out {}'.format(self.user.activePoke.name))
		self.battleStatus()
		while not self.checkBattleOver():
			input()
			if self.turns % 2 == 0:
				# user turn
				# attack, bag, pokemon, run (if wild)
				self.userTurn()
			else:
				self.oppTurn()
				# opp turn
			if self.runAway or self.pokemonCaught:
				return

			self.battleStatus()

			# checks for fainted activePoke
			if not self.user.activePoke.alive():
				if self.user.nextAlivePokemon() != None:
					self.user.switchActivePoke()
				else:
					input('You have 0 Pokemon left!')
					input('You blacked out!')
			if not self.opp.activePoke.alive():
				self.giveXP()
				if len(self.user.pokemon) > 0:
					# switches opponents pokemon to the next available one
					self.opp.activePoke = self.opp.nextAlivePokemon()
					if not self.wildBattle and self.opp.activePoke != None:
						input('{} has sent out {}!'.format(self.opp.name, self.opp.activePoke.name))

			if self.opp.activePoke != None:
				self.user.pokedex.seenNew(self.opp.activePoke.pokedexData['id']) # makes sure that the opponents pokemon is now seen in the pokedex
			self.turns += 1

		self.battleOver()

class PokeBall(object):

	def __init__(self, name):
		ballMultipliers = {
			"Poke Ball": 1,
			"Great Ball": 1.5,
			"Ultra Ball": 2,
		}
		self.name = name
		self.multiplier = ballMultipliers[self.name]
		self.usableOutsideBattle = False

	def catchPokemon(self, trainer, pokemon):
		input('You threw a {}!'.format(self.name))
		input('{} is in the ball!'.format(pokemon.name))
		HPmax = pokemon.stats['HP']
		HPcurr = pokemon.stats['CurrHP']
		rate = 255
		# https://bulbapedia.bulbagarden.net/wiki/Catch_rate (Gen 3-4)
		catchRate = round(((3 * HPmax - 2 * HPcurr) * rate * self.multiplier) / (3 * HPmax))
		randomNum = random.randint(0,255)
		if randomNum <= catchRate:
			input('Congratulations! You have caught {}!'.format(pokemon.name))
			trainer.addPokemon(pokemon)
			return True
		else:
			input('Uh oh! The wild {} escaped from the ball!'.format(pokemon.name))
			return False

class Potion(object):

	def __init__(self, name):
		hpKey = {
			"Potion": 15,
			"Super Potion": 40,
			"Max Potion": 999
		}
		self.name = name
		self.hp = hpKey[self.name]
		self.usableOutsideBattle = True

	def healPokemon(self, pokemon):
		input('You used a {} on {}'.format(self.name, pokemon.name))
		pokemon.stats['CurrHP'] += self.hp
		if pokemon.stats['CurrHP'] > pokemon.stats['HP']:
			pokemon.stats['CurrHP'] = pokemon.stats['HP']
		return self







