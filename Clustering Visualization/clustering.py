#imports
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score

def cluster(year):
    data = pd.read_csv('../dataset/modern_RAPTOR_by_team.csv')
    year = int(year)

    #choose season, for now latest season
    data = data[data.season == year]
    data.dropna(inplace=True)

    features = ['raptor_box_offense', 'raptor_box_defense', 'raptor_onoff_offense', 'raptor_onoff_defense', 'predator_offense',
            'predator_defense', "pace_impact"]
    
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data[features])

    k = 3

    kmeans = KMeans(n_clusters=k, random_state=42)
    clusters = kmeans.fit_predict(scaled_data)

    # Add clusters to the original dataframe
    data['cluster'] = clusters

    numeric_data = data.select_dtypes(include=np.number)

    # Analyze clusters
    cluster_stats = numeric_data.groupby('cluster').mean()
    #print(cluster_stats)

    # Visualize clusters using PCA
    pca = PCA(n_components=2)
    pca_data = pca.fit_transform(scaled_data)

    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=pca_data[:, 0], y=pca_data[:, 1], hue=clusters, palette='viridis')
    plt.title('PCA Visualization of Clusters')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.legend(title='Cluster')
    plt.show()

        # Perform t-SNE dimensionality reduction
    tsne = TSNE(n_components=2, random_state=42)
    tsne_data = tsne.fit_transform(scaled_data)

    # Plot t-SNE visualization with cluster labels
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=tsne_data[:, 0], y=tsne_data[:, 1], hue=clusters, palette='viridis', legend='full')
    plt.title('t-SNE Visualization of Clusters')
    plt.xlabel('t-SNE Component 1')
    plt.ylabel('t-SNE Component 2')
    plt.legend(title='Cluster')
    plt.show()

    cluster_names = assign_cluster_names(cluster_stats)

    # Add cluster names to the cluster statistics dataframe
    cluster_stats['cluster_name'] = cluster_names

    # Print cluster statistics along with assigned names
    print(cluster_stats)



def assign_cluster_names(cluster_stats):
    cluster_names = []
    
    # Calculate the difference between defensive and offensive RAPTOR scores for each cluster
    cluster_stats['raptor_difference'] = cluster_stats['raptor_defense'] - cluster_stats['raptor_offense']
    
    # Find the index of the cluster with the greatest difference (most defensive)
    most_defensive_cluster_idx = cluster_stats['raptor_difference'].idxmax()
    
    # Find the index of the cluster with the least difference (most offensive)
    most_offensive_cluster_idx = cluster_stats['raptor_difference'].idxmin()
    
    # Find the index of the remaining cluster
    balanced_cluster_idx = cluster_stats.index[~cluster_stats.index.isin([most_defensive_cluster_idx, most_offensive_cluster_idx])][0]
    
    # Label clusters as offensive, defensive, or balanced
    for idx in cluster_stats.index:
        if idx == most_offensive_cluster_idx:
            cluster_names.append("Offensive Powerhouses")
        elif idx == most_defensive_cluster_idx:
            cluster_names.append("Defensive Specialists")
        elif idx == balanced_cluster_idx:
            # Determine whether the balanced cluster leans towards offense or defense
            if cluster_stats.loc[idx, 'raptor_offense'] > cluster_stats.loc[idx, 'raptor_defense']:
                cluster_names.append("Balanced Players (leaning towards offense)")
            elif cluster_stats.loc[idx, 'raptor_defense'] > cluster_stats.loc[idx, 'raptor_offense']:
                cluster_names.append("Balanced Players (leaning towards defense)")
            else:
                cluster_names.append("Balanced Players (neutral)")
    return cluster_names

def get_players_in_clusters_grouped_by_team(data):
    players_in_clusters = {}
    for cluster_label in data['cluster'].unique():
        players_in_clusters[cluster_label] = data[data['cluster'] == cluster_label].groupby('team')['player_name'].apply(list).to_dict()
    return players_in_clusters

def get_player_cluster(player_name, data, cluster_stats):
    # Check if the player is in the dataset
    if player_name in data['player_name'].values:
        # Get the cluster label for the player
        player_cluster = data.loc[data['player_name'] == player_name, 'cluster'].values[0]
        # Get the cluster name from cluster_stats
        cluster_name = cluster_stats.loc[player_cluster, 'cluster_name']
        return player_cluster, cluster_name
    else:
        return None, None