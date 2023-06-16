from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from django.shortcuts import reverse
from django.core.exceptions import ValidationError
from datetime import date, datetime


User = get_user_model()

def validate_date(value):
	current_date = date.today()
	start_date = value
	if start_date < current_date:
		raise ValidationError("Дата начала не может быть в прошлом.")

def validate_start_date(value):
	if value < timezone.now():
		raise ValidationError("Дата начала не может быть в прошлом.")


class Selection(models.Model):
	name = models.CharField(max_length=20)
	price = models.DecimalField(max_digits=7, decimal_places=2)

	def __str__(self):
		return self.name

	class Meta:
		db_table  = "Selection"
		verbose_name_plural = 'Selections'


class Activity(models.Model):
	name = models.CharField(max_length=20)

	def __str__(self):
		return self.name

	class Meta:
		db_table  = "Activity"
		verbose_name_plural = 'Activities'

class Day(models.Model):
	activity = models.ManyToManyField(Activity)
	name = models.CharField(max_length=10)
	description = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.name

	class Meta:
		db_table  = "Day"
		verbose_name_plural = 'Day'

class TourPackageInclusion(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

	class Meta:
		db_table  = "TourPackageInclusion"
		verbose_name_plural = 'Tour Package Inclusions'

class TourPackageExclusion(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

	class Meta:
		db_table  = "TourPackageExclusion"
		verbose_name_plural = 'Tour Package Exclusions'

class TourAvailableDates(models.Model):
	available_date = models.DateField(validators=[validate_date])

	def __str__(self):
		return str(self.available_date)

	class Meta:
		db_table  = "TourAvailableDates"
		verbose_name_plural = 'Tour Available Dates'

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	age = models.IntegerField(validators=[MinValueValidator(0)])
	sex = models.CharField(max_length=10)
	passport_no = models.CharField(max_length=20)
	nationality = models.CharField(max_length=100)
	phone = models.CharField(max_length=20)
	image = models.ImageField( upload_to="UserProfile", default="default_user.png")

	@property
	def imageURL(self):
		try:
			image = self.image.url
		except:
			image = ''
		return image

	def __str__(self):
		return self.user.username

	class Meta:
		db_table  = "UserProfile"

class TravelInfo(models.Model):
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	age = models.IntegerField(validators=[MinValueValidator(0)])
	sex = models.CharField(max_length=10)
	passport_no = models.CharField(max_length=20)
	nationality = models.CharField(max_length=100)
	phone = models.CharField(max_length=20)

	def __str__(self):
		return self.passport_no

	class Meta:
		db_table  = "TravelInfo"

class TourPackage(models.Model):
	name = models.CharField(max_length=50)
	total_price = models.DecimalField(max_digits=7, decimal_places=2)
	discount_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	starting_point = models.CharField(max_length=20)
	selections = models.ManyToManyField(Selection)
	activities = models.ManyToManyField(Activity)
	days =models.ManyToManyField(Day)
	city = models.CharField(max_length=50)
	country = models.CharField(max_length=50)
	age = models.IntegerField(validators=[MinValueValidator(0)])
	tour_package_inclusion = models.ManyToManyField(TourPackageInclusion)
	tour_package_exclusion = models.ManyToManyField(TourPackageExclusion)
	full = models.BooleanField(default=False)
	tour_dates = models.ManyToManyField(TourAvailableDates)
	slug = models.SlugField()

	def __str__(self):
		return self.name

	def get_average_rating(self):
		average_rating = Review.objects.filter(tour=self).aggregate(Avg('rating'))['rating__avg']
		return int(average_rating)

	def get_count_rating(self):
		rating_count = Review.objects.filter(tour=self).count()
		return rating_count

	def get_num_days(self):
		return self.days.count()

	def get_absolute_url(self):
		return reverse('tourDetails',kwargs={
		'slug':self.slug
		})

	def get_total_price(self):
		if self.discount_price:
			return self.discount_price
		return self.total_price

	def get_discount(self):
		if self.discount_price and self.total_price:
			discount_percentage = (self.discount_price / self.total_price) * 100
			return 100 - int(discount_percentage)
		return 0
	# companions = models.ManyToManyField(TravelInfo)
class Booking(models.Model):

	STATUS_CHOICES = (
		('pending','Pending'),
		('approved', 'Approved'),
		('cancelled', 'Cancelled'),
	)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	tour = models.ForeignKey(TourPackage, on_delete=models.CASCADE)
	ordered_date = models.DateTimeField(blank=True, null=True)
	num_of_people = models.IntegerField()
	ref_code = models.CharField(max_length=10)
	status = models.CharField(max_length=100, choices=STATUS_CHOICES)
	dates = models.ManyToManyField(TourAvailableDates)
	selections = models.ManyToManyField(Selection)
	companions = models.ManyToManyField(TravelInfo)
	grand_total = models.DecimalField(max_digits=7, decimal_places=2)

	paid = models.BooleanField(default=False)

	def __str__(self):
		return self.tour.name

	class Meta:
		db_table  = "Booking"
		verbose_name_plural = 'Bookings'

class TourPackageImage(models.Model):
	tour = models.ForeignKey(TourPackage, on_delete=models.CASCADE)
	image = models.ImageField(null=True, blank=True)

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

	def __str__(self):
		return self.tour.name

	class Meta:
		db_table  = "TourPackageImage"
		verbose_name_plural = 'Tour Package Images'


class Review(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	tour = models.ForeignKey(TourPackage, on_delete=models.CASCADE)
	comment = models.TextField(max_length=500)
	rating = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.tour.name

	class Meta:
		db_table  = "Review"
		verbose_name_plural = 'Reviews'


class Contact(models.Model):
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	phone = models.CharField(max_length=20)
	message = models.TextField()
	email = models.CharField(max_length=100)
	read = models.BooleanField(default=False)

	def __str__(self):
		return self.first_name + " " + self.last_name

	class Meta:
		db_table  = "Contact"

