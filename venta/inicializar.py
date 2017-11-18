from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User
from django.db.models import *

def iniciarSuperUser():
	username = 'fiaOferta2017'
	password = 'root_2017'
	email='waltermarro777@hotmail.com'
	try:
		user = User.objects.get(username=username)
		return False
	except :
		user = User.objects.create_superuser(username=username,email=email, password= password)
		user.save()
		return True