from src.data.clean_data import return_df_as_csv, build_classes
import os
import fnmatch


path_pattern = "*.csv"
files = os.listdir("data/raw_data/")
for csv in files:
    if fnmatch.fnmatch(csv, path_pattern):
        return_df_as_csv(build_classes(csv, .95, 3), "cleaned_" + csv)
        return_df_as_csv(build_classes(csv, .9, 3), "deep_cleaned_" + csv)
        return_df_as_csv(build_classes(csv, .8, 3), "badly_cleaned_" + csv)

