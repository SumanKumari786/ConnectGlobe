from django.contrib import admin
from django.urls import path

from Globe import views
from Globe.views import ActivateAccount

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<str:slug>', views.continuepost, name='postcontinue'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),

]
