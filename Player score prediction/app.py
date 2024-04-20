from flask import Flask, jsonify, request, render_template
import pandas as pd
import numpy as np
app = Flask(__name__)

# Load your dataset
df = pd.read_csv('complete_dataset.csv')

@app.route('/')
def index():
    teams = df['team'].dropna().unique().tolist()  # Extract unique teams and convert to list
    return render_template('index.html', teams=teams)

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

if __name__ == '__main__':
    app.run(debug=True)
