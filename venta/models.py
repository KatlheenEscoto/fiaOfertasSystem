from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Vendedor(models.Model):
	carnet = models.CharField(max_length=7)
	nombre = models.CharField(max_length=50)
	apellido = models.CharField(max_length=50)
	telefono = models.CharField(max_length=10,blank=True)
	email = models.CharField(max_length=50, blank=True)
	password = models.CharField(max_length=10)
	image = models.ImageField(blank=True)
	genero = models.CharField(max_length=10, blank=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)


class Producto(models.Model):
	nombre = models.CharField(max_length=100)
	precio = models.DecimalField(max_digits=6, decimal_places=2)
	fecha = models.DateField()
	descripcion=  models.CharField(max_length=100)
	image = models.ImageField(blank=False)
	tipo = models.CharField(max_length=17)
	vendedor = models.ForeignKey(settings.AUTH_USER_MODEL)

	def __str__(self):
		return self.nombre

class comentarioProducto(models.Model):
	texto = models.CharField(max_length=100)
	emisor = models.CharField(max_length=50)
	producto = models.ForeignKey(Producto,on_delete=models.CASCADE)

class mensaje(models.Model):
	texto = models.CharField(max_length=100)
	emisor = models.CharField(max_length=50)
	usuario = models.ForeignKey(settings.AUTH_USER_MODEL)


class Utilidad(models.Model):
	nombre = models.CharField(max_length=100)
	saldo = models.DecimalField(max_digits=10, decimal_places=2)
	concepto = models.CharField(max_length=150)
	fecha = models.DateField()
	user = models.ForeignKey(settings.AUTH_USER_MODEL)


class ReportarUsuario(models.Model):
	numeroReport = models.IntegerField(default=0,blank=True)
	usuarioReportado = models.ForeignKey(settings.AUTH_USER_MODEL)
	

class TipoReporte(models.Model):
	usuarioReportador = models.ForeignKey(settings.AUTH_USER_MODEL)
	tipo = models.CharField(max_length=200)
	reportes = models.ForeignKey(ReportarUsuario,on_delete=models.CASCADE)
