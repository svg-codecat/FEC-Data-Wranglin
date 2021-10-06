from src.data.data_fetcher import DataFetcher

fetcher = DataFetcher("2020", "P", None, "IA", "Sioux City")
fetcher.api_starting_url_container
fetcher.gimmie_data(record_limit=100)
fetcher.save_df_data() 