import pickle
from classes import *
from tools import *
from random import randint, choice
import numpy.random

# ask brendan to make the storyline
# storyline sepecifications
# - almost completely linear
# - route unlocks after gym badges



choices = ['New Game', 'Load Game']
# choiceIndex = userChoice(choices, 'Where would you like to start from?')
choiceIndex = 0
choice = choices[choiceIndex]
if choice == 'New Game':
	gameData = {
		"newGame": True,
		"trainer": Trainer(''),
		"wildEncounterChance": 25,
		"starterLevel": 2,
		"pokeMartItems": {
			"Potion": {
				"gymBadgesRequired": 0,
				"price": 150
			},
			"Super Potion": {
				"gymBadgesRequired": 1,
				"price": 350
			},
			"Max Potion": {
				"gymBadgesRequired": 3,
				"price": 600
			},
			"Poke Ball": {
				"gymBadgesRequired": 0,
				"price": 100
			},
			"Great Ball": {
				"gymBadgesRequired": 1,
				"price": 300
			},
			"Ultra Ball": {
				"gymBadgesRequired": 2,
				"price": 600
			}
		},
		"locations": {
			"Ecrin Town": {
				"city": True,
				"gym": False,
				"pokecenter": True,
				"pokemart": False,
				"paths": [
					"Route 001"
				],
				"npcs": [
					{
						"name": "Mom",
						"messages": [
							"I hope your adventure is going well sweetie!"
						]
					}

				]
			},
			"Route 001": {
				"gymBadgesRequired": 0,
				"city": False,
				"trainers": [
					Trainer('Trainer Jenny', [Pokemon('Machop', 2)]),
					Trainer('Trainer Ryan', [Pokemon('Starly', 2)])
				],
				"wild": [
					{
						"name": "Starly",
						"lvlRange": (1,2),
						"chance": .75
					},
					{
						"name": "Shinx",
						"lvlRange": (1,2),
						"chance": .25
					}
				],
				"travelKey": {
					"Ecrin Town": "Velia Town",
					"Velia Town": "Ecrin Town"
				}
			},
			"Velia Town": {
				"city": True,
				"gym": False,
				"pokecenter": True,
				"pokemart": True,
				"paths": [
					"Route 001",
					"Route 002",
					"Route 003"
					]
			},
			"Route 002": {
				"gymBadgesRequired": 0,
				"city": False,
				"trainers": [
					Trainer('Trainer Alexander', [Pokemon('Machop', 4), Pokemon('Chimchar', 4)]),
					Trainer('Trainer Alexander', [Pokemon('Turtwig', 4)])
				],
				"wild": [
					{
						"name": "Starly",
						"lvlRange": (2,3),
						"chance": .33
					},
					{
						"name": "Shinx",
						"lvlRange": (2,3),
						"chance": .33
					}
					,
					{
						"name": "Machop",
						"lvlRange": (3,4),
						"chance": .34
					}
				],
				"travelKey": {
					"Casno City": "Velia Town",
					"Velia Town": "Casno City"
				}
			},
			"Casno City": {
				"city": True,
				"gym": True,
				"pokecenter": True,
				"pokemart": True,
				"gymData": {
					"type": "Normal",
					"trainers": [
						Trainer('Gym Rat Rex', [Pokemon('Staravia', 6)]),
						Trainer('Gym Rat Xavier', [Pokemon('Munchlax', 6)]),
						Trainer('Gym Leader Nolan', [Pokemon('Staravia', 7), Pokemon('Munchlax', 7)], gymLeader=True)
					],
					"leaderMessages": {
						"beforeBattle": [
							"I see...",
							"A new challenger has surpased my assistants.",
							"My Pokemon's type might be Normal...",
							"But their trainer is not!"
						],
						"afterBattle": [
							'Wow...',
							'You have exceeded my expectations.',
							'Here. Take this badge.',
							'Now you will be able to travel farther and face more challenges in your journey.',
							'I wish you good luck!'
						]
					}
				},
				"paths": [
					"Route 002",
					"Route 004"
					]
			},
			"Route 003": {
				"gymBadgesRequired": 1,
				"city": False,
				"trainers": [
					Trainer('Birdkeeper Mary', [Pokemon('Staravia', 5)]),
					Trainer('Surfer Mark', [Pokemon('Buizel', 4), Pokemon('Piplup', 4)])
				],
				"wild": [
					{
						"name": "Gastly",
						"lvlRange": (3,4),
						"chance": .20
					},
					{
						"name": "Shinx",
						"lvlRange": (3,4),
						"chance": .35
					},
					{
						"name": "Machop",
						"lvlRange": (3,4),
						"chance": .35
					}
					,
					{
						"name": "Pichu",
						"lvlRange": (4,4),
						"chance": .10
					}
				],
				"travelKey": {
					"Laupel City": "Velia Town",
					"Velia Town": "Laupel City"
				}
			},
			"Laupel City": {
				"city": True,
				"gym": False,
				"pokecenter": True,
				"pokemart": True,
				"paths": [
					"Route 003",
					"Route 005",
					"Route 006"
					],
				"sailing": "Seagrass Island"
			},
			"Route 004": {
				"gymBadgesRequired": 1,
				"city": False,
				"trainers": [
					Trainer('Trainer Armando', [Pokemon('Gastly', 5), Pokemon('Ponyta', 6)]),
					Trainer('Trainer Veronica', [Pokemon('Floatzel', 6), Pokemon('Ponyta', 7)])
				],
				"wild": [
					{
						"name": "Buizel",
						"lvlRange": (4,6),
						"chance": .25
					},
					{
						"name": "Ponyta",
						"lvlRange": (4,6),
						"chance": .25
					}
					,
					{
						"name": "Machop",
						"lvlRange": (4,6),
						"chance": .50
					}
				],
				"travelKey": {
					"Casno City": "Tapron Town",
					"Tapron Town": "Casno City"
				}
			},
			"Tapron Town": {
				"city": True,
				"gym": False,
				"pokecenter": True,
				"pokemart": True,
				"paths": [
					"Route 004",
					"Route 008",
					"Route 005"
					]
			},
			"Route 005": {
				"gymBadgesRequired": 1,
				"city": False,
				"trainers": [
					Trainer('Rock Climber Pablo', [Pokemon('Pikachu', 7), Pokemon('Monferno', 7)]),
					Trainer('Breeder Nico', [Pokemon('Grotle', 7), Pokemon('Riolu', 7)])
				],
				"wild": [
					{
						"name": "Staravia",
						"lvlRange": (5,7),
						"chance": .50
					},
					{
						"name": "Haunter",
						"lvlRange": (6,7),
						"chance": .2
					},
					{
						"name": "Pikachu",
						"lvlRange": (5,7),
						"chance": .2
					},
					{
						"name": "Gible",
						"lvlRange": (5,6),
						"chance": .1
					}
				],
				"travelKey": {
					"Laupel City": "Tapron Town",
					"Tapron Town": "Laupel City"
				}
			},
			"Route 006": {
				"gymBadgesRequired": 1,
				"city": False,
				"trainers": [
					Trainer('Electrician Jerry', [Pokemon('Pikachu', 9), Pokemon('Luxray', 9)]),
					Trainer('Trainer Mandy', [Pokemon('Floatzel', 10), Pokemon('Prinplup', 9)])
				],
				"wild": [
					{
						"name": "Luxio",
						"lvlRange": (7,7),
						"chance": .30
					},
					{
						"name": "Floatzel",
						"lvlRange": (7,8),
						"chance": .30
					},
					{
						"name": "Haunter",
						"lvlRange": (7,8),
						"chance": .1
					}
					,
					{
						"name": "Machoke",
						"lvlRange": (7,8),
						"chance": .30
					}
				],
				"travelKey": {
					"Laupel City": "Jetano City",
					"Jetano City": "Laupel City"
				}
			},
			"Jetano City": {
				"city": True,
				"gym": False,
				"pokecenter": True,
				"pokemart": True,
				"gymData": {
					"type": "Electric",
					"trainers": [
						Trainer('Gym Rat Ernest', [Pokemon('Raichu', 10)]),
						Trainer('Gym Rat Ethan', [Pokemon('Luxray', 9), Pokemon('Luxray', 9)]),
						Trainer('Gym Leader Ian', [Pokemon('Raichu', 10), Pokemon('Luxray', 10)], gymLeader=True)
					],
					"leaderMessages": {
						"beforeBattle": [
							"I see...",
							"A new challenger has surpased my assistants.",
							"My Pokemon's type might be Normal..."
							"But their trainer is not!"
						],
						"afterBattle": [
							'Wow...',
							'You have exceeded my expectations.',
							'Here. Take this badge.',
							'Now you will be able to travel farther and face more challenges in your journey.',
							'I wish you good luck!'
						]
					}
				},
				"paths": [
					"Route 006",
					"Route 007"
					]
			},
			"Route 007": {
				"gymBadgesRequired": 2,
				"city": False,
				"trainers": [
					Trainer('Climber Rocky', [Pokemon('Machamp', 10)]),
					Trainer('Trainer Ricardo', [Pokemon('Staraptor', 11), Pokemon('Floatzel', 10)]),
					Trainer('Breeder Ignacio', [Pokemon('Rapidash', 11)])
				],
				"wild": [
					{
						"name": "Ponyta",
						"lvlRange": (9,10),
						"chance": .35
					},
					{
						"name": "Machoke",
						"lvlRange": (9,10),
						"chance": .35
					},
					{
						"name": "Sneasel",
						"lvlRange": (9,10),
						"chance": .15
					},
					{
						"name": "Riolu",
						"lvlRange": (9,10),
						"chance": .15
					}
				],
				"travelKey": {
					"Corenes City": "Jetano City",
					"Jetano City": "Corenes City"
				}
			},
			"Route 008": {
				"gymBadgesRequired": 2,
				"city": False,
				"trainers": [
					Trainer('Businessman Isaac', [Pokemon('Snorlax', 11)]),
					Trainer('Swimmer Mike', [Pokemon('Floatzel', 12)]),
					Trainer('Climber Ivan', [Pokemon('Machamp', 10), Pokemon('Sneasel', 10)]),
				],
				"wild": [
					{
						"name": "Munchlax",
						"lvlRange": (9,10),
						"chance": .15
					},
					{
						"name": "Staraptor",
						"lvlRange": (9,10),
						"chance": .35
					},
					{
						"name": "Rapidash",
						"lvlRange": (10,10),
						"chance": .25
					},
					{
						"name": "Raichu",
						"lvlRange": (10,10),
						"chance": .25
					}
				],
				"travelKey": {
					"Corenes City": "Tapron Town",
					"Tapron Town": "Corenes City"
				}
			},
			"Corenes City": {
				"city": True,
				"gym": False,
				"pokecenter": True,
				"pokemart": True,
				"gymData": {
					"type": "Fighting",
					"trainers": [
						Trainer('Gym Rat Lawrence', [Pokemon('Machamp', 12)]),
						Trainer('Gym Rat Adam', [Pokemon('Machamp', 11), Pokemon('Riolu', 10)]),
						Trainer('Gym Leader Frank', [Pokemon('Machamp', 11), Pokemon('Lucario', 12)], gymLeader=True)
					],
					"leaderMessages": {
						"beforeBattle": [
							"I see...",
							"A new challenger has surpased my assistants.",
							"My Pokemon's type might be Normal...",
							"But their trainer is not!"
						],
						"afterBattle": [
							'Wow...',
							'You have exceeded my expectations.',
							'Here. Take this badge.',
							'Now you will be able to travel farther and face more challenges in your journey.',
							'I wish you good luck!'
						]
					}
				},
				"paths": [
					"Route 007",
					"Route 008",
					"Route 009",
					"Victory Road"
					]
			},
			"Route 009": {
				"gymBadgesRequired": 3,
				"city": False,
				"trainers": [
					Trainer('Farmer Julio', [Pokemon('Rapidash', 11), Pokemon('Luxray', 12)]),
					Trainer('Rock Climber Dave', [Pokemon('Machamp', 11), Pokemon('Staraptor', 12)]),
					Trainer('Rock Climber Barry', [Pokemon('Machamp', 12)])
				],
				"wild": [
					{
						"name": "Machamp",
						"lvlRange": (10,11),
						"chance": .33
					},
					{
						"name": "Luxray",
						"lvlRange": (10,11),
						"chance": .33
					},
					{
						"name": "Staraptor",
						"lvlRange": (10,11),
						"chance": .34
					}
				],
				"travelKey": {
					"Corenes City": "Orawell Town",
					"Orawell Town": "Corenes City"
				}
			},
			"Orawell Town": {
				"city": True,
				"gym": False,
				"pokecenter": True,
				"pokemart": True,
				"paths": [
					"Route 009",
					"Route 010"
					]
			},
			"Route 010": {
				"gymBadgesRequired": 3,
				"city": False,
				"trainers": [
					Trainer('Trainer Julio', [Pokemon('Gabite', 13)]),
					Trainer('Breeder James', [Pokemon('Lucario', 13)]),
					Trainer('Hiker Marlin', [Pokemon('Rapidash', 12), Pokemon('Weavile', 11)]),
				],
				"wild": [
					{
						"name": "Machamp",
						"lvlRange": (11,12),
						"chance": .30
					},
					{
						"name": "Raichu",
						"lvlRange": (11,12),
						"chance": .25
					},
					{
						"name": "Rapidash",
						"lvlRange": (11,12),
						"chance": .25
					},
					{
						"name": "Sneasel",
						"lvlRange": (10,11),
						"chance": .15
					}
				],
				"travelKey": {
					"Caubalt Summit": "Orawell Town",
					"Orawell Town": "Caubalt Summit"
				}
			},
			"Caubalt Summit": {
				"city": True,
				"gym": False,
				"pokecenter": False,
				"pokemart": False,
				"paths": [
					"Route 010"
					]
			},
			"Victory Road": {
				"gymBadgesRequired": 3,
				"city": False,
				"trainers": [
					Trainer('Veteran Ricky', [Pokemon('Staraptor', 13), Pokemon('Floatzel', 13)]),
					Trainer('Veteran Jimmy', [Pokemon('Gengar', 14)]),
					Trainer('Trainer Derek', [Pokemon('Rapidash', 15)]),
					Trainer('Swimmer Dustin', [Pokemon('Floatzel', 13), Pokemon('Empoleon', 13)]),
					Trainer('Businessman Jacob', [Pokemon('Snorlax', 14)])
				],
				"wild": [
					{
						"name": "Staraptor",
						"lvlRange": (11,13),
						"chance": .15
					},
					{
						"name": "Luxray",
						"lvlRange": (11,13),
						"chance": .15
					},
					{
						"name": "Machamp",
						"lvlRange": (11,13),
						"chance": .15
					},
					{
						"name": "Floatzel",
						"lvlRange": (11,13),
						"chance": .15
					},
					{
						"name": "Rapidash",
						"lvlRange": (11,13),
						"chance": .15
					},
					{
						"name": "Raichu",
						"lvlRange": (11,13),
						"chance": .15
					},
					{
						"name": "Gabite",
						"lvlRange": (11,13),
						"chance": .05
					},
					{
						"name": "Sneasel",
						"lvlRange": (11,13),
						"chance": .05
					},
				],
				"travelKey": {
					"Corenes City": "Pokemon League",
					"Pokemon League": "Corenes City"
				}
			},
			"Pokemon League": {
				"city": True,
				"gym": False,
				"pokecenter": True,
				"pokemart": True,
				"paths": [
					"Victory Road"
					]
			},
			"Seagrass Island": {
				"city": True,
				"gym": False,
				"pokecenter": False,
				"pokemart": False,
				"sailing": "Laupel City"
			}
		}
	}
else:
	with open('save_file.pkl', 'rb') as file:
		gameData = pickle.load(file)

def saveGame():
	input('Saving the game overwrites any previous save files.')
	choices = ['Yes', 'No']
	choiceIndex = userChoice(choices, 'Would you like to save the game?')
	if choices[choiceIndex] == 'Yes':
		with open('save_file.pkl', 'wb') as file:
			pickle.dump(gameData, file)
		print('Game Saved!')
		quit()

def blackout():
	print('Your Mom has picked you up from the closest town and brought you home to heal.')
	gameData['trainer'].location = 'Ecrin Town'
	gameData['trainer'].blackout = False

def wildEncounterChance(currRoute):
	if not randint(1,100) > gameData['wildEncounterChance']:
		#https://stackoverflow.com/a/41564971 random choice w/ probability
		choices = [p for p in currRoute['wild']]
		probability = [p['chance'] for p in currRoute['wild']]
		wildPokemonData = numpy.random.choice(choices, p=probability)
		name = wildPokemonData['name']
		lvlRangeMin = wildPokemonData['lvlRange'][0]
		lvlRangeMax = wildPokemonData['lvlRange'][1]
		wildPokemon = Pokemon(wildPokemonData['name'], level=randint(lvlRangeMin, lvlRangeMax))
		return TrainerBattle(gameData['trainer'], Trainer('Wild', [wildPokemon]))
	return None

def route(routeName):
	input('You are now on {}'.format(routeName))
	currRoute = gameData['locations'][routeName]
	# creates a list of Battles for the trainer to fight
	battles = []
	for t in currRoute['trainers']: # 
		battles.append(wildEncounterChance(currRoute))
		battles.append(TrainerBattle(gameData['trainer'], t))
		battles.append(wildEncounterChance(currRoute))

	for b in battles:
		if b != None:
			b.start()
			if gameData['trainer'].blackout == True:
				blackout()
				return
			# input('Press ENTER to continue on {}'.format(routeName))

	gameData['trainer'].location = gameData['locations'][routeName]['travelKey'][gameData['trainer'].location]
	input('You have arrived in {}'.format(gameData['trainer'].location))

	return

def travel():
	# curr location information
	currLocationName = gameData['trainer'].location
	currLocation = gameData['locations'][currLocationName]
	print('Current Location: {}'.format(currLocationName))

	# choose next location
	availablePaths = [l for l in currLocation['paths'] if gameData['locations'][l]['gymBadgesRequired'] <= len(gameData['trainer'].gymBadges)]
	availablePaths.append('Exit')
	pathIndex = userChoice(availablePaths, 'Where Will You Travel?')
	if availablePaths[pathIndex] == 'Exit':
		return
	else:
		routeName = currLocation['paths'][pathIndex]
		
		# fights trainers/wild pokemon on route and sets your location to the next city
		route(routeName)

def sail():
	currLocationName = gameData['trainer'].location
	currLocation = gameData['locations'][currLocationName]
	choices = [currLocation['sailing'], 'Exit']
	choiceIndex = userChoice(choices, 'Where would you like to sail?')
	choice = choices[choiceIndex]
	if choice == 'Exit':
		return
	else:
		input('You have set sail to {}!'.format(choice))
		input('The ocean is very beautiful.')
		input('You have arrived!')
		gameData['trainer'].location = choice

def talk():
	npcs = gameData['locations'][gameData['trainer'].location]['npcs']
	npcNames = []
	for npc in npcs:
		npcNames.append(npc['name'])
	npcNames.append('Exit')
	choiceIndex = userChoice(npcNames, 'Who would you like to talk to?')
	if npcNames[choiceIndex] == 'Exit':
		return
	else:
		for msg in npcs[choiceIndex]['messages']:
			input(msg)

def bag():

	input(gameData['trainer'].bag)

def pokedex():

	input(gameData['trainer'].pokedex)

def pokemon():
	print('Your Pokemon')
	for p in gameData['trainer'].pokemon:
		print(p)
	choices = ['Yes', 'No']
	choiceIndex = userChoice(choices, 'Would you like to change the party leader?')
	if choices[choiceIndex] == 'Yes':
		gameData['trainer'].changePartyLeader()

def pokeCenter():
	choices = ['Yes', 'No']
	choiceIndex = userChoice(choices, 'Would you like to heal your Pokemon?')
	choice = choices[choiceIndex]
	if choice == 'Yes':
		gameData['trainer'].heal()
		input('Your Pokemon have been healed!')
	else:
		input('Okay! See you again soon!')

def pokeMart():
	allItems = gameData['pokeMartItems']
	purchasableItems = []
	choices = []
	for item in allItems:
		if allItems[item]['gymBadgesRequired'] <= len(gameData['trainer'].gymBadges):
			purchasableItems.append(item)
			choices.append('{} | ${}'.format(item, allItems[item]['price']))
	choices.append('Exit')
	choiceIndex = userChoice(choices, 'What item would you like to purchase?')
	if choices[choiceIndex] == 'Exit':
		return
	else:
		itemName = purchasableItems[choiceIndex]
		item = allItems[itemName]
		quantityOptions = ['Exit']
		for i in range(1,10):
			quantityOptions.append('${}'.format((i * item['price']) ))
		quantity = userChoice(quantityOptions, "How many {}s would you like to buy?".format(itemName))
		if quantity == 0:
			return
		else:
			totalPrice = quantity * item['price']
			if gameData['trainer'].money >= totalPrice:
				input('You have purchased {}x {}'.format(quantity, itemName, totalPrice))
				gameData['trainer'].gainMoney(-1 * totalPrice)
				for i in range(quantity):
					gameData['trainer'].bag.addItem(itemName)
			else:
				input("You don't have enough money!")

	

	print('pokeMart')

def fightGym():
	currLocation = gameData['trainer'].location
	gymData = gameData['locations'][currLocation]['gymData']


	input('Welcome to the {} gym!'.format(currLocation))
	input('The pokemon here are {} type.'.format(gymData['type']))
	input('In order to obtain the gym bagde we have some rules you must follow')
	input('1. You must beat all gym trainers and the gym leader')
	input('2. You may only leave the gym to visit the nearest PokeCenter')
	gymLeaderBeaten = False
	while not gymLeaderBeaten:
		menuChoices = ['Visit PokeCenter', 'Pokemon', 'Me', 'Battle']
		choiceIndex = userChoice(menuChoices, "What's Next {}?".format(gameData['trainer'].name))
		answer = menuChoices[choiceIndex]
		if answer == 'Visit PokeCenter':
			pokeCenter()
		elif answer == 'Pokemon':
			pokemon()
		elif answer == 'Me':
			trainer()
		elif answer == 'Battle':
			for t in gymData['trainers']:
				if not t.defeated:
					currTrainer = t
					break
			if currTrainer.gymLeader:
				for msg in gymData['leaderMessages']['beforeBattle']:
					input('{}: {}'.format(currTrainer.name, msg))
			TrainerBattle(gameData['trainer'], currTrainer).start()
			if gameData['trainer'].blackout == True:
				blackout()
				return
			else:
				# the user won!
				if currTrainer.gymLeader:
					input('Congratulations! You have beaten {}'.format(currTrainer.name))
					if currTrainer.gymLeader:
						for msg in gymData['leaderMessages']['afterBattle']:
							input('{}: {}'.format(currTrainer.name, msg))
					input('{} has obtained the {} badge!'.format(gameData['trainer'].name, gymData['type']))
					gameData['trainer'].gymBadges.append(gymData['type'])
					gymLeaderBeaten = True
				else:
					input('Nice job! Keep going!')
			currTrainer.heal()

def map():

	print('map')

def trainer():

	input(gameData['trainer'])


def menu():
	print('Trainer {}\n{}'.format(gameData['trainer'].name, gameData['trainer'].location))
	menuChoices = ['Travel', 'Talk', 'Bag', 'Pokedex', 'Pokemon', 'Map','Me', 'Save']
	currLocation = gameData['locations'][gameData['trainer'].location]
	if currLocation['pokecenter']:
		menuChoices.append('Visit PokeCenter')
	if currLocation['pokemart']:
		menuChoices.append('Visit PokeMart')
	if currLocation['gym']:
		menuChoices.append('Fight Gym')
	if 'sailing' in currLocation and len(gameData['trainer'].gymBadges) >= 3:
		menuChoices.append('Sail')


	answerIndex = userChoice(menuChoices, "What's Next {}?".format(gameData['trainer'].name))
	answer = menuChoices[answerIndex]
	if answer == 'Travel':
		travel()
	elif answer == 'Talk':
		talk()
	elif answer == 'Bag':
		bag()
	elif answer == 'Pokedex':
		pokedex()
	elif answer == 'Pokemon':
		pokemon()
	elif answer == 'Visit PokeCenter':
		pokeCenter()
	elif answer == 'Visit PokeMart':
		pokeMart()
	elif answer == 'Fight Gym':
		fightGym()
	elif answer == 'Map':
		map()
	elif answer == 'Me':
		trainer()
	elif answer == 'Save':
		saveGame()
	elif answer == 'Sail':
		sail()


def preGame():
	print('enter name, choose pokemon, talk w/ professor, recieve poke balls, and pokedex')
	gameData['trainer'] = Trainer('Joey')
	gameData['trainer'].addPokemon(Pokemon('Chimchar', level=gameData['starterLevel']))
	for i in range(5):
		gameData['trainer'].bag.addItem('Poke Ball')
		gameData['trainer'].bag.addItem('Potion')

def main():
	if gameData['newGame']:
		preGame()
		gameData['newGame'] = False
	gameover = False
	while not gameover:
		menu()
main()
