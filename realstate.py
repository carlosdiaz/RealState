from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from functools import wraps
import sqlite3


app = Flask(__name__)

#app.database = "marciarealstate.db"
app.database = "realstate.db"
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

			flash('Valor de state %s ' %stateValue )
			flash('Valor de city %s '  %cityValue)
			flash('Valor de city %s '  %statusValue)
			flash('Valor de city %s '  %typeValue)
			return render_template('searchlist.html', propertyRecords = propertyRecords)
		else:
			
			flash('Hubo un error' )
			#return redirect(url_for('welcome'))
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
	cur = g.db.execute('select price, type, contract, location, description, imagetodisplay from properties where type="Departamento"' )
	propertyRecords = [dict(price=row[0], type=row[1], contract=row[2] , location=row[3], description=row[4], imagetodisplay=row[5]) for row in cur.fetchall()]
	g.db.close()	
	
	print propertyRecords

	return render_template('departamentoslist.html', propertyRecords = propertyRecords)
	#return render_template('departamentoslist.html',  linksPropertiesRecords = linksPropertiesRecords)

@app.route('/casaslist')
def casaslist():
	g.db = connect_db()
	cur = g.db.execute('select price, type, contract, location, description, imagetodisplay from properties where type="Casa"' )
	propertyRecords = [dict(price=row[0], type=row[1], contract=row[2] , location=row[3], description=row[4], imagetodisplay=row[5]) for row in cur.fetchall()]
	g.db.close()	
	print propertyRecords
	
	return render_template('casaslist.html' , propertyRecords = propertyRecords)

@app.route('/terrenoslist')
def terrenoslist():
	return render_template('terrenoslist.html')

@app.route('/acerca')
def acerca():
	return render_template('acerca.html')

def connect_db():
	return sqlite3.connect(app.database)

def searchProperties( state, city, status, typeprop):
	g.db = connect_db()
	query = 'select price, type, contract, location, description, imagetodisplay from properties where state = "%s"' %state + ' and type = "%s"' %typeprop
	print query
	cur = g.db.execute(query)
	print 
	#cur = g.db.execute('select price, type, contract, location, description, imagetodisplay from properties where state = %s ' %state  )
	propertyRecords = [dict(price=row[0], type=row[1], contract=row[2] , location=row[3], description=row[4], imagetodisplay=row[5]) for row in cur.fetchall()]
	g.db.close()		
	return propertyRecords

if __name__ == '__main__':
    #app.run()
    app.run(debug=True)