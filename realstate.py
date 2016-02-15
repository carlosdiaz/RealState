from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from functools import wraps
import sqlite3
import smtplib


app = Flask(__name__)

#app.database = "marciarealstate.db"
#Next was the original database
#app.database = "realstate.db"
#Next is the database created with flask admin
app.database = "/tmp/propertyRS.db"

app.secret_key = "xcFtjs3Ji896Ghm"



@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		#flash('Es un post' )
		if request.form['state'] != "" :	
			stateValue = request.form['state']
			cityValue = request.form['city']
			statusValue = request.form['status']
			typeValue = request.form['type']
			propertyRecords = searchProperties(stateValue, cityValue, statusValue, typeValue)		
			return render_template('searchlist.html', propertyRecords = propertyRecords)

	g.db = connect_db()
	#cur = g.db.execute('select id, price, typeprop, contract, location, description, imagetodisplay, area, bathrooms , bedrooms from property order by id desc limit 4' )	
	cur = g.db.execute('select property.id, price, typeprop, contract, location, description, image.path, area, bathrooms , bedrooms from property inner join image on property.id = image.property_id order by property.id desc limit 4' )	
	#select * from property inner join image on property.id = image.id order by property.id desc limit 4
	propertyRecords = [dict(id=row[0], price=row[1], type=row[2], contract=row[3] , location=row[4], description=row[5], imagetodisplay=row[6], area=row[7], bathrooms=row[8], bedrooms=row[9]) for row in cur.fetchall()]
	g.db.close()

	#print propertyRecords
	print "##########################################################"

	#Now we get the properties that are ready to be sold
	g.db = connect_db()
	#cur = g.db.execute("select id, price, type, contract, location, description, imagetodisplay from property where contract = 'Venta' order by id desc limit 3" )	
	cur = g.db.execute("select property.id, price, typeprop, contract, location, description, image.path from property inner join image on property.id = image.property_id where contract = 'Venta' order by property.id desc limit 3" )	
	propertyRecordsRented = [dict(id=row[0], price=row[1], type=row[2], contract=row[3] , location=row[4], description=row[5], imagetodisplay=row[6]) for row in cur.fetchall()]
	g.db.close()

	print propertyRecordsRented


	#Now we get the properties that are ready to be rented
	g.db = connect_db()
	#cur = g.db.execute("select id, price, type, contract, location, description, imagetodisplay, area, bathrooms, bedrooms from properties where contract = 'Renta' order by id desc limit 2" )	
	cur = g.db.execute("select property.id, price, typeprop, contract, location, description, image.path, area, bathrooms, bedrooms from property inner join image on property.id = image.property_id where contract = 'Renta' order by property.id desc limit 2" )	
	propertyRecordsSold = [dict(id=row[0], price=row[1], type=row[2], contract=row[3] , location=row[4], description=row[5], imagetodisplay=row[6], area=row[7], bathrooms=row[8], bedrooms=row[9]) for row in cur.fetchall()]
	g.db.close()

	print propertyRecordsSold

	return render_template('index.html', propertyRecords = propertyRecords, propertyRecordsSold = propertyRecordsSold, propertyRecordsRented = propertyRecordsRented)


@app.route('/contact', methods= ['GET', 'POST'])
def contact():	
	if request.method == 'POST':
		flash('enviar mail' )
		print('Estamos dentro del post')
		if request.form['name'] != "" :	
			name = request.form['name']
			email = request.form['email']
			print(email)
			subject = request.form['subject']
			message = request.form['message']

			sender = email
			receivers = ['diazcont@hotmail.com']
			
			try:
			   print "Before sending email"
			   smtpObj = smtplib.SMTP('localhost')
			   print "Right Before sending email"
			   smtpObj.sendmail(sender, receivers, message)         
			   print "Successfully sent email"
			except Exception:
			   print "Error: unable to send email"
			#propertyRecords = searchProperties(stateValue, cityValue, statusValue, typeValue)		
			#return render_template('searchlist.html')
	elif request.method == 'GET':
		print('Estamos dentro del get')

	return render_template('contact.html')

@app.route('/departamentos')
def departamentos():
	return render_template('depas.html')

@app.route('/depaslist')
def depaslist():
	g.db = connect_db()
	cur = g.db.execute('select property.id, price, typeprop, contract, location, description, image.path from property inner join image on property.id = image.property_id where typeprop="Departamento"' )
	propertyRecords = [dict(id=row[0], price=row[1], type=row[2], contract=row[3] , location=row[4], description=row[5], imagetodisplay=row[6]) for row in cur.fetchall()]
	g.db.close()	
	
	#print propertyRecords

	return render_template('departamentoslist.html', propertyRecords = propertyRecords)
	#return render_template('departamentoslist.html',  linksPropertiesRecords = linksPropertiesRecords)

@app.route('/casaslist')
def casaslist():
	g.db = connect_db()
	cur = g.db.execute('select property.id, price, typeprop, contract, location, description, image.path from property inner join image on property.id = image.property_id where typeprop="Casa"' )
	propertyRecords = [dict(id=row[0], price=row[1], type=row[2], contract=row[3] , location=row[4], description=row[5], imagetodisplay=row[6]) for row in cur.fetchall()]
	g.db.close()	
	#print propertyRecords
	
	return render_template('casaslist.html' , propertyRecords = propertyRecords)

@app.route('/terrenoslist')
def terrenoslist():
	g.db = connect_db()
	cur = g.db.execute('select property.id, price, typeprop, contract, location, description, image.path from property inner join image on property.id = image.property_id where typeprop="Terreno"' )
	propertyRecords = [dict(id=row[0], price=row[1], type=row[2], contract=row[3] , location=row[4], description=row[5], imagetodisplay=row[6]) for row in cur.fetchall()]
	g.db.close()	
	#print propertyRecords
	
	return render_template('terrenoslist.html' , propertyRecords = propertyRecords)


@app.route('/description/<int:post_id>')
def show_post(post_id):
    g.db = connect_db()
    sql = 'select property.id, price, typeprop, contract, location, state, description, image.path from property inner join image on property.id = image.property_id where property.id=%d' %post_id
    #'select property.id, price, typeprop, contract, location, description, image.path, area, bathrooms , bedrooms from property inner join image on property.id = image.property_id order by property.id desc limit 4' )	
    print sql
    cur = g.db.execute(sql)
    propertyRecords = [dict(id=row[0], price=row[1], type=row[2], contract=row[3] , location=row[4], state=row[5], description=row[6], imagetodisplay=row[7]) for row in cur.fetchall()]
    g.db.close()
    print propertyRecords
    return render_template('single.html', propertyRecords = propertyRecords)


@app.route('/acerca')
def acerca():
	return render_template('acerca.html')

def connect_db():
	return sqlite3.connect(app.database)

def searchProperties( state, city, status, typeprop):
	g.db = connect_db()
	query = 'select property.id, price, typeprop, contract, location, description, image.path from property inner join image on property.id = image.property_id where state = "%s"' %state + ' and typeprop = "%s"' %typeprop
	print query
	cur = g.db.execute(query)
	print 
	#cur = g.db.execute('select price, type, contract, location, description, imagetodisplay from properties where state = %s ' %state  )
	propertyRecords = [dict(id=row[0], price=row[1], type=row[2], contract=row[3] , location=row[4], description=row[5], imagetodisplay=row[6]) for row in cur.fetchall()]
	g.db.close()		
	return propertyRecords

if __name__ == '__main__':
    #app.run()
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=2525, use_reloader=True)