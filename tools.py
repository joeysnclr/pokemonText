def userChoice(choices, prompt):
	valid = False
	validAnswers = [i for i in range(len(choices))]
	while not valid:
		for i in range(len(choices)):
			print('{} | {}'.format(i, choices[i]))
		answer = input("{} >> ".format(prompt))

		# checks if it is an int
		try:
			answer = int(answer)
		except ValueError:
			print('Please enter a valid option.')
			continue

		# checks if it is a valid answer
		if answer not in validAnswers:
			print('Please enter a valid option.')
			continue
		valid = True
		return answer
	