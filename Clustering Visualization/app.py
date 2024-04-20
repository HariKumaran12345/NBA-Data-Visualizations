from flask import Flask, render_template, request, redirect, url_for
from clustering import cluster
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import matplotlib

app = Flask(__name__)

#import nba-api
from nba_api.stats.static import teams, players
from nba_api.stats.endpoints import shotchartdetail, playercareerstats, commonteamroster
from shotMapByTeam import getPlayerShotChartDetail, get_contributing_players, create_shot_chart

matplotlib.use('agg')

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
        return render_template('results.html', pca_plot_path=pca_plot_path, tsne_plot_path=tsne_plot_path, cluster_stats=cluster_stats, players_grouped=players_grouped, active_tab = 'index')

@app.route('/shot-map-home')
def shot_map_home():
    return render_template('shot_chart.html')

@app.route('/shot_chart', methods=['POST'])
def shot_chart():
    team_name = request.form['team']
    season_id = request.form['season']
    roster, positions, ppg = get_contributing_players(team_name, season_id)
    print(ppg)
    plt.rcParams['figure.figsize'] = (24, 22)  

    num_players = len(roster)
    rows = 2 
    cols = (num_players + 1) // 2

    fig, axs = plt.subplots(rows, cols)

    if rows > 1 and cols > 1:
        axs = axs.flatten()

    for i, player_name in enumerate(roster):
        player_shotchart_df, league_avg = getPlayerShotChartDetail(player_name, season_id)
        
        # Draw Court and plot Shot Chart for the player
        axs[i].set_title(f"{player_name} ({positions[i]}) - PPG: {ppg[i]}", fontsize=14, pad=10) 
        create_shot_chart(player_shotchart_df, title= axs[i].get_title(), ax=axs[i])
    for j in range(len(roster), rows * cols):
        axs[j].axis('off')

    # Adjust layout and show plot
    fig.suptitle(f"Shot Charts for - {team_name} - Season {season_id}", fontsize=20, y=.98)  
    plt.tight_layout(rect=[0, 1, 1, 0.97])  
    plt.subplots_adjust(hspace=0.1)     
    
    # Save the plot to a file
    plt.savefig('static/shot_chart.png')
    plt.close()  # Close the plot to free up resources
    
    return render_template('shot_chart.html', team_name=team_name, season_id=season_id)


if __name__ == '__main__':
    app.run(debug=True)
