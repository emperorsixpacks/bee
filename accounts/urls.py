from django.urls import path, include
from .emailview import verify_user_and_activate, request_new_link
from .views import deactivate_and_activate_url, register, login, referral_register, logout, settings


urlpatterns = [
    path(f'user/verify-email/<useremail>/<usertoken>/', verify_user_and_activate, name='verify-email'),
    path(f'user/verify-email/request-new-link/<useremail>/<usertoken>/', request_new_link, name='request-new-link'
                                                                                                '-from-token'),
    path(f'user/verify-email/request-new-link/', request_new_link, name='request-new-link-from-email'),
    path(f'account-deactivated/', deactivate_and_activate_url, name='activate'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('settings/', settings, name='settings'),
    path('referral/<str:code>', referral_register, name='referral'),

]
