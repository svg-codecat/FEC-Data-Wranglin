# FEC-Data-Wranglin
get_that_data.py pulls data from FEC API to use later on ML project. 

 
If you want to make more than a handful of requests you need an api_key, visit https://api.open.fec.gov/developers/#/ to get a key. Set your api_key as an environment variable. i.e. `FEC_API_KEY=DEMO_KEY`
		 
Run `python3 get_that_data.py` in the terminal

Resulting data will be saved in a csv in `FEC-Data-Wranglin/data/` and will be structured as seen below.

Each row contains the information of one donation, the first five columns reference the contributor's information and party is the party of the candidate they donated to.

|   | contributor_occupation | contributor_employer   | contributor_city | contributor_state | contributor_zip | party | 
|---|------------------------|------------------------|------------------|-------------------|-----------------|-------| 
| 0 | RETIRED                | RETIRED                | BENTON           | AR                | 72019           | OTH   | 
| 1 | SYSTEMS MANAGER        | AVANIR PHARMACEUTICALS | ALISO VIEJO      | CA                | 92656           | OTH   | 
| 2 | RETIRED                | RETIRED                | OSHKOSH          | WI                | 549048984       | OTH   | 
| 3 | INSURANCE REP          | BRS FINANCIAL GROUP    | FRESNO           | CA                | 93701           | IND   | 
| 4 | EDITOR                 | GLOBAL FINANCE MEDIA   | GREENLAWN        | NY                | 11740           | OTH   | 
| 5 | FALSE                  | FORMATIV HEALTH        | HOOSICK FALLS    | NY                | 12090           | OTH   | 


