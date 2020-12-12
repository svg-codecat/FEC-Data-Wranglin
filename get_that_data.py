from src.data.data_fetcher import DataFetcher

fetcher = DataFetcher("2010", "S")
fetcher.api_starting_url_container
fetcher.gimmie_data(record_limit=4)
fetcher.save_df_data() 