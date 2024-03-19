import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from functions.data_manipulation import get_comp_info,\
                                        get_matches_df,\
                                        get_team_matches_df,\
                                        expand_single_match_df,\
                                        get_match_info,\
                                        get_multi_match_df,\
                                        normalise_df,\
                                        get_lineup_info,\
                                        plot_events

comp_id, season_id = get_comp_info("data/competitions.json",
                                   "Premier League",
                                   "2015/2016")

#get dataframe of all matches in competition season
matches_df = get_matches_df(f"data/matches/{comp_id}/{season_id}.json",
                            comp_id,
                            season_id)

#filter dataframe for a team's matches
team_matches = get_team_matches_df("Leicester City", matches_df)
match_ids = team_matches.match_id.tolist()

all_matches = get_multi_match_df("data/events",
                                 match_ids)

player_events = plot_events(all_matches,
                            "Leicester City",
                            "Robert Huth",
                            "Shot",
                            color="blue",
                            heatmap=False)

#add env file
#move plotting into another file
#to do
#add sb logo in code
#speed of attack?
#extend kde to full pitch?
#split into grid
# add match info - date, score
# add stats on under pressure/completed/
#arrows
# complete
#most common receiptient
#r/l/other
#heatmaps
#convex hull
#possession chains
#streamlit?

    


    
    
    
    
    
    
    
    
            
            