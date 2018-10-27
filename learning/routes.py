from learning import app

@app.route('/')
@app.route('/index')
def index():
	return "Start Here"