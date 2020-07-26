import random

def get_child_type(t1, t2, choice):
	choice = set(choice)
	if t1 in choice:
		choice.remove(t1)
	if t2 in choice:
		choice.remove(t2)
	choice = list(choice)
	r = random.random()
	if r < 0.45:
		return t1
	elif r < 0.9:
		return t2
	else:
		u = random.randint(0, len(choice) - 1)
		return choice[u]

def mate_breed(breed1, breed2):
	new_breed = "L"
	new_breed += get_child_type(breed1[1], breed2[1], ["1", "2", "3", "4", "5"])
	new_breed += "R"
	new_breed += get_child_type(breed1[3], breed2[3], ["1", "2", "3", "4", "5"])
	new_breed += "B"
	new_breed += get_child_type(breed1[5], breed2[5], ["1", "2", "3", "4", "5"])
	new_breed += "W"
	r = random.random()
	if r < 0.005:
		new_breed += "4"
	elif r < 0.05:
		new_breed += "3"
	elif r < 0.2:
		new_breed += "2"
	else:
		new_breed += "1"
	new_breed += "S"
	new_breed += get_child_type(breed1[9], breed2[9], ["1", "2", "3", "4", "5"])
	return new_breed

def get_price(breed, age):
	price = 1
	l = int(breed[1])
	r = int(breed[3])
	b = int(breed[5])
	w = int(breed[7])
	s = int(breed[9])
	if l == r and r == b:
		price = 200
	else:
		if b < 3:
			price = 25
		elif b == 3:
			price = 50
		elif b == 4:
			price = 60
		elif b == 5:
			price = 100
		if l != r:
			price *= 2
	if b == s:
		price += 200
	if w == 1:
		price += 25
	elif w == 2:
		price += 100
	elif w == 3:
		price += 300
	elif w == 4:
		price += 600
	if age < 2:
		price *= 0.5
	elif age > 5 and age < 8:
		price *= 0.5
	elif age > 8:
		price *= 0.1
	return price