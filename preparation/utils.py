import pandas as pd


def map_languages_to_color_list(languages_color_palette: dict, s_2011_proficiencies_top_10: pd.Series) -> list[str]:
    # mapping values from dictionary to palette color list to be fed to plot bar code
    return [languages_color_palette[s_2011_proficiencies_top_10.index[i]] for i in
            range(len(s_2011_proficiencies_top_10))]


