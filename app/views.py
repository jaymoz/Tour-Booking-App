from django.shortcuts import render,redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import *
import random,string
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
import json
from datetime import timedelta
from django.utils import timezone
from django.forms import formset_factory


def create_ref_code():
	return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))


def calculate_tour_duration(tour_package):
	duration_dict = {}
	tour_dates = tour_package.tour_dates.all()
	days_count = tour_package.days.count()

	for tour_date in tour_dates:
		tour_duration = tour_date.available_date + timedelta(days=days_count)
		duration_dict[tour_date.available_date] = tour_duration

	return duration_dict

def check_user_review(user, tour):
	reviews = Review.objects.filter(user=user, tour=tour)
	if reviews.exists():
		return True
	return False

def checkUserProfile(user):
	prof = UserProfile.objects.filter(user=user)
	if prof.exists():
		return True
	return False

def home(request):
	return render(request, "app/home-page--fsv.html")


def registerUser(request):
	if request.user.is_authenticated:
		return redirect('home')

	user_form = RegisterUserForm()
	if request.method == "POST":
		print("THIS IS A POST REQUEST")
		user_form = RegisterUserForm(request.POST)
		if user_form.is_valid():
			email = user_form.cleaned_data['email']
			if User.objects.filter(email=email).exists():
				messages.error(request, "Электронная почта уже существует. Пожалуйста, используйте другой адрес электронной почты.")
				return redirect("register")
			try:
				user_form.save()
				messages.success(request, "Ваша учетная запись была успешно создана")
				return redirect("login")
			except Exception as e:
				messages.error(request, str(type(e)))
				return redirect("register")
		else:
			messages.warning(request, user_form.errors)

	context = {'user_form': user_form}
	return render(request, 'app/register.html', context)

@login_required(login_url="/login")
def Logout(request):
	logout(request)
	messages.success(request, "Мы надеемся увидеть вас в ближайшее время")
	return redirect("home")

def loginUser(request):
	if request.user.is_authenticated:
		return redirect('home')
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "Добро пожаловать " + user.username)
			return redirect("home")
		else:
			messages.info(request, "Предоставлены недействительные данные")
			return redirect("login")
	context = {}
	return render(request,'app/login.html',context)

def tours(request):
	tour_list = TourPackage.objects.all()
	context = {"tours":tour_list}
	return render(request, "app/tour.html", context)


def tourDetail(request, slug):
	user_profile = UserProfile.objects.filter(user=request.user)
	if not user_profile.exists():
		messages.warning(request, "Please create a profile to book tour packages")
	tour = get_object_or_404(TourPackage, slug=slug)
	reviews = Review.objects.all()
	user_has_profile = checkUserProfile(request.user)
	context = {"tour":tour, "reviews":reviews, "user_has_profile":user_has_profile}
	existing_order = False

	if Booking.objects.filter(user=request.user, tour=tour, paid=False).exists():
		existing_order = True
		context.update({"existing_order":existing_order})
	if request.user.is_authenticated:
		user_review = check_user_review(request.user, tour)
		context.update({"user_review":user_review})

	return render(request, "app/tour-detail.html", context)

def drop_review(request, slug):
	tour = get_object_or_404(TourPackage, slug=slug)
	return render(request, "app/add-review.html")

def checkout(request, slug):
	tour = get_object_or_404(TourPackage, slug=slug)

	if request.method == "POST":
		available_dates = request.POST.getlist('available_dates')
		number_of_people = request.POST.get('num_of_people')
		selections = request.POST.getlist('selections')

		existing_order = Booking.objects.filter(user=request.user, tour=tour, paid=False).exists()

		if existing_order:
			messages.warning(request, "You already have an existing order.")
			return redirect('payment')

		if len(available_dates) > 0 and number_of_people and int(number_of_people) > 0:
			booking = Booking(
				user=request.user,
				tour=tour,
				num_of_people=number_of_people,
				status='pending',
				grand_total=tour.get_total_price(),
				paid=False
			)
			booking.save()

			for date in available_dates:
				date_mod = get_object_or_404(TourAvailableDates, available_date=date)
				booking.dates.add(date_mod)

			for sel in selections:
				sel_mod = get_object_or_404(Selection, name=sel)
				booking.selections.add(sel_mod)
				booking.grand_total += sel_mod.price

			booking.grand_total *= len(available_dates)
			booking.grand_total *= int(number_of_people)
			booking.save()
			if number_of_people and int(number_of_people) > 1:
				required_num = int(number_of_people) - 1
				return redirect("process-travel-info",id=booking.id, num=required_num)
			return redirect("payment", slug=booking.tour.slug)
		else:
			messages.warning(request, "Please pick at least one date or The number of people cannot be zero!!")

	context = {"tour": tour}
	return render(request, "app/checkout-page.html", context)

def deleteBooking(request, id):
	booking = get_object_or_404(Booking, id=id)
	booking.delete()
	messages.success(request, "Booking deleted successfully")
	return redirect('tours')

def payment(request, slug):
	booking = Booking.objects.filter(user=request.user, paid=False, tour__slug = slug)
	context = {"booking":booking[0]}
	return render(request, "app/payment.html", context)

@login_required(login_url="/login")
def payment_completed(request):
	if request.method == 'POST':
		body = json.loads(request.body)
		booking = get_object_or_404(Booking, id=body["bookingID"])
		status = body["status"]
		if status.lower() == "completed":
			booking.ordered_date = timezone.now()
			booking.ref_code = create_ref_code()
			booking.status = "pending"
			booking.paid = True
			booking.save()
			# Redirect to the payment completed page
			return redirect('payment-successful')
		else:
			# Redirect to the payment not complete page
			return redirect('payment-failed')
	else:
		# Return a bad request response if the request is not a POST request
		return HttpResponseBadRequest()

@login_required(login_url="/login")
def payment_successful(request):
	return render(request, "app/payment-successful.html")

@login_required(login_url="/login")
def payment_unsuccessful(request):
	return render(request, "app/payment-unsuccessful.html")

@login_required(login_url="/login")
def dashboard(request):
	bookings = Booking.objects.filter(user=request.user, paid=True).order_by('-ordered_date')
	context = {"bookings":bookings}
	return render(request, "app/dashboard.html", context)

def contact(request):

	if request.method == "POST":
		first_name = request.POST.get("first_name")
		last_name = request.POST.get("last_name")
		phone = request.POST.get("phone")
		message = request.POST.get("message")
		email = request.POST.get("email")

		user_contact = Contact.objects.create(
			first_name = first_name,
			last_name = last_name,
			phone = phone,
			message = message,
			email = email
		)
		messages.success(request, "Your request has been received! We will contact you shortly")
	return render(request, "app/contact.html")

def gallery(request):
	gallery = TourPackageImage.objects.all()
	context = {"gallery":gallery}
	return render(request, "app/gallery.html", context)

def bookingDetail(request, id):
	booking = get_object_or_404(Booking, id=id)
	durations = calculate_tour_duration(booking.tour)
	# for tour_date, duration in durations.items():
	# 	print(f"Tour Date: {tour_date}, Duration: {duration}")
	context = {"booking": booking, "durations" : durations}
	return render(request, "app/booking-detail.html", context)


def processTravelInfo(request, id, num):
	TravelInfoFormSet = formset_factory(TravelInfoForm, extra=num)
	booking = get_object_or_404(Booking, id=id)
	if request.method == 'POST':
		formset = TravelInfoFormSet(request.POST)
		if formset.is_valid():
			for form in formset:
				# Process each form in the formset and access its cleaned data
				first_name = form.cleaned_data.get('first_name')
				last_name = form.cleaned_data.get('last_name')
				phone = form.cleaned_data.get('phone')
				age = form.cleaned_data.get('age')
				passport_no = form.cleaned_data.get('passport_no')
				nationality = form.cleaned_data.get('nationality')
				sex = form.cleaned_data.get('sex')
				travel_info = TravelInfo.objects.create(
					first_name=first_name,
					last_name=last_name,
					phone=phone,
					age=age,
					passport_no=passport_no,
					nationality=nationality,
					sex=sex,
				)
				booking.companions.add(travel_info)
				booking.save()
			messages.success(request, "Wee have received the data. Thank you!") # Redirect to a success page or any other desired action
			return redirect("payment", slug=booking.tour.slug)
		else:
			messages.warning(request, formset.errors)
	else:
		formset = TravelInfoFormSet()

	context = {'formset': formset}
	return render(request, 'app/travel-info.html', context)
