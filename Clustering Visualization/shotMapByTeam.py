import numpy as np
import pandas as pd
import sys

#import the nba api
from nba_api.stats.static import teams,players
from nba_api.stats.endpoints import shotchartdetail, playercareerstats, commonteamroster
#import matplot lib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Circle, Rectangle, Arc, ConnectionPatch, Polygon, PathPatch
from matplotlib.path import Path
from matplotlib.collections import PatchCollection
from matplotlib.colors import LinearSegmentedColormap, ListedColormap, BoundaryNorm

def getPlayerShotChartDetail(player_name, season_id):
    # Get player information
    nba_players = players.get_players()
    player_dict = next((player for player in nba_players if player['full_name'] == player_name), None)
    if player_dict is None:
        raise ValueError(f"Player '{player_name}' not found.")

    # Get player career stats
    career_stats = playercareerstats.PlayerCareerStats(player_id=player_dict['id'])
    career_df = career_stats.get_data_frames()[0]

    # Filter career data by season_id
    filtered_career_df = career_df[career_df['SEASON_ID'] == season_id]
    if filtered_career_df.empty:
        raise ValueError(f"No data found for season ID '{season_id}'.")

    # Get team ID for the specified season
    team_id = filtered_career_df.iloc[0]['TEAM_ID']

    # Get shot chart data
    shot_chart = shotchartdetail.ShotChartDetail(team_id=int(team_id),
                                                 player_id=int(player_dict['id']),
                                                 season_type_all_star='Regular Season',
                                                 season_nullable=season_id,
                                                 context_measure_simple="FGA").get_data_frames()

    return shot_chart[0], shot_chart[1]

#basic court
def draw_court(ax=None, color="blue", lw=1, outer_lines=False):

    if ax is None:
        ax = plt.gca()

    # Basketball Hoop
    hoop = Circle((0,0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Backboard
    backboard = Rectangle((-30, -12.5), 60, 0, linewidth=lw, color=color)

    # The paint
    # outer box
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
    # inner box
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)

    # Free Throw Top Arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, fill=False)

    # Free Bottom Top Arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)

    # Restricted Zone
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)

    # Three Point Line
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, color=color)

    # list of court shapes
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw, bottom_free_throw, restricted, corner_three_a, corner_three_b, three_arc, center_outer_arc, center_inner_arc]

    #outer_lines=True
    if outer_lines:
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw, color=color, fill=False)
        court_elements.append(outer_lines)

    for element in court_elements:
        ax.add_patch(element)

#map for shots
def create_shot_chart(data, title="", color="b", xlim=(-250, 250), ylim=(422.5, -47.5), line_color="blue",
               court_color="white", court_lw=2, outer_lines=False,
               flip_court=False, gridsize=None,
               ax=None, despine=False):

    if ax is None:
        ax = plt.gca()

    if flip_court:
        xlim = xlim[::-1]
        ylim = ylim[::-1]

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.tick_params(labelbottom=False, labelleft=False)
    ax.set_title(title, fontsize=14)

    # draws the court using the draw_court()
    draw_court(ax, color=line_color, lw=court_lw, outer_lines=outer_lines)

    # separate color by make or miss
    missed_data = data[data['EVENT_TYPE'] == 'Missed Shot']
    made_data = data[data['EVENT_TYPE'] == 'Made Shot']

    # Plot missed shots
    miss = ax.scatter(missed_data['LOC_X'], missed_data['LOC_Y'], c='r', marker="x", s=300, linewidths=3)
    # Plot made shots
    make = ax.scatter(made_data['LOC_X'], made_data['LOC_Y'], facecolors='none', edgecolors='g', marker='o', s=100, linewidths=3)

    # Set the spines to match the rest of court lines, makes outer_lines
    # somewhat unnecessary
    for spine in ax.spines.values():
        spine.set_lw(court_lw)
        spine.set_color(line_color)

    if despine:
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
    #legend
    #ax.legend(handles=[make, miss], title='Legend', loc='upper left')


    return ax
def get_contributing_players(team_name, season):
    nbaTeams = teams.get_teams()
    team_info = next((team for team in nbaTeams if team['full_name'] == team_name), None)
    if team_info is None:
        raise ValueError(f"Team '{team_name}' not found.")
    team_id = team_info['id']
    team_roster = commonteamroster.CommonTeamRoster(team_id=team_id, season=season).get_data_frames()[0]
    playerIds=team_roster['PLAYER_ID'].tolist()
    filteredPlayers = []
    positions = []
    finalPPG = []
    for id in playerIds:
        currPlayerStats = playercareerstats.PlayerCareerStats(player_id=id).get_data_frames()[0]
        currSeasonStats = currPlayerStats[currPlayerStats['SEASON_ID'] == season]
        total_points = currSeasonStats['PTS'].sum()
        total_games = currSeasonStats['GP'].sum()
        ppg = total_points / total_games if total_games > 0 else 0
        if currSeasonStats['GP'].sum() > 41 and ppg > 5.0:
            filteredPlayers.append(players.find_player_by_id(id)['full_name'])
            positions.append(team_roster.loc[team_roster['PLAYER_ID'] == id, 'POSITION'].iloc[0])
            finalPPG.append(round(ppg,1))
    return filteredPlayers, positions, finalPPG

if __name__ == "__main__":
    if len(sys.argv) >= 4:
        team_name = ' '.join(sys.argv[1:-1])
        season_id = sys.argv[-1]

        roster, positions, ppg = get_contributing_players(team_name, season_id)
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
            axs[i].set_title(f"{player_name} ({positions[i]}) - PPG: {ppg}", fontsize=14, pad=10) 
            create_shot_chart(player_shotchart_df, title= axs[i].get_title(), ax=axs[i])
        for j in range(len(roster), rows * cols):
            axs[j].axis('off')

        # Adjust layout and show plot
        fig.suptitle(f"Shot Charts for {team_name} - Season {season_id}", fontsize=20, y=.98)  
        plt.tight_layout(rect=[0, 1, 1, 0.97])  
        plt.subplots_adjust(hspace=0.5)     
        plt.show()
    else:
        print("Please enter team name and season in format (e.g 2023-24)")