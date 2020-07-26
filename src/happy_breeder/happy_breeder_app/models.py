from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone

class Breeder(AbstractUser):
	nickname=models.CharField(max_length=50)
	fortune = models.IntegerField(default=100)
	experience = models.IntegerField(default=0)
	house_level_choice = (
		(0, "start house"),
		(1, "advanced house"),
		(2, "super house"),
		(3, "noble house"),
		(4, "royal house"),
		)
	house_level = models.IntegerField(default=0, choices=house_level_choice)
	litter_level = models.IntegerField(default=0)
	first_login = models.BooleanField(default=True)
	visitors = models.ManyToManyField("self", blank=True, symmetrical=False, through='Record')

	def __str__(self):
		return self.username

class Record(models.Model):
	host = models.ForeignKey(Breeder, related_name='visit_host', on_delete=models.CASCADE)
	guest = models.ForeignKey(Breeder, related_name='visit_guest', on_delete=models.CASCADE)
	time = models.DateTimeField()
	get_furball_amount = models.IntegerField(default=0)


ITEM_TYPE = [
	('food', 'food'),
	('clean', 'clean'),
	('health', 'health'),
]
class Item(models.Model):
  name = models.CharField(max_length=120,unique=True)
  price = models.IntegerField(default=0)
  info_type = models.CharField(max_length=50, choices=ITEM_TYPE, default='food')
  info_level = models.IntegerField(default=0)
  picture = models.ImageField(upload_to='store_imgs/',default ='store_imgs/milk.png')
  breeder = models.ManyToManyField(Breeder, through = 'BreederItemThrough')

  def __str__(self):
	  return self.name


class BreederItemThrough(models.Model):
	breeder = models.ForeignKey(Breeder, on_delete=models.CASCADE)
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	amount = models.IntegerField(default = 0)

# Create your models here.
def validate_color(value):
	if len(value) != 7 or value[0] != "#":
		raise ValidationError('%s is not an valid color' % value)
	for i in range(1, len(value)):
		if (ord(value[i]) >= 48 and ord(value[i]) <= 57):
			pass
		elif (ord(value[i]) >= 65 and ord(value[i]) <= 70):
			pass
		elif (ord(value[i]) >= 97 and ord(value[i]) <= 102):
			pass
		else:
			raise ValidationError('%s is not a valid color' % value)

def validate_age(value):
	if value < 0 or value >= 20:
		raise ValidationError('%s is not a valid age' % value)

def validate_with_in_100(value):
	if value < 0 or value > 100:
		raise ValidationError('%s is not a valid value' % value)

def validate_with_in_5(value):
	if value < 0 or value > 5:
		raise ValidationError('%s is not a valid value' % value)

def validate_with_in_10(value):
	if value < 0 or value > 10:
		raise ValidationError('%s is not a valid value' % value)

# class Breed(models.Model):
# 	eye_color_choice = models.CharField(max_length = 50, validators = [validate_color])
# 	fur_color_1 = models.CharField(max_length = 50, validators = [validate_color])
# 	fur_color_2 = models.CharField(max_length = 50, validators = [validate_color])
# 	pattern_choice = (
# 		(0, "pure"),
# 		(1, "mix"),
# 		)
# 	pattern = models.IntegerField(choices = pattern_choice)

class Pet(models.Model):
	breeder = models.ForeignKey(Breeder, on_delete=models.CASCADE)
	age = models.FloatField(default=0.0, validators = [validate_age])
	fur_amount = models.FloatField(default=10.0, validators = [validate_with_in_10])
	gender_choice = (
		(0, "male"),
		(1, "female"),
		)
	gender = models.IntegerField(default=0, choices = gender_choice)
	health = models.IntegerField(default=100, validators = [validate_with_in_100])
	cleanness = models.IntegerField(default=100, validators = [validate_with_in_100])
	food_level = models.IntegerField(default=100, validators = [validate_with_in_100])
	# last_mate_time = models.TimeField()
	last_refresh_time = models.DateTimeField(default=timezone.now())
	breed = models.CharField(default = "L1R1B1W1S1", max_length = 10)
	pos_x = models.IntegerField(default=0)
	pos_y = models.IntegerField(default=0)
	price = models.IntegerField(default=50)
	last_mate_time = models.DateTimeField(default=timezone.now())
	img = models.ImageField(upload_to='cats/', max_length=5000, default='oreo.png')

# class Message(models.Model):
# 	pet = models.OneToOneField(Pet, on_delete=models.CASCADE)
# 	breeder = models.OneToOneField(Breeder, on_delete=models.CASCADE)
# 	content = models.TextField()
