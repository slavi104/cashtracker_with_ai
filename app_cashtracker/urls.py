from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from .views.General import *
from .views.Categories import *
from .views.Profiles import *
from .views.Payments import *
from .views.Register import *
from .views.Login import *
from .views.Reports import *

urlpatterns = [
    url(r'^select_category/',
        csrf_exempt(select_category), name='select_category'),
    url(r'^generate_fake_payments/(?P<number_of_payments>[0-9]+)',
        generate_fake_payments, name='generate_fake_payments'),
    url(r'^delete_report/$', delete_report, name='delete_report'),
    url(r'^delete_payment/$', csrf_exempt(delete_payment),
        name='delete_payment'),
    url(r'^reports/$', reports, name='reports'),
    url(r'^payments/$', csrf_exempt(payments), name='payments'),
    url(r'^generate_report/$', generate_report, name='generate_report'),
    url(r'^add_payment/$', csrf_exempt(add_payment), name='add_payment'),
    url(r'^add_edit_category_action/([0-9]+)',
        add_edit_category_action, name='add_edit_category_action'),
    url(r'^delete_category_action/(?P<category_id>[0-9]+)',
        delete_category_action, name='delete_category_action'),
    url(r'^add_edit_category/(?P<category_id>[0-9]+)',
        add_edit_category, name='add_edit_category'),
    url(r'^edit_categories/$', edit_categories, name='edit_categories'),
    url(r'^edit_profile/$', edit_profile, name='edit_profile'),
    url(r'^edit_profile_action/$',
        csrf_exempt(edit_profile_action), name='edit_profile_action'),
    url(r'^login/$', login, name='login'),
    url(r'^login_action/$', csrf_exempt(login_action), name='login_action'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^register/$', csrf_exempt(register), name='register'),
    url(r'^register_action/$', csrf_exempt(register_action),
        name='register_action'),
    url(r'^home/$', csrf_exempt(home), name='home'),
    url(r'^$', index, name='index'),
]
