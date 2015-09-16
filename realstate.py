from flask import Flask, render_template
app = Flask(__name__)


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
	return render_template('departamentoslist.html')

@app.route('/casaslist')
def casaslist():
	return render_template('casaslist.html')


if __name__ == '__main__':
    app.run()