from __future__ import unicode_literals
from __future__ import absolute_import #importamos ambas lineas para que no se generen errores

from django.conf.urls import url, handler404
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib import admin

#from django.conf.urls import handler404
#import django.views.defaults 

app_name = 'venta'
admin.autodiscover()


urlpatterns = [
    url(r'^login/$', views.auth_login,name="authentication"),
    url(r'^registrarse/$', views.auth_signup,name="authentication"),
    url(r'^logout/$',auth_views.logout, {'next_page':'/'}, name='logout'),
    url(r'^$', views.index),
	url(r'^perfil/', views.perfil,name='perfil'),
    url(r'^mensajes/', views.ver_mensajes),
    url(r'^misventas/', views.misventas),
    url(r'^eliminarUtilidad/', views.eliminarUtilidad),
    url(r'^(?P<producto_id>[0-9]+)/producto/$', views.ver_producto, name="producto"), 
    url(r'^(?P<perfil_id>[0-9]+)/ver_perfil/$',views.ver_perfil, name='ver_perfil'),
    url(r'^(?P<perfil_id>[0-9]+)/editar$',views.editar, name='editar'),
    url(r'^(?P<perfil_id>[0-9]+)/editar_foto/$',views.editar_foto, name='editar_foto'),
    url(r'^(?P<user_id>[0-9]+)/editar_contra/$',views.editar_contra, name='editar_contra'),
    url(r'^(?P<envio_id>[0-9]+)/message/$',views.mensaje_envio, name='message'),    
    url(r'^(?P<prod_id>[0-9]+)/comentario/$',views.comentario_producto, name='comentario'),
    url(r'^(?P<venta_id>[0-9]+)/eliminar/$',views.eliminarVenta, name='eliminar'),
    url(r'^(?P<user_id>[0-9]+)/eliminarUsuario/$',views.EliminarUsuario, name='eliminarUsuario'),
    url(r'^reporte/$', views.reporte),
	url(r'^nuevoProducto/', views.nuevoProducto),
]


