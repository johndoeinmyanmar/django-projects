from django.conf.urls import url
from . import views
import django.contrib.auth.views as auth_views

urlpatterns = [
	#post views
	#url(r'^login/$', views.user_login, name='login'),
	#dashboard url
	url(r'^dashboard/$', views.dashboard, name='dashboard'),
	url(r'^edit/$', views.edit, name='edit'),
	url(r'^dashboard/(?P<slug>[-\w]+)/(?P<postfix>[-\w]+)/$', views.item_edit, name='item_edit'),
	url(r'^share/$', views.shareform, name='share'),
	url(r'^show_info/$', views.show_info, name='show_info'),

	#login / logout urls
	url(r'^login/$', auth_views.login, name='login'),
	url(r'^logout/$', auth_views.logout, name='logout'),
	url(r'^logout-then-login/$', auth_views.logout_then_login, name='logout_then_login'),

	#password change
	url(r'^password-change/$', auth_views.password_change,name='password_change'),
	url(r'^password-change/done/$', auth_views.password_change_done, name='password_change_done'),

	#password reset
	url(r'^password-reset/$', auth_views.password_reset, name='password_reset'),
	url(r'^password-reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
	url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',auth_views.password_reset_confirm,
		name='password_reset_confirm'),
	url(r'^password-reset/complete/$', auth_views.password_reset_complete,
		name='password_reset_complete'),


	#register the user
	url(r'^register/$', views.register, name='register'),
]