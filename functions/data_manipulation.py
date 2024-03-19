import pandas as pd
import os
import matplotlib.pyplot as plt
from functions.pitch_plot import drawpitch
import seaborn as sns

# add binary for adding shot/pass stats on viz

def get_pass_stats():
    x=1
    
    return x
    
    # given a df of passes get stats on passes etc.

def get_shot_stats():
    x=1
    
    return x
    
    # given a df of shots get stats on xg, goals, R/L/H etc


def plot_events(team_matches_df,
                team, 
                player,
                event_type,
                heatmap,
                color):
    
    player_events = team_matches_df[(team_matches_df["team_name"] == team)&
                              (team_matches_df["player_name"] == player)&
                              (team_matches_df["type_name"] == event_type)]
    
    fig,ax = plt.subplots(figsize=(12,8))
    
    drawpitch(ax, 
              measure='SB',
              orientation="horizontal",
              facecolor="white",
              linecolor="0.1",
              lw = 1.5,
              x_offset = [1,1],
              y_offset = [1,1]) 
    
    plt.scatter(player_events['location_x'],
                player_events['location_y'],
                color=color,
                s=50,
                ec="0.1",
                lw=1.5,
                alpha=0.8
                ,zorder=2)
    
    plt.title(f"{player} | {team} | {len(player_events)} {event_type} events",
              fontsize=16)
    
    if heatmap:
    
        sns.kdeplot(x=player_events['location_x'],
                    y=player_events['location_y'],
                    shade=True,n_levels=40,zorder=1)
        
    plt.ylim(80,0)
    plt.axis("off")
    plt.tight_layout()
    plt.show()
    
    return player_events

def get_lineup_info(lineup_path, match_id):
    
    lineup_df = pd.read_json(f"{lineup_path}/{match_id}.json")

    lineup_info = {}
    
    for (n, team_name) in enumerate(lineup_df.team_name):
        
        lineup_info[team_name] = pd.DataFrame(lineup_df.iloc[n]["lineup"])
    
    return lineup_info

def get_multi_match_df(match_path, match_ids):
    
    multi_match_df = pd.DataFrame({})

    for match in match_ids:
        
        match_df = pd.read_json(f"{match_path}/{match}.json")
        
        match_df = expand_single_match_df(match_df)
        match_df["match_id"] = match
        
        multi_match_df = pd.concat([multi_match_df, match_df])
        
    return multi_match_df

def get_match_info(match_id, matches_df):
    
    match_details = matches_df[matches_df["match_id"] == match_id].iloc[0].to_dict()
    
    match_details["home-away"] = match_details["home_team_name"] +\
        " - " + match_details["away_team_name"]
        
    match_details["final_score"] = match_details["home_score"] + "-" + match_details["away_score"]

    return match_details

def expand_single_match_df(match_df):
    
    # expand nested cols for dict only cols
    for i in list(match_df):
        
        # find which are just dicts
        col_value_types = list(set([type(i) for i in match_df[i].tolist()]))
        
        if dict in col_value_types:
            
            expanded_col = pd.json_normalize(match_df[i])
            
            expanded_col.columns = [f"{i}_{j}" for j in list(expanded_col)]
            
            expanded_col['id'] = match_df['id']
            
            match_df = match_df.merge(expanded_col, on="id")
            
        else:
            
            pass
        
    for i in list(match_df):
        
        if "location" in i:
            
            loc_df = match_df[[i,"id"]].dropna()
            
            new_col_names = [f"{i}_{n}" for n in ["x","y","z"]]
            
            expanded_loc_column = loc_df[i].apply(pd.Series)
            
            loc_df[new_col_names[:len(list(expanded_loc_column))]] = expanded_loc_column
            
            del loc_df[i]
    
            match_df = match_df.merge(loc_df, how="left", on="id")    
            
    return match_df

def get_team_matches_df(team, matches_df):
    
    team_matches = matches_df[(matches_df["home_team_name"] == team)|
                          (matches_df["away_team_name"] == team)]
    
    return team_matches

def get_comp_info(comp_df_path, comp_name, season):
    
    """
    Retrieves information about a specific competition and season from a DataFrame read from a JSON file.

    Parameters:
    comp_df_path (str): File path to the JSON file containing information about competitions.
    comp_name (str): Name of the competition.
    season (str): Name of the season.

    Returns:
    tuple: A tuple containing the competition ID and season ID.

    """
    # Check if comp_df_path is a string
    if not isinstance(comp_df_path, str):
        raise TypeError("Input 'comp_df_path' must be a string.")

    if not os.path.exists(comp_df_path):
        raise FileNotFoundError(f"File not found at: {comp_df_path}")

    if not isinstance(comp_name, str) or not isinstance(season, str):
        raise TypeError("comp_name and season must be provided as strings.")

    comp_df = pd.read_json(comp_df_path)

    selected_comp_info = comp_df[(comp_df["competition_name"] == comp_name) & 
                                 (comp_df["season_name"] == season)]

    if selected_comp_info.empty:
        raise KeyError(f"No match found for the competition '{comp_name}' and season '{season}'.")

    if len(selected_comp_info) > 1:
        raise KeyError("Multiple matches found for the competition name and season. Unable to proceed.")

    selected_comp_info = selected_comp_info.iloc[0].to_dict()

    comp_id = selected_comp_info.get("competition_id")
    season_id = selected_comp_info.get("season_id")

    if comp_id is None or season_id is None:
        raise KeyError("Invalid column names in the DataFrame for competition or season.")

    return comp_id, season_id


def get_comp_info(comp_df_path, comp_name, season):
    
    comp_df = pd.read_json(comp_df_path)

    selected_comp_info = comp_df[(comp_df["competition_name"] == comp_name)
                            &(comp_df["season_name"] == season)].iloc[0].to_dict()
    
    comp_id, season_id = selected_comp_info["competition_id"],\
                         selected_comp_info["season_id"]

    return (comp_id, season_id)

def get_matches_df(matches_df_path, comp_id, season_id):
    
    """
    Reads a JSON file containing match data, normalizes it into a DataFrame, and adds a column 
    indicating the home-away team combination.

    Parameters:
    matches_df_path (str): File path to the JSON file containing match data.
    comp_id (int): ID of the competition.
    season_id (int): ID of the season.

    Returns:
    pandas.DataFrame: DataFrame containing the normalized match data with an additional column 
                      indicating the home-away team combination.

    """
    
    # Check if matches_df_path exists
    if not os.path.exists(matches_df_path):
        raise FileNotFoundError(f"File not found at: {matches_df_path}")

    # Check if comp_id and season_id are integers
    if not isinstance(comp_id, int) or not isinstance(season_id, int):
        raise ValueError("comp_id and season_id must be integers.")
                     
    matches_df = normalise_df(pd.read_json(matches_df_path))

    matches_df["home-away"] = matches_df["home_team_name"] + "-" + matches_df["away_team_name"]
    
    return matches_df

def normalise_df(matches_df):
    
    """
    Normalizes a DataFrame containing nested dictionaries into a flat DataFrame.

    Parameters:
    matches_df (pandas.DataFrame): DataFrame containing nested dictionaries.

    Returns:
    pandas.DataFrame: Normalized DataFrame with flattened nested dictionaries.
    
    """
    
    # Check if matches_df is a DataFrame
    if not isinstance(matches_df, pd.DataFrame):
        raise TypeError("Input 'matches_df' must be a pandas DataFrame.")

    for i in list(matches_df):

        if type(matches_df[i].tolist()[0]) == dict:
            
            new_cols = pd.json_normalize(matches_df[i])
        
            new_col_names = list(matches_df[i].tolist()[0].keys())
            
            matches_df = pd.concat(
                    [
                        matches_df,
                        pd.DataFrame(
                            new_cols, 
                            index=matches_df.index, 
                            columns=new_col_names
                        )
                    ], axis=1
                )
            
            del matches_df[i]
            
        else:
            
            pass
        
    return matches_df