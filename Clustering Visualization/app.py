from flask import Flask, render_template, request, send_file, jsonify
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

#code for player score prediction
df = pd.read_csv('../dataset/complete_dataset.csv')

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
    
    return render_template('shot_chart.html', team_name=team_name, season_id=season_id, active_tab = 'maps')

@app.route('/player-score-prediction')
def score_prediction():
    teams = df['team'].dropna().unique().tolist()  # Extract unique teams and convert to list
    return render_template('scorePrediction.html', teams=teams, active_tab ='player_score_prediction')

@app.route('/data', methods=['POST'])
def data():
    print(request.json)
    if not request.json or 'team' not in request.json:
        return jsonify({'error': 'Missing or malformed request data'}), 400
    team = request.json['team']
    filtered_df = df[df['team'] == team]
       # Count the number of entries per player and select the top 10 players with the most entries
    top_players_counts = filtered_df['player_name'].value_counts().nlargest(10)
    top_players = filtered_df[filtered_df['player_name'].isin(top_players_counts.index)]

    data = []
    for player in top_players['player_name'].unique():
        player_data = top_players[top_players['player_name'] == player]
        player_data = player_data.loc[player_data.groupby('season')['predator_total'].idxmax()]
        player_data_sorted = player_data.sort_values(by='season')  # Sort data by season
        # trace = {
        #     'x': player_data_sorted['season'].tolist(),
        #     'y': player_data_sorted['predator_total'].tolist(),
        #     'type': 'scatter',
        #     'mode': 'lines+markers',
        #     'name': player,
        #     'line': {'dash': np.where(player_data_sorted['season'].isin(['2023', '2024']), 'dash', 'solid').tolist()}
        # }
        # data.append(trace)

        actual_data = player_data_sorted[player_data_sorted['season'] <= 2022]
        predicted_data = player_data_sorted[player_data_sorted['season'] >= 2022]

        # Trace for actual data
        trace_actual = {
            'x': actual_data['season'].tolist(),
            'y': actual_data['predator_total'].tolist(),
            'type': 'scatter',
            'mode': 'lines+markers',
            'name': player,
            'line': {'dash': 'solid'}
        }
        data.append(trace_actual)

        # Trace for predicted data
        if not predicted_data.empty:  # Check if there is any predicted data
            trace_predicted = {
                'x': predicted_data['season'].tolist(),
                'y': predicted_data['predator_total'].tolist(),
                'type': 'scatter',
                'mode': 'lines+markers',
                'name': player + ' (Predicted)',
                'line': {'dash': 'dash'},
                'showlegend': False  # Avoid duplicate legend entries
            }
            data.append(trace_predicted)
    return jsonify(data)


#d3 visualization
@app.route('/moe-table')
def visualization():
    return render_template('moe_table.html', active_tab='moe_table')

@app.route('/results-data')
def resultsData():
    return send_file('../dataset/results.csv', as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)
