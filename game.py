from classes import *
from time import sleep

gameData = {
	"trainer": Trainer(''),
	"starters": [ ['Turtwig', 'Grass'], ['Chimchar', 'Fire'], ['Piplup', 'Water']],
	"opponents": [
		Trainer('Trainer Jenny', [Pokemon('Turtwig', 1)]),
		Trainer('Trainer Bob', [Pokemon('Piplup', 4), Pokemon('Pikachu', 3)])
	]
}


def displayMessages(messages):
	for message in messages:
		input(message)

def chooseStarter():
	i = 0
	for starter in gameData['starters']:
		print('{:3} | {:8} | {:8}'.format(i, starter[0], starter[1]))
		i += 1
	validStarterOption = False
	while not validStarterOption:
		starterIndex = input('Which Pokemon do you choose? >>> ')
		try:
			starterIndex = int(starterIndex)
		except ValueError:
			print('Must be a number!')
			continue
		if starterIndex not in range(i):
			print('Must be a valid option!')
			continue
		validStarterOption = True
	choice = Pokemon(gameData['starters'][starterIndex][0])
	gameData['trainer'].addPokemon(choice)

def newGameIntro():
	gameplayText = [
		'All new trainers start somewhere.',
		'My name is Professor Rowan and I study Pokemon!',
		'It comes to my attention that you want to follow my path.',
		'I definitely will be able to help you with that!',
		'Before we get into the details, introduce yourself.'
		]
	displayMessages(gameplayText)

	trainerName = input('What is your name? >>> ')
	gameData['trainer'] = Trainer(trainerName)

	gameplayText = [
		'Nice to meet you {}.'.format(gameData['trainer'].name),
		'I hope that this Journey will teach you much about Pokemon and the world around you.',
		'To prepare you for your journey we will share a special moment together.',
		'Choosing your first Pokemon!',
		]
	displayMessages(gameplayText)
	chooseStarter()

	gameplayText = [
		'Ahh so you chose {}!'.format(gameData['trainer'].pokemon[0].name),
		'What a great choice.',
		'Now... Before I send you off on to your journey...',
		'I want you to have this.',
		'{} obtained the Pokedex'.format(gameData['trainer'].name),
		'The Pokedex is a high tech machine that will track how many Pokemon you have encountered.',
		'Come back to me when you have filled it up!',
		'Now is the time {}.'.format(gameData['trainer'].name),
		'Enjoy your adventure. It starts now.'
		]
	displayMessages(gameplayText)


def battleTrainers():
	for t in gameData['opponents']:
		TrainerBattle(gameData['trainer'], t).start()


def main():
	newGameIntro()
	battleTrainers()



main()