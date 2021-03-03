from src.data.data_fetcher import DataFetcher

fetcher = DataFetcher("2020", "P")
fetcher.api_starting_url_container
fetcher.gimmie_data(record_limit=500)
fetcher.save_df_data() 