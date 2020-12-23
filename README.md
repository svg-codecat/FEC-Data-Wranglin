# FEC-Data-Wranglin
`get_that_data.py` pulls data from FEC API
`clean_that_data.py` finds duplicate values from the same column using [TF-IDF](https://en.wikipedia.org/wiki/Tf–idf)
    i.e. "Not Employeed" is replaced by "Not Employed" or "Apple INC" is replaced with "Apple"
 
If you want to make more than a handful of requests you need an api_key, visit [fec.gov](https://api.open.fec.gov/developers/#/) to get a key. 
***Set your api_key as an environment variable.*** 
i.e. `FEC_API_KEY=DEMO_KEY`
		 
## When you run `python3 get_that_data.py` in the terminal:

Resulting data will be saved in a csv in `FEC-Data-Wranglin/data/raw_data` and will be structured as seen below.

Each row contains the information of one donation, the first five columns reference the contributor's information and party is the party of the candidate they donated to.

|   | contributor_occupation | contributor_employer   | contributor_city | contributor_state | contributor_zip | party | 
|---|------------------------|------------------------|------------------|-------------------|-----------------|-------| 
| 0 | RETIRED                | RETIRED                | BENTON           | AR                | 72019           | OTH   | 
| 1 | SYSTEMS MANAGER        | AVANIR PHARMACEUTICALS | ALISO VIEJO      | CA                | 92656           | OTH   | 
| 2 | RETIRED                | RETIRED                | OSHKOSH          | WI                | 549048984       | OTH   | 
| 3 | INSURANCE REP          | BRS FINANCIAL GROUP    | FRESNO           | CA                | 93701           | IND   | 
| 4 | EDITOR                 | GLOBAL FINANCE MEDIA   | GREENLAWN        | NY                | 11740           | OTH   | 
| 5 | FALSE                  | FORMATIV HEALTH        | HOOSICK FALLS    | NY                | 12090           | OTH   | 




## After gathering your data you can try to clean it up a little. 

The process I have used for cleaning the data can be found [here](https://bergvca.github.io/2017/10/14/super-fast-string-matching.html)

### The more data you have the better the cleaning will work!

Run `python3 clean_that_data.py` after `python3 get_that_data.py`.

You can change the how many times a file is 'cleaned' by adding or removing this line to the `if` statement in `clean_that_data.py`:

`return_df_as_csv(build_classes(csv, lowest_similarity, ngram_size), saved_file_name)`

***csv*** -- `data/raw_data/` `.csv` -- File you want to clean. It must be a `.csv` and must be in `data/raw_data/`

***lowest_similarity*** -- `float` between 0 and 1 -- similarity threshold between two values in a column, values with similarity greater than `lowest_similarity` will become the same value.

***ngram_size*** -- `int` (ideally between 2 and 4) -- size of character chunks used to assess similarity.
i.e. ngram_size of 3 for `similarity`: `' si' 'sim' 'imi' 'mil' 'ila' 'lar' 'ari' 'rit' 'ity' 'ty '`