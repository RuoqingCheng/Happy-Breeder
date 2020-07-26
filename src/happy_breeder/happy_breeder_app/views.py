from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.forms import UserCreationForm
# from django.utils.data import Q
from .forms import *
from django.urls import reverse_lazy
from django.views import generic
from .models import *
from django.utils import timezone

from datetime import datetime, timedelta
import time
import random
import operator

from django.contrib.auth.decorators import login_required

FUR_PRICE = 1
MATE_AGE = 1
MATE_INTERVAL = 1 #1s
FUR_AMOUNT = 3.3
AGE_AMOUNT = 0.2
REFRESH_INTERVAL = 30

def random_pos():
	x = random.randint(130, 660)
	y = random.randint(-70, 140)
	return x,y

def welcome(request):
	# if request.user.is_authenticated:
	# 	return redirect(breederhome)
	return render(request=request,
				  template_name='welcome.html')

def buy_item(request):
	# store:

	# front -> back:
	#     XML: {"request_store": "true"}

	# back -> front:
	#     json: {"item1ID": {"name": "", "img_url": "", "price": ""}, "item2ID": {"name": "", "img_url": "", "price": ""}}

	# front -> back:
	#     XML: {"request_purchase": "true", "itemID": "", "amount": ""}

	# back -> front:
	#     json: {"state": "success" or "fail", "user_fortune": "", "itemID": "", "amount": ""}
	if request.GET.get('request_purchase', None) == "true":
		item_id = int(request.GET.get('item_id'))
		item = Item.objects.get(id=item_id)
		amount = int(request.GET.get('amount'))
		price = amount * item.price

		if request.user.fortune < price:
			data = {
				'status': 'error'
			}

		else:
			if BreederItemThrough.objects.filter(breeder=request.user,item=item).exists():
				tochange = BreederItemThrough.objects.get(breeder=request.user,item=item)
				tochange.amount += amount
				tochange.save()
			else:
				tochange = BreederItemThrough.objects.create(breeder=request.user,
											  item=item, amount=amount)
				tochange.save()
			request.user.fortune -= price
			request.user.save()

			data = {
				'status': 'success',
				'id': tochange.id,
				'name': item.name,
				'img': str(item.picture),
				'qt': tochange.amount,
				'fortune': request.user.fortune,
			}

	return JsonResponse(data)

def change_pos(request):
	data={}
	if request.GET.get('request_change_pos', None) == "true":
		cat_id = request.GET.get('cat_id')
		cat = Pet.objects.get(id=cat_id)
		cat.pos_x = request.GET.get('x')
		cat.pos_y = request.GET.get('y')
		cat.save()
		data['status'] = 'success'
	return JsonResponse(data)

def ready_to_mate(age, last_mate_time, health, cleanness, food_level):
	message = ""
	if age < MATE_AGE:
		message = "The cat is at " + str(age) + " years old. Cat below age " + str(MATE_AGE) + " is not ready to mate!"
		return False, message
	if timezone.now().timestamp() - last_mate_time.timestamp() < MATE_INTERVAL:
		wait_time = (MATE_INTERVAL - (timezone.now().timestamp() - last_mate_time.timestamp())) / 1000;
		message = "The cat need to wait " + str(wait_time) + "s to get ready to mate!"
		return False, message

	if health < 80 or cleanness < 80 or food_level < 80:
		message = "All levels of the cat has to be above 80 to be ready to mate!"
		return False, message

	return True, message

# ruoqing, yinjie, jie
def action(request):
	data = {}
	if request.GET.get('request_action', None) == "true":
		action = request.GET.get('action')
		if (action == 'pat'):
			cat_id = request.GET.get('cat_id')
			cat = Pet.objects.get(id=cat_id)
			request.user.fortune += FUR_PRICE * cat.fur_amount; #fortune of one furball
			request.user.fortune = min(5000, request.user.fortune)
			cat.fur_amount = 0
			data['fur_amount'] = '0'
			data['user_fortune'] = str(request.user.fortune)
			cat.save()
			request.user.save()
			data['status'] = 'success'
		elif (action == 'scoop'):
			cat_id = request.GET.get('cat_id')
			cat = Pet.objects.get(id=cat_id)
			cat.cleanness = 100
			data['level_clean'] = str(cat.cleanness)
			cat.save()
			request.user.save()
			data['status'] = 'success'
		elif (action == 'sell'):
			cats = Pet.objects.filter(breeder = request.user)
			if len(cats) > 2:
				cat_id = request.GET.get('cat_id')
				cat = Pet.objects.get(id=cat_id)
				request.user.fortune += cat.price
				request.user.fortune = min(5000, request.user.fortune)
				cat.delete()
				request.user.save()
				data['status'] = 'success'
				data['sold'] = 'true'
				data['user_fortune'] = str(request.user.fortune)
		elif (action == 'mate'):
			can_mate = False
			cat_1 = Pet.objects.get(id=request.GET.get('cat_id'))
			cat_2 = Pet.objects.get(id=request.GET.get('cat_id2'))
			cat_1_can_mate, message = ready_to_mate(cat_1.age, cat_1.last_mate_time, cat_1.health, cat_1.cleanness, cat_1.food_level)
			cat_2_can_mate, message = ready_to_mate(cat_2.age, cat_2.last_mate_time, cat_2.health, cat_2.cleanness, cat_2.food_level)

			if cat_1_can_mate and cat_2_can_mate:
				now = timezone.now()
				now -= timedelta(microseconds = now.microsecond)
				now -= timedelta(seconds = 1)
				cat_1.last_mate_time = timezone.now()
				cat_2.last_mate_time = timezone.now()
				cat_1.save()
				cat_2.save()
				x, y = random_pos()
				pet = Pet.objects.create(breeder=request.user, pos_x=x, pos_y=y)
				pet.breed = mate_breed(cat_1.breed, cat_2.breed)
				pet.age = 0.0
				pet.price = get_price(pet.breed, pet.age)
				pet.last_refresh_time = now
				pet.clean_level, pet.health_level, pet.food_level = 100, 100, 100
				pet.fur_amount = 0.0
				pet.save()
				data["status"] = 'success'
				data["mate_status"] = 'success'
				data["cat_id"] = str(pet.id)
				data.update({"food_level": pet.food_level, "cleanness": pet.cleanness, "health": pet.health, "fur_amount": pet.fur_amount, "price": int(pet.price), "ready_to_mate": "false", "pos_x": pet.pos_x, "pos_y": pet.pos_y, "breed": pet.breed, "age": int(pet.age)})
			else:
				data["status"] = 'fail'
				data["mate_status"] = 'fail'
				data["message"] = message

		else:
			item = Item.objects.get(name=action)
			cat_id = request.GET.get('cat_id')
			cat = Pet.objects.get(id=cat_id)
			breeder_item = BreederItemThrough.objects.get(breeder=request.user, item = item)

			if item.info_type == 'food':
				if cat.food_level < 100:
					data['status'] = 'success'
					cat.food_level = min(item.info_level + cat.food_level, 100)
					data['level_food'] = str(cat.food_level)
				else:
					data['status'] = 'fail'
			if item.info_type == 'health':
				if cat.health < 100:
					data['status'] = 'success'
					cat.health = min(item.info_level + cat.health, 100)
					data['level_health'] = str(cat.health)
				else:
					data['status'] = 'fail'
			if item.info_type == 'clean':
				if cat.cleanness < 100:
					data['status'] = 'success'
					cat.cleanness = min(item.info_level + cat.cleanness, 100)
					data['level_clean'] = str(cat.cleanness)
				else:
					data['status'] = 'fail'

			if data['status'] == 'success':
				breeder_item.amount -= 1
				if breeder_item.amount == 0:
					data["delete_item"] = str(breeder_item.id)
					breeder_item.delete()
				else:
					breeder_item.save()
					data['item'] = action
					data['item_qt'] = breeder_item.amount

			cat.save()
			request.user.save()

	# print(data)
	return JsonResponse(data)


@login_required
def breederhome(request):
	if request.user.is_authenticated and request.user.first_login:
		now = timezone.now()
		now -= timedelta(microseconds = now.microsecond)
		now -= timedelta(seconds = 1)
		x, y = random_pos()
		pet = Pet.objects.create(gender=0,breeder=request.user, pos_x=x, pos_y=y)
		pet.breed = "L1R1B1W1S1"
		pet.price = get_price(pet.breed, pet.age)
		pet.last_refresh_time = now
		pet.clean_level, pet.health_level, pet.food_level = 100, 100, 100
		pet.fur_amount = 10.0
		pet.age = 0.0
		pet.save()
		x, y = random_pos()
		pet = Pet.objects.create(gender=1,breeder=request.user, pos_x=x, pos_y=y)
		pet.breed = "L1R1B2W1S2"
		pet.price = get_price(pet.breed, pet.age)
		pet.last_refresh_time = now
		pet.clean_level, pet.health_level, pet.food_level = 100, 100, 100
		pet.fur_amount = 10.0
		pet.age = 0.0
		pet.save()
		request.user.first_login = False
		request.user.save()

	warehouse_items = BreederItemThrough.objects.filter(breeder=request.user)
	min_next_refresh_time = timezone.now() + timedelta(seconds = REFRESH_INTERVAL)
	# print(timezone.now(), min_next_refresh_time)
	pets = Pet.objects.filter(breeder = request.user)

	if request.GET.get('request_refresh', None) == "true":
		return render(request=request,
					  template_name='breeder_home_yinjie.html',
					  context={"items": Item.objects.all(),
							   "warehouse_items": warehouse_items,
							   "cats": pets,
							   "next_request": min_next_refresh_time})

	for pet in pets:
		add_age, add_fur, amount, new_refresh_time, next_refresh_time = refresh(pet.last_refresh_time)
		print("*** \n\n\n update \n\n\n ***")
		print(amount, add_age, pet.last_refresh_time, new_refresh_time)
		min_next_refresh_time = min(min_next_refresh_time, next_refresh_time)
		pet.fur_amount = min(10, pet.fur_amount + add_fur)
		pet.age = min(10, pet.age + add_age)
		pet.food_level = max(0, pet.food_level - amount)
		pet.cleanness = max(0, pet.cleanness - amount)
		pet.health = max(0, pet.health - amount)
		pet.last_refresh_time = new_refresh_time
		pet.save()

	if request.user.is_authenticated:
		r = Record.objects.filter(host=request.user)
		ordered = sorted(r, key=operator.attrgetter('time'))
		ordered.reverse()

	return render(request=request,
				  template_name='breeder_home_yinjie.html',
				  context={"items": Item.objects.all(),
						   "warehouse_items": warehouse_items,
						   "cats": pets,
						   "next_request": min_next_refresh_time.timestamp(),
						   'vr': ordered})

def template(request):
	return render(request=request,
				  template_name='template.html')

class signup (generic.CreateView):
	form_class = BreederCreationForm
	success_url = reverse_lazy('login')
	template_name = 'registration/signup.html'


# jie ajax related function to visit other
def visitothers(request):
	# print("get visit ajax")
	if request.is_ajax():
		if request.GET.get('visit'):
			return JsonResponse({ 'success': True})


# jie get the furball from other's cats
def daodan(request):
	# print("is ajax?", request.is_ajax())
	# if request.is_ajax():
	# 	print("who owns the cats", request.GET.get('this_host'))
	# 	intercation = request.GET.get('visit_interaction')
	# 	print(request.GET)
	# 	if intercation == "pat":
	# 		cat_id = request.GET.get('cat_id')
	# 		cat = Pet.objects.get(id=cat_id)
	# 		host_id = int(request.GET.get('this_host'))
	# 		host = Breeder.objects.get(id=host_id)
	# 		host.fortune += 20
	# 		print("cat fur amount", cat.fur_amount)
	# 		if cat.fur_amount >= 1:
	# 			cat.fur_amount -= 1
	# 		else:
	# 			cat.fur_amout = 0
	# 		cat.save()
	# 		print("cat fur amount after", cat.fur_amount)
	# 		request.user.save()
	# 		data = {'status': 'success'}
	# 		return JsonResponse(data)

	data = {}
	if request.GET.get('request_action', None) == "true":
		action = request.GET.get('action')
		if (action == 'daodan'):
			# get the furball from the visitor' cats
			host_id = int(request.GET.get('host_id'))
			host = Breeder.objects.get(id=host_id)
			cat_id = request.GET.get('cat_id')
			cat = Pet.objects.get(id=cat_id)
			get_amount = cat.fur_amount
			if get_amount >= 1:
				cat.fur_amount -= 1
				cat.save()
				request.user.fortune += FUR_PRICE * 1; #fortune of one furball
				request.user.fortune = min(5000, request.user.fortune)
				request.user.save()
			# add how many furball the visitor get in this visiting
				rs = Record.objects.filter(host=host, guest=request.user)
				ordered_rs = sorted(rs, key=operator.attrgetter('time'))
				most_recent_record = ordered_rs[-1]
				most_recent_record.get_furball_amount += 1
				most_recent_record.save()

			data['fur_amount'] = cat.fur_amount
			data['user_fortune'] = str(request.user.fortune)
			data['status'] = 'success'
	return JsonResponse(data)

# jie visit other's homepage
def seeothers(request):
	if request.method == "POST" and request.user.is_authenticated:
		context = {}
		# get the random id to visit
		myId = request.user.id
		breeders = Breeder.objects.all()
		all_ids = []
		all_username = []
		for breeder in breeders:
			all_ids.append(breeder.id)
			all_username.append(breeder.username)
		while True:
			randomIndex = random.randint(0, len(all_ids) - 1)
			randomId = all_ids[randomIndex]
			randomUser = Breeder.objects.get(id=randomId)
			if randomId != myId and randomUser.username != "admin":
				break
		host = Breeder.objects.get(id=randomId)
		# print("go to", randomId)
		# print("go to", host.nickname)

		# create visiting record
		all_records = Record.objects.filter(host=host)
		if all_records.count() >= 10:
			minimum = timezone.now()
			mini_id = -1
			for record in all_records:
				# print(minimum, record.time)
				if record.time < minimum:
					minimum = record.time
					mini_id = record.id
			if mini_id != -1:
				record_to_del = Record.objects.get(id=mini_id)
				host_to_del = record_to_del.host
				guest_to_del = record_to_del.guest
				host_to_del.visitors.remove(guest_to_del)
		r = Record(host=host, guest=request.user, time=timezone.now())
		r.save()

		# print("___history___")
		# print(r.host)
		# print(r.guest)
		# print(host.visitors)
		# r2 = Record.objects.filter(host=host)
		# for item in r2:
		# 	print("sooo")
		# 	print(item.time)
		# 	print(item.host)
		# 	print(item.guest)

		context["host_id"] = randomId
		context["host_nickname"] = host.nickname
		context["cats"] = Pet.objects.filter(breeder=host)
		context["warehouse_items"] = BreederItemThrough.objects.filter(breeder=host)
		return render(request, "visit_others.html", context)


# def interact(request):
	# interact:

	# front -> back:
	#     XML: {"request_action": "true", "action": "itemID" or "brush" or "scoop", "cat_ID": ""}

	# back -> front:
	#     json: {"state": "success" or "fail", "user_exp": "", "user_fortune": "", "item_ID": "None" or "", "amount": "None" or "", "cat_ID": "", "food_level": "", "clean_level": "", "health_level": ""}

	# if request.isAjax() and request.POST:
	#     if "request_action" in request.POST:
			# "brush"
			# "scoop"
			# "itemID" "info_type food health clean" -1 if 0 do nothing

	# bit = BreederItemThrough.objects.filter(Q(breeder = breeder) & Q(item = item))

def refresh(refresh_time):
	# this function is to calculate refresh time and level decreasing
	now = timezone.now()
	now -= timedelta(microseconds = now.microsecond)
	print(now)
	print(refresh_time)
	s = (now - refresh_time).seconds
	print(s)
	if s > REFRESH_INTERVAL:
		remainder = s % REFRESH_INTERVAL
		print(remainder)
		amount = (s - remainder + 1) // REFRESH_INTERVAL
		print(amount)
		add_age = amount * AGE_AMOUNT
		add_fur = amount * FUR_AMOUNT
		new_refresh_time = now - timedelta(seconds = remainder)
		next_refresh_time = new_refresh_time + timedelta(seconds = REFRESH_INTERVAL)
		return add_age, add_fur, amount, new_refresh_time, next_refresh_time
	else:
		next_refresh_time = refresh_time + timedelta(seconds = REFRESH_INTERVAL)
		return 0, 0, 0, refresh_time, next_refresh_time

def auto_update(request):
	# for auto-update

	# front -> back:
	#     XML: {"request_refresh": "true"}

	# back -> front:
	#     json: {"state": "success" or "fail", "catID": {"food_level": "", "clean_level": "", "health_level": ""}, "catID": {"food_level": "", "clean_level": "", "health_level": ""}, "next_request": ""}
	pets = Pet.objects.filter(breeder = request.user)
	context = {}
	min_next_refresh_time = timezone.now() + timedelta(seconds = REFRESH_INTERVAL)
	for pet in pets:
		add_age, add_fur, amount, new_refresh_time, next_refresh_time = refresh(pet.last_refresh_time)
		min_next_refresh_time = min(min_next_refresh_time, next_refresh_time)
		# print(add_fur)
		print(add_age,add_fur)
		pet.fur_amount = min(10, pet.fur_amount + add_fur)
		# print("fur amount: ", pet.fur_amount)
		# print(pet.food_level, amount)
		pet.age = min(10, pet.age + add_age)
		pet.food_level = max(0, pet.food_level - amount)
		pet.cleanness = max(0, pet.cleanness - amount)
		pet.health = max(0, pet.health - amount)
		pet.last_refresh_time = new_refresh_time
		pet.price = get_price(pet.breed, pet.age)
		pet.save()
		ready, _ = ready_to_mate(pet.age, pet.last_mate_time, pet.health, pet.cleanness, pet.food_level)
		if ready:
			ready = 'true'
		else:
			ready = 'false'
		context[str(pet.id)] = {"food_level": pet.food_level, "cleanness": pet.cleanness, "health": pet.health, "fur_amount": int(pet.fur_amount), "price": pet.price, "ready_to_mate": ready, "age": int(pet.age)}
	context["state"] = "success"
	#context["next_request"] = min_next_refresh_time
	#print (min_next_refresh_time.timestamp())
	context["next_request"] = min_next_refresh_time.timestamp()
	# print(context)
	return JsonResponse(context)

def get_child_type(t1, t2, choice, rate):
	choice = set(choice)
	if t1 in choice:
		choice.remove(t1)
	if t2 in choice:
		choice.remove(t2)
	choice = list(choice)
	# print(choice)
	r = random.random()
	if r < rate:
		return t1
	elif r < 2 * rate:
		return t2
	else:
		u = random.randint(0, len(choice) - 1)
		return choice[u]

def mate_breed(breed1, breed2):
	w1 = int(breed1[7])
	w2 = int(breed2[7])
	if w1 == 4 or w2 == 4:
		rate = 0.2
	elif w1 == 3 or w2 == 3:
		rate = 0.3
	elif w1 == 2 or w2 == 2:
		rate = 0.4
	else:
		rate = 0.5
	new_breed = "L"
	new_breed += get_child_type(breed1[1], breed2[1], ["1", "2", "3", "4", "5"], rate)
	new_breed += "R"
	new_breed += get_child_type(breed1[3], breed2[3], ["1", "2", "3", "4", "5"], rate)
	new_breed += "B"
	new_breed += get_child_type(breed1[5], breed2[5], ["1", "2", "3", "4", "5"], rate)
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
	new_breed += get_child_type(breed1[9], breed2[9], ["1", "2", "3", "4", "5"], rate)
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
	if age < 1:
		price *= 0.1
	elif age > 5 and age < 8:
		price *= 0.5
	elif age > 8:
		price *= 0.2
	return price
