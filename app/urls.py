from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginUser, name="login"),
    path("logout/", views.Logout, name="logout"),
    path('register/', views.registerUser, name="register"),
    path("tours/", views.tours, name="tours"),
    path("tour-detail/<slug>/", views.tourDetail, name="tourDetails"),
    path("drop-a-review/<slug>/", views.drop_review, name="drop-review"),
    path("checkout/<slug>/", views.checkout, name="checkout"),
    path("payment/<slug>/", views.payment, name="payment"),
    path("delete/<int:id>", views.deleteBooking, name="delete"),
    path('payment-completed/', views.payment_completed, name='payment-completed'),
    path('payment-successful/', views.payment_successful, name="payment-successful"),
    path('paypal-failed/', views.payment_unsuccessful, name="payment-failed"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("contact/", views.contact, name="contact"),
    path("gallery/", views.gallery, name="gallery"),
    path("booking-detail/<int:id>/", views.bookingDetail, name="booking-detail"),
    path("process-travel-info/<int:id>/<int:num>/", views.processTravelInfo, name="process-travel-info")
]
