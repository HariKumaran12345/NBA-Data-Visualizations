# NBA Visualizations
Our package comprises several innovative components aimed at enhancing insights into NBA player performance and game outcomes for a variety of audiences.

## DESCRIPTION
### Linear Regression Predictions:
We've implemented Linear Regression to forecast player performance for upcoming seasons. This method not only enhances visualization but also offers predictive insights, allowing stakeholders to anticipate future player potential. The backend, powered by a Python Flask server, handles data requests and serves predictive models based on player metrics. The frontend visualization, built using Plotly.js, dynamically updates to display player performance over seasons, distinguishing future predictions with dashed lines. This interactive visualization empowers users to make informed decisions based on predicted player performance.

### Table Model: 
Leveraging Linear Regression on ELO data, we've achieved a 69% accuracy in binary classification (Winner/Loser). Using D3, we've created a visualization showing predicted Margin of Victory (MOV) for all possible team matchups. Additionally, users can select specific teams to focus on, enhancing usability.

### Player Clustering: 
We've employed K-means clustering on RAPTOR scores and relevant player metrics to categorize NBA players into distinct groups based on playing styles and skill sets. The frontend presents cluster assignments, statistics, and visualizations using matplotlib, enabling users to understand player roles and team compositions better. This approach enhances traditional clustering methods by incorporating advanced performance metrics.

### Shot Map Visualizations: 
We've expanded shot map visualizations to show player shot distributions on a team-by-team basis. These shot maps provide essential information in a simple format, allowing casual fans to understand offensive schemes easily. By filtering players based on game participation and scoring criteria, and utilizing the NBA API, we've constructed shot maps hosted on Flask-powered front-end templates.

## INSTALLATION
1. Clone the repostiroy:
git clone https://github.gatech.edu/hkumaran3/CSE6242DataVis_NBA_Visualizations.git
2. Navigate to the project directory:
cd '.\CODE\Clustering Visualization\'
3. Install dependencies
pip install -r requirements.txt

## EXECUTION
1. Run the Flask server:
python app.py
2. Navigate to http://127.0.0.1:5000/ on your browser
