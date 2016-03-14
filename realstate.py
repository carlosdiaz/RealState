import sqlite3
import smtplib
from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from functools import wraps
from mapping_model import Property, Image
from sqlalchemy.orm import scoped_session, sessionmaker, Query
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import join



app = Flask(__name__)


#Next was the original database
#app.database = "realstate.db"
#Next is the database created with flask admin
app.database = "propertyRS.db"

app.secret_key = "xcFtjs3Ji896Ghm"

#Next lines are for SQL Alchemy use
engine = create_engine("sqlite:////tmp/propertyRS.db")
Base = declarative_base()
Base.metadata.reflect(engine)



@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'POST':		
		if request.form['state'] != "" :	
			stateValue = request.form['state']
			cityValue = request.form['city']
			statusValue = request.form['status']
			typeValue = request.form['type']
			propertyRecords = searchProperties(stateValue, cityValue, statusValue, typeValue)		
			return render_template('searchlist.html', propertyRecords = propertyRecords)
    

	db_session = scoped_session(sessionmaker(bind=engine))
	propertyRecords = []
	propertyRecordsRented = []
	propertyRecordsSold = []
	

	for prop in db_session.query(Property.id, Property.price, Property.typeprop,Property.contract, Property.location, Property.description, Image.path, Property.area, Property.bathrooms, Property.bedrooms).join(Image).order_by(Property.id.desc()).limit(4):
		propertyDict = dict(id=prop[0], price=prop[1], type=prop[2], contract=prop[3] , location=prop[4], description=prop[5], imagetodisplay=prop[6], area=prop[7], bathrooms=prop[8], bedrooms=prop[9])    		
		propertyRecords.append(propertyDict)
		print propertyDict    	
    		
	for prop in db_session.query(Property.id, Property.price, Property.typeprop,Property.contract, Property.location, Property.description, Image.path, Property.area, Property.bathrooms, Property.bedrooms).join(Image).filter(Property.contract == 'Venta').order_by(Property.id.desc()).limit(3):		
		propertyDict = dict(id=prop[0], price=prop[1], type=prop[2], contract=prop[3] , location=prop[4], description=prop[5], imagetodisplay=prop[6], area=prop[7], bathrooms=prop[8], bedrooms=prop[9])    		
		propertyRecordsRented.append(propertyDict)
		#print propertyDict


	#Now we get the properties that are ready to be rented
	for prop in db_session.query(Property.id, Property.price, Property.typeprop,Property.contract, Property.location, Property.description, Image.path, Property.area, Property.bathrooms, Property.bedrooms).join(Image).filter(Property.contract == 'Renta').order_by(Property.id.desc()).limit(2):		
		propertyDict = dict(id=prop[0], price=prop[1], type=prop[2], contract=prop[3] , location=prop[4], description=prop[5], imagetodisplay=prop[6], area=prop[7], bathrooms=prop[8], bedrooms=prop[9])    		
		propertyRecordsSold.append(propertyDict)
		print propertyDict
		
	print propertyRecordsSold
	return render_template('index.html', propertyRecords = propertyRecords, propertyRecordsSold = propertyRecordsSold, propertyRecordsRented = propertyRecordsRented)


@app.route('/contact', methods= ['GET', 'POST'])
def contact():	
	if request.method == 'POST':
		flash('enviar mail' )		
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

@app.errorhandler(404)
def page_not_found(error):	
	return render_template('404.html'), 404

if __name__ == '__main__':
    #app.run()
    #app.run(debug=True)
    app.debug = False
    app.run()
    #app.run(host='0.0.0.0', port=2525, use_reloader=True)