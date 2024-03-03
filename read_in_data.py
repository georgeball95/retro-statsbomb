import pandas as pd

comp_path = "data/competitions.json"

comp_df = pd.read_json(comp_path)

#def get_competition_details(comp_name,season,comp_df):
    
comp_name = "Premier League"
season = "2015/2016"
    
selected_comp_info = comp_df[(comp_df["competition_name"] == comp_name)
                        &(comp_df["season_name"] == season)].iloc[0].to_dict()

comp_id, season_id = selected_comp_info["competition_id"],\
                     selected_comp_info["season_id"]
                     
matches_df_path = f"data/matches/{comp_id}/{season_id}.json"
matches_df = pd.read_json(matches_df_path)

