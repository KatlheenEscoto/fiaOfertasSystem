from django.db.models import Count
from django.utils import timezone
from .models import *

def modificarUsuario(id_usuario, email, telefono):
	perfil = get_object_or_404(Vendedor, pk= id_usuario)
	try:
		perfil.email=email
		perfil.telefono=telefono

	except (KeyError, perfil.DoesNotExist):
		return -1
	else:
		return 0


