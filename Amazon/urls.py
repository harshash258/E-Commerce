from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', views.index, name='index'),
                  path('register/', views.register, name='register'),
                  path("login/", views.signIn, name='signIn'),
                  path('logout/', views.logoutUser, name='logout'),
                  path("product=<str:slug>/", views.viewProduct, name="viewProduct"),
                  path('accounts/', include('allauth.urls')),
                  path("search_result/", views.searchProduct, name="searchResult"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
