from src.data.data_fetcher import DataFetcher

fetcher = DataFetcher("2020", "P")
fetcher.api_starting_url_container
fetcher.gimmie_data(record_limit=50000)
fetcher.save_df_data() 