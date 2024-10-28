"""Utils functions module"""
import pandas as pd


def map_languages_to_color_list(languages_color_palette: dict, proficiencies_top_10: pd.Series) -> list:
    """Map values from dictionary to palette color list, given a pandas series used as index

    Args:
        languages_color_palette (dict): key-value pair that associate language-color
        proficiencies_top_10 (pd.Series): top ten languages list

    Returns:
        list: a list of colors based on the series of languages 
    """
    return [languages_color_palette[proficiencies_top_10.index[i]] for i in
            range(len(proficiencies_top_10))]
