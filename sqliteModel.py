import sqlite3

with sqlite3.connect("realstate.db") as connection:
	c = connection.cursor()
	#c.execute(""" DROP TABLE properties""")
	#c.execute(""" DROP TABLE linksproperties""")
	#First version will only store the path of the image
	
	
	c.execute(""" CREATE TABLE properties (ID TEXT, PRICE TEXT, TYPE TEXT, CONTRACT TEXT, LOCATION TEXT, STATE TEXT, CITY TEXT,
											BATHROOMS TEXT, BEDROOMS TEXT, AREA TEXT, FEATURES TEXT, 
											DESCRIPTION TEXT, IMAGETODISPLAY TEXT)""")

	c.execute(' INSERT INTO properties VALUES("1", "$6,000.00", "Departamento", "Renta", "Cuernavaca", "Morelos", "Cuernavaca", "2", "3", "80 m2", "Piscina, Roof gardern, estacionamiento para dos autos","Precioso departamento en renta bien ubicado", 	"http://serviciosinformaticos.com.mx/MarciaRealState/Departamentos/DepaNaranjos1/11.jpg")')
	c.execute(' INSERT INTO properties VALUES("2", "$1,250,000.00", "Casa", "Venta", "Cuernavaca", "Morelos", "Cuernavaca","2", "3", "80 m2", "Piscina, Roof gardern, estacionamiento para dos autos", "Departamento en venta ", "http://serviciosinformaticos.com.mx/MarciaRealState/Departamentos/DepaNaranjos1/21.jpg")')
	c.execute(' INSERT INTO properties VALUES("3", "$200,000.00", "Terreno", "Venta", "Cuernavaca", "Morelos", "Cuernavaca","NA", "NA", "200 m2", "NA", "Terreno plano en venta", "http://serviciosinformaticos.com.mx/MarciaRealState/Departamentos/DepaNaranjos1/26.jpg") ')
	c.execute(' INSERT INTO properties VALUES("4", "$4,000,000.00", "Bodega", "Venta", "Jiutepec", "Morelos", "Jiutepec","NA", "NA", "500 m2", "NA", "Bodega en venta", "https://farm1.staticflickr.com/741/20117728204_43aea09d3d_k.jpg")')

#[url=https://flic.kr/p/wDJBGQ][img]https://farm1.staticflickr.com/741/20117728204_43aea09d3d_k.jpg[/img][/url][url=https://flic.kr/p/wDJBGQ]Untitled[/url] by [url=https://www.flickr.com/photos/carlos_diaz/]Carlos Diaz[/url], on Flickr
	

	
