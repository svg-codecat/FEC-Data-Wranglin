from src.data.data_fetcher import DataFetcher



fetcher = DataFetcher("2020", "P")
print(fetcher.api_starting_url_container)
print(fetcher.gimmie_data(record_limit=5))


#### Need to write this into the other file

# Create instance of data_fetcher class class
# fec = data_fetcher(starting_url, complete_list)

# # Inizialize get_the_data to work
# work = get_the_data(fec)

# # Starts looping over all transactions
# work.gimmie_data()

# # Once complete_list has all transaction we create a pandas dataframe
# df = pd.DataFrame(
#     complete_list,
#     columns=[
#         "contributor_occupation",
#         "contributor_employer",
#         "contributor_city",
#         "contributor_state",
#         "contributor_zip",
#         "party",
#     ],
# )

# Saves DataFrame as serialized object, will import this to ML program
# Add path and uncommet to save pickled data
# df.to_pickle("./pickled_data.pkl")

# Prints DataFrame, be careful, this can get bigggggg
# print(df)

# Thanks for reading my Ted Talk