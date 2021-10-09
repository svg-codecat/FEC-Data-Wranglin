from src.data.data_fetcher import DataFetcher

fetcher = DataFetcher("2020", "A", "51106", "IA", "Sioux City")
fetcher.api_starting_url_container
fetcher.gimmie_data()
fetcher.save_df_data() 