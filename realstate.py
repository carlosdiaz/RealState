from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from functools import wraps
import sqlite3


app = Flask(__name__)

#app.database = "marciarealstate.db"
app.database = "realstate.db"
app.secret_key = "xcFtjs3Ji896Ghm"



@app.route('/')
def home():
	return render_template('index.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/departamentos')
def departamentos():
	return render_template('depas.html')

@app.route('/depaslist')
def depaslist():
	g.db = connect_db()
	cur = g.db.execute('select price, type, contract, location, description, imagetodisplay from properties')
	propertyRecords = [dict(price=row[0], type=row[1], contract=row[2] , location=row[3], description=row[4], imagetodisplay=row[5]) for row in cur.fetchall()]
	#(ID TEXT, PRICE TEXT, TYPE TEXT, CONTRACT TEXT, LOCATION TEXT, BATHROOMS TEXT, BEDROOMS TEXT, AREA TEXT, FEATURES TEXT, DESCRIPTION TEXT)""")
	
	#curLinks = g.db.execute('select name from linksproperties where id = "1"')
	#linksPropertiesRecords = curLinks.fetchone()

	g.db.close()	
	#return render_template('departamentoslist.html', propertyRecords = propertyRecords, linksPropertiesRecords = linksPropertiesRecords)
	return render_template('departamentoslist.html', propertyRecords = propertyRecords)
	#return render_template('departamentoslist.html',  linksPropertiesRecords = linksPropertiesRecords)

@app.route('/casaslist')
def casaslist():
	return render_template('casaslist.html')

@app.route('/terrenoslist')
def terrenoslist():
	return render_template('terrenoslist.html')

@app.route('/acerca')
def acerca():
	return render_template('acerca.html')

def connect_db():
	return sqlite3.connect(app.database)


if __name__ == '__main__':
    #app.run()
    app.run(debug=True)