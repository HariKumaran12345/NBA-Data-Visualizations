# CSE6242DataVis_NBA_Visualizations

## Shot Map Instructions
Download all the required files under **Shot Map Visualizations**
### Individual Shot Map Creations (Non-Flask UI)
shotMap.py takes the following command line format to run properly: python shotMap.py (First Name Last Name of Player) (Season in the form (YYYY-YY)), f
for example you can run the file to find Lebron James's shotmap this past season by running **python shotMap.py Lebron James 2023-24**
The resulting output will show you the overarching makes and misses plotted with green circles and red X's respectively.

shotMapByTeam is similar except instead of the player name you can put a team name and it will show the shot maps for players who have played a certain number of games
and a certain number of points. An example command line instruction is **python shotMapByTeam Los Angeles Lakers 2023-24**

### Flask Shot Map Creations
You will need Flask for this (you can run pip install Flask in your terminal).
If you would like to use a web version you can simply run **python app.py** from within the directory, and then proceed to enter the season and team name on the local host page. Copy the URL generated in the terminal/command line and paste it in a browser (http://127.0.0.1:5000/)

## Player Score Prediction Instructions

1) Download all the required files
2) Navigate to Player Score Prediction directory on terminal/command line
3) run 'python app.py' - Make sure you have the right version of python (3.8 or higher and have flask, pandas, numpy installed)
4) Copy the URL generated in the terminal/command line and paste it in a browser (http://127.0.0.1:5000/)
5) Thats all!
