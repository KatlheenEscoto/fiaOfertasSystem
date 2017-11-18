import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, cm 
from reportlab.platypus import Paragraph, TableStyle,Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from django.http import HttpResponse
from datetime import time, date
from django.conf import settings


def generar_reporte(request, usuario):
	#Creando la cabecera HTTPResponse con PDF.
	response =HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename=Ventas.pdf'
	
	#Creando el objeto PDF, usando el objeto BytesIO
	buffer = BytesIO()
	fecha= date.today()
	c = canvas.Canvas(buffer,pagesize=A4)

	#Cabecera
	cabecera(c)
	c.setLineWidth(.3)
	c.setFont('Helvetica',25)
	c.drawString(30,750,'FIAOfertas')
	#Se lee de izquierda a derecha y de abajo hacia arriba.

	c.setFont('Helvetica',12)
	c.drawString(30,735,'Reporte')

	c.setFont('Helvetica',12)
	c.drawString(480,750,fecha.strftime("%d-%m-%y"))
	c.line(460,747,560,747)

	#Table Header.
	styles = getSampleStyleSheet()
	styleBH = styles["Normal"]
	styleBH.alignment = TA_CENTER
	styleBH.fontSize = 12

	numero = Paragraph('''#''', styleBH)
	nombre = Paragraph('''Producto''', styleBH)
	precio = Paragraph('''Precio''', styleBH)
	fechaProducto = Paragraph('''Fecha''', styleBH)

	data = []

	data.append([numero, nombre, precio, fechaProducto])

	#i = 1
	#for ut in request.user.utilidad_set.all():
	#	utilidades = [{'#': i, 'nombre':ut.nombre, 'precio': ut.saldo, 'fechaProducto': ut.fecha, }]
	#	i = i + 1

	utilidades = [
		{'#':i+1, 'nombre': ut.nombre, 'precio': ut.saldo, 'fechaProducto':ut.fecha}
		for i, ut in enumerate(request.user.utilidad_set.all())
	]

	#utilidades

	#utilidades = [{'#':'1', 'nombre':'Carro', 'precio': '400.00', 'fechaProducto':'10/20/30'},
	#			  {'#':'2', 'nombre':'Carro2', 'precio': '400.00', 'fechaProducto':'10/20/30'},]

	#Table
	styleN = styles["BodyText"]
	styleN.alignment = TA_CENTER
	styleN.fontSize = 10

	high = 650
	for util in utilidades:
		this_utilidad = [util['#'], util['nombre'], util['precio'], util['fechaProducto']]
		data.append(this_utilidad)
		high = high - 18

	#Table size
	width, height = A4
	table = Table(data, colWidths=[2.5 * cm, 9.5 * cm, 3 * cm, 3.5 * cm])
	table.setStyle(TableStyle([ #Estilos de la tabla
		('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
		('BOX', (0, 0), (-1, -1), 0.25, colors.black), ]))

	#PDF size
	table.wrapOn(c, width, height)
	table.drawOn(c, 30,high)


	c.showPage() #Guardar pagina

	#Guardar PDF.
	c.save()

	#Obteniendo los valores de BytesIO buffer y escribiedo el reponse.
	pdf= buffer.getvalue()
	buffer.close()
	response.write(pdf)
	return response

def cabecera(pdf):
	imagen = settings.MEDIA_ROOT+'/fiaOfertasLogo.PNG'
	pdf.drawImage(imagen,40,750,120,90, preserveAspectRatio=True)





