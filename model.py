
def menuAction():
	print('1 | View Pokedex')
	print('2 | View Bag')
	print('3 | View Pokemon')
	print('4 | Travel Somewhere')
	print('5 | Save & Exit')
	action = int(input('What do u want to do? >> '))
	if action == 1:
		viewPokedex()
	elif action == 2:
		viewBag()
	elif action == 3:
		viewPokemon()
	elif action == 4:
		travel()

def viewPokedex():
	print('You have seen 17 out of 210 Pokemon')

def viewBag():
	print('Items')
	print('\tMap')
	print('Poke Balls')
	print('\t4 x Great Ball')

def viewPokemon():
	print('Chimchar | Lvl 5 | HP 19/19')

def travel():
	print('List of places to travel')


def adventure():
	print('Welcome to *insert creative pokemon text based game name here*!')
	gameover = False
	while not gameover:
		menuAction()
adventure()