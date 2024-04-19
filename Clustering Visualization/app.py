from flask import Flask, render_template, request, redirect, url_for
from clustering import cluster

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cluster', methods=['POST'])
def cluster_route():
    if request.method == 'POST':
        selected_year = request.form['year']
        # Call the cluster function with the selected year
        cluster(selected_year)
        # Redirect the user back to the homepage after processing the form
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
