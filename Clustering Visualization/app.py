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
        pca_plot_path, tsne_plot_path, cluster_stats, players_grouped = cluster(selected_year)
        # Redirect the user back to the homepage after processing the form
        return render_template('results.html', pca_plot_path=pca_plot_path, tsne_plot_path=tsne_plot_path, cluster_stats=cluster_stats, players_grouped=players_grouped)


if __name__ == '__main__':
    app.run(debug=True)
