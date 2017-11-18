from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.http.response import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.views.defaults import page_not_found
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Sum
from datetime import time, date
from .models import *
from .reporte import generar_reporte
from django.db.models import Q
from .inicializar import *
from django.contrib.staticfiles import  *
#metodo para logearse
def auth_login(request):
	if request.method == 'POST':
		username = request.POST.get('username',None)
		password = request.POST.get('password', None)
		user = authenticate(username=username, password=password)
	 	if user:
			login(request,user)
			return redirect('/')
		else :
			valor = "Volver a escribir credenciales."
			context= { 'valor':valor }
			return render(request,'Main/login.html',context)

	context= {}
	return render(request,'Main/login.html',context)

#metodo para registrarse
def auth_signup(request):
	newUser = Vendedor()
	if request.method == 'POST':
		username = request.POST.get('username',None)
		password = request.POST.get('password', None)
		password2 = request.POST.get('password2', None)
		email=request.POST.get('email',None)
		user = authenticate(username=username, password=password, password2=password2)
		
		if user :
		 	valor = "Ese usuario ya esta registrado, seleccione otro"
			context= { 'valor':valor }
			return render(request,'Main/registrar.html',context)
		if password==password2:
			newUser.carnet = username
			newUser.password = request.POST.get('password',None)
			newUser.password2 = request.POST.get('password2',None)
			newUser.nombre = request.POST.get('nombre',None)
			newUser.apellido =request.POST.get('apellido',None)
			genero = request.POST.get('genero',None)
			newUser.image= request.FILES.get('imagen',None)
			newUser.genero=genero

			newUser.telefono= request.POST.get('telefono',None)
			newUser.email=request.POST.get('email',None)
			user = User.objects.create_user(username=username,email=email, password= password)
		 	user.save()
		 	report = ReportarUsuario()
		 	report.usuarioReportado=user
		 	report.save()
		 	newUser.user=user
			newUser.save()
		 	login(request,user)
		 	return redirect('/')
		else :
			valor1 = "Las contrasenias son diferentes"
			context= { 'valor1':valor1 }
			return render(request,'Main/registrar.html',context) 	
	context= {}
	return render(request,'Main/registrar.html',context)
	
"""def mi_error_404(request):
    nombre_template = '404.html'
    return page_not_found(request, template_name=nombre_template)
 """

def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response


def index(request):
	product = Producto.objects.order_by('fecha') #todos los productos
	electronico=Producto.objects.filter(tipo__contains='electronico').order_by('fecha')
	material=Producto.objects.filter(tipo__contains='material').order_by('fecha')
	libros =Producto.objects.filter(tipo__contains='libros').order_by('fecha')
	otros=Producto.objects.filter(tipo__contains='otros').order_by('fecha')
	template = loader.get_template('Main/index.html')
	todos = User.objects.all()
	usuarios = User.objects.exclude(username__contains='fiaOferta2017')
	superuser = User.objects.filter(username__contains='fiaOferta2017')
	iniciarSuperUser()
	i = len(product)

	context = {
		'i':i,
		'todos':todos,
		'usuarios':usuarios,
		'superuser':superuser,
		'electronico':electronico,
		'material':material,
		'libros':libros,
		'otros':otros,
		'product':product,
	}
	if request.method=='POST':
		action=request.POST.get('action',None)
		if action =='buscar':
			nombre = request.POST.get('buscar',None)
			context=buscar(nombre)
			return HttpResponse(template.render(context,request) )
	return HttpResponse(template.render(context, request))


def superUsuario(request):
	template=loader.get_template('Main/index.html')
	context = 'Estas como super usuario'
	return HttpResponse(template.render(context,request))

def buscar(nombre):
	producto = Producto.objects.filter(nombre__contains=nombre).order_by('fecha')
	i = len(producto)
	context ={'otros':producto,'i':i, 'busqueda':'busqueda'}
	return context

def reporte(request):
	usuario=request.user
	return generar_reporte(request, usuario)


def ver_producto(request,  producto_id):
	producto = get_object_or_404(Producto, pk= producto_id)
	try:
		nomb = request.user
		context={'producto':producto,'nomb':nomb}
		return render(request,'Main/producto.html',context)

	except (KeyError, producto.DoesNotExist):
		return render(request, '404.html', {
		    	'error_message': "Tiene que seleccionar una respuesta",
		})
	else:
		return redirect('/')


def perfil(request):
	template = loader.get_template('Main/perfil.html')
	return HttpResponse(template.render({}, request))


def ver_mensajes(request):
	template = loader.get_template('Main/mensajes.html')
	return HttpResponse(template.render({}, request))

def misventas(request):
	template = loader.get_template('Main/misventas.html')
	utilidad = 0;

	usuario = request.user
		#utilidad = Utilidad.objects.aggregate(Sum('saldo'))
	for ut in request.user.utilidad_set.all() :
		utilidad = utilidad + ut.saldo

	return HttpResponse(template.render({'utilidad':utilidad}, request))	
	

def ver_perfil(request, perfil_id):
	perfil = get_object_or_404(User, pk= perfil_id)
	usuario = request.user
	try:
		if request.method=='POST':
			try:
				tipo = TipoReporte.objects.get(usuarioReportador=usuario)
				reportes = ReportarUsuario.objects.filter(usuarioReportado=perfil)
				context = {'perfil':perfil,'usuario':usuario,'reportes':reportes,'valor':'ya antes ha reportado a este usuario'}
				return render(request,'Main/ver_perfil.html',context)
			except (KeyError, TipoReporte.DoesNotExist):
				reporte = ReportarUsuario.objects.get(usuarioReportado=perfil)
				tipo = TipoReporte()
				tipo.tipo=request.POST.get('dato',None)
				tipo.usuarioReportador=usuario
				reporte.numeroReport = reporte.numeroReport+1
				reporte.save()
				tipo.reportes=reporte
				tipo.save()
		
		reportes = ReportarUsuario.objects.filter(usuarioReportado=perfil)
		context = {'perfil':perfil,'usuario':usuario,'reportes':reportes,}
		return render(request,'Main/ver_perfil.html',context)
		
	except (KeyError, perfil.DoesNotExist):
		return render(request, 'Main/404.html', {
		    	'error_message': "Tiene que seleccionar una respuesta",
		})
	else:
		return redirect('/')

def eliminarUtilidad(request):
	usuario = request.user
	try:
		for ut in usuario.utilidad_set.all() :
			ut.delete()
		return render_to_response('Main/index.html',{'mensaje':'objeto eliminado con exito'})
	except (KeyError, venta.DoesNotExist):
		return render(request, 'Main/404.html', {
		    	'error_message': "No selecciono una venta valida a eliminar",
		})
	else:
		return redirect('/')

def EliminarUsuario(request,user_id):
	usuarioE = get_object_or_404(User,pk= user_id)
	try:
		usuarioE.delete()
		return render_to_response('Main/index.html',{'mensaje':'objeto eliminado con exito'})
	except (KeyError, venta.DoesNotExist):
		return render(request, 'Main/404.html', {
		    	'error_message': "No selecciono una venta valida a eliminar",
		})
	else:
		return redirect('/')

def editar(request, perfil_id):
	perfil = get_object_or_404(Vendedor, pk= perfil_id)
	try:
		if request.method == 'POST' :
			email = request.POST.get('email','SM') #SM = Sin Modificacion
			cel = request.POST.get('telefono','SM')
			perfil.telefono = cel
			perfil.email= email
			newId = request.POST.get('newid','SM')
			perfil.save()
			context={'email':email, 'cel':cel, 'perfil':perfil, perfil_id:'perfil_id', 'newid':newId}

			return render_to_response('Main/index.html',context)		
		else :
			context={'perfil':perfil}
			return render_to_response('Main/editar.html',context)	

	except (KeyError, perfil.DoesNotExist):
		return render(request, 'Main/404.html', {
		    	'error_message': "Tiene que seleccionar",
		})
	else:
		return redirect('/')

def editar_foto(request, perfil_id):
	perfil = get_object_or_404(Vendedor, pk= perfil_id)
	try:
		if request.method == 'POST':
			foto = request.FILES.get('imagen','SM') #SM = Sin Modificacion
			perfil.image=foto
			perfil.save()
			context={perfil_id:'perfil_id', foto:'foto'}			
			return render_to_response('Main/index.html',context)		
		else :
			context={'perfil':perfil}
			return render_to_response('Main/editar_foto.html',context)	

	except (KeyError, perfil.DoesNotExist):
		return render(request, 'Main/404.html', {
		    	'error_message': "Tiene que seleccionar",
		})
	else:
		return redirect('/')

def editar_contra(request, user_id):
	perfil = get_object_or_404(User, pk= user_id)
	try:
		if request.method == 'POST':
			password=request.POST.get('password', None)
			pas=check_password(password, perfil.password)
			if pas:
			
			    contra = request.POST.get('contra',None) 
			    info='Debe volver a iniciar sesion'
			    perfil.set_password(contra)
			    perfil.save()
			    login(request,perfil)#esto es xq al guardar otra contrasena cierra sesion
			    #update_session_auth_hash(request,perfil) #tambien se puede usar 
			    info='Debe volver a iniciar sesion'
			    context={contra:'contra', info:'info'}
			    return redirect('/',context)
			else:
				valor='Contrasenia incorrecta'
				context={'valor':valor}
				return render(request, 'Main/perfil.html', context)
            

		else :
			context={}
			return render_to_response('Main/editar_contra.html',context)	

	except (KeyError, perfil.DoesNotExist):
		return render(request, 'Main/404.html', {
		    	'error_message': "Tiene que seleccionar",
		})
	else:
		return redirect('/')

def comentario_producto(request, prod_id):
	product = get_object_or_404(Producto, pk= prod_id)
	try:
		if request.method == 'POST':
			mess = comentarioProducto()
			emisor = request.POST.get('emisor',None) 
			coment = request.POST.get('coment',None) 
			mess.texto=coment
			mess.emisor=emisor
			mess.producto=product
			mess.save()
			context={emisor:'emisor', coment:'coment'}
			return redirect('/',context)
		else :
			context={}
			return redirect('/',context)

	except (KeyError, product.DoesNotExist):
		return render(request, 'Main/404.html', {
		    	'error_message': "Tiene que seleccionar",
		})
	else:
		return redirect('/')

def mensaje_envio(request, envio_id):
	usuario = get_object_or_404(User, pk= envio_id)
	try:
		if request.method == 'POST':
			mess = mensaje()
			emisor = request.POST.get('emisor',None) 
			coment = request.POST.get('coment',None) 
			mess.texto=coment
			mess.emisor=emisor
			mess.usuario=usuario
			mess.save()
			context={emisor:'emisor', coment:'coment'}
			return redirect('/',context)
		else :
			context={}
			return render_to_response('Main/index.html',context)	
	except (KeyError, usuario.DoesNotExist):
		return render(request, 'Main/404.html', {
		    	'error_message': "Tiene que seleccionar",
		})
	else:
		return redirect('/')



def nuevoProducto(request):
	newProduct = Producto()
	if request.method == 'POST':
		newProduct.nombre= request.POST.get('nombre',None)
		newProduct.precio= request.POST.get('precio',None)
		newProduct.fecha= date.today()
		newProduct.descripcion= request.POST.get('descripcion',None)
		newProduct.image=request.FILES.get('imagen',None)
		newProduct.vendedor= request.user
		newProduct.tipo=request.POST.get('tipo',None)		
		newProduct.save()
		return redirect('/')
	context= {
	}
	return render(request,'Main/edicionProducto.html',context)


def eliminarVenta(request, venta_id):
	venta = get_object_or_404(Producto,pk=venta_id)
	try:
		util = Utilidad()
		util.nombre = venta.nombre
		util.saldo = venta.precio
		util.concepto=venta.descripcion
		util.fecha=date.today() #dia de la venta
		util.user=venta.vendedor
		util.save()
		venta.delete()
		return render_to_response('Main/index.html',{'mensaje':'objeto eliminado con exito','saldo':util.saldo, 'nombre':util.nombre})
	except (KeyError, venta.DoesNotExist):
		return render(request, 'Main/404.html', {
		    	'error_message': "No selecciono una venta valida a eliminar",
		})
	else:
		return redirect('/')



