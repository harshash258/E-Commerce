from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from . import views

urlpatterns = [
                  path('', views.index, name='index'),
                  path('register/', views.register, name='register'),
                  path("login/", views.signIn, name='login'),
                  path('logout/', views.logoutUser, name='logout'),
                  path("product=<str:slug>/", views.viewProduct, name="viewProduct"),
                  path('accounts/', include('allauth.urls')),
                  path("product_search/", views.searchProduct, name="searchResult"),
                  path("mycart/", views.viewCart, name='myCart'),
                  path("updateItem/", views.addToCart),
                  path('profile/<username>/', views.viewProfile, name='profile'),
                  path('checkout/', views.checkOut, name='checkout'),
                  path('payment', views.payment, name='payment')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
