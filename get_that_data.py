import json
import urllib.request
import pandas as pd
import time

# Create a list of lists where each transaction will be one list
complete_list = []

# Set count for pages
big_count = 0
little_count = 0


api_url = "https://api.open.fec.gov/v1/schedules/schedule_a/?"

def make_api_url(api_url):
    '''
        Description:
            Build the starting_url to get campaign donation receipt data of individual's donations for a two year time period.

        Parameters:
            Argument:
                api_url -- FEC api endpoint, schedules/schedule_a denotes campaign donation receipt data.
            
            
            USER INPUT:
            api_key -- DEMO_KEY can be used to DEMO API, to obtain API key visit: https://api.open.fec.gov/developers/#/
            two_year_transaction_period -- This is a two-year period that is derived from the year a transaction took place, if you want an odd-number year enter the following even-numbered year. i.e. want 2019, enter 2020.
            recipient_committee_type -- The one-letter type code of the office the political campaign was for: (H = House) (S = Senate) (P = Presidential).
            

        Returns:
            A URL string for either House, Senate, or Presidential political campaigns from a specified two year period. 
    '''

    set_parameters = "&sort=-contribution_receipt_date&sort_hide_null=true&sort_null_only=false&is_individual=true&contributor_type=individual&per_page=100"

    api_key = input("Enter API key or press enter for DEMO_KEY: ")
    
    if len(api_key) < 1:
        api_key = "DEMO_KEY"
    

    two_year_transaction_period = input("Enter even numbered year between 2000 and 2020: ")

    if two_year_transaction_period.isnumeric():
        if (int(two_year_transaction_period) % 2) == 0:
            if int(two_year_transaction_period) >= 2000 and int(two_year_transaction_period) <= 2020:
                pass
            else:
                two_year_transaction_period = "2020"
                print("Invalid input, defaulting to 2020.")
        else:
            two_year_transaction_period = "2020"
            print("Invalid input, defaulting to 2020.")
    else:
        two_year_transaction_period = "2020"
        print("Invalid input, defaulting to 2020.")

    
    recipient_committee_type = input("Enter H for House, S for Senate, or P for Presidential donations transactions: ")

    if recipient_committee_type == "H" or recipient_committee_type == "House":
        recipient_committee_type = "H"
    elif recipient_committee_type == "S" or recipient_committee_type == "Senate":
        recipient_committee_type = "S"
    elif recipient_committee_type == "P" or recipient_committee_type == "Presidential":
        recipient_committee_type = "P"
    else:
        print("Invalid input, defaulting to Presidential")
        recipient_committee_type = "P"

    starting_url = api_url + "two_year_transaction_period=" + two_year_transaction_period + "&api_key=" + api_key + "&recipient_committee_type=" + recipient_committee_type + set_parameters
    return starting_url

def total_pages(starting_url):

    '''
        Description:   
            Preforms a get request on starting_url
            returns integer with the total number of pages
            depending on the results per page in starting_url.
            Replaces last two digits with 00 to allow clean looping later.

        Parameters: 
            starting_url is a Get request starting with 
            https://api.open.fec.gov/v1/schedules/schedule_a/?api_key=DEMO_KEY
       
        Returns:
            Pages -- an interger of pages remaining of starting_url
    '''
    
    uh = urllib.request.urlopen(starting_url)
    data = uh.read().decode()
    info = json.loads(data)
    # Yes this is ridiculous but whatever
    pages = info["pagination"]["pages"]
    pages = pages[:-3]
    pages = pages + "000"
    pages = int(pages)
    return pages



class data_fetcher:
    """
        It's big and ugly but it does the job.

        Description:
            Contains two functions, get_next_page and get_transactions on page, 
            the former gets the next page the latter gets all the transactions on a page.
        
        Parameters:
            starting_url -- This url is made using make_api_url() 
            complete_list -- Is an empty list that will be filled with lists. The lists each contain one transactions data.

        Returns:
            complete_list is returned after getting all transactions from a page.

    """

    def __init__(self, starting_url, complete_list):
        self.starting_url = starting_url
        self.complete_list = complete_list

    def get_next_page(self):
        """
            Adds two items to starting_url to get to the next page of transactions.

            Description:
                Takes the starting_url and concatenates last_index and last_contribution_receipt_date
                to get the next page of transactions.
        """
        
        try:
            url = self.starting_url + "&last_index=" + self.last_index + "&last_contribution_receipt_date=" + self.last_contribution_receipt_date
        except:
            url = self.starting_url
        uh = urllib.request.urlopen(url)
        data = uh.read().decode()
        self.info = json.loads(data)
        

    def get_transactions_on_page(self):
        """
            Loops over the transactions on a page using self.info from get_next_page.
            Puts that data into current_list.
            Puts current_list into complete_list.
            Gets last_index and last_contribution_receipt_date to pass to get_next_page.
            Returns complete_list with transactions from page.
        """
        # Pull out the data we want from each transaction on a page and add it to the complete_list
        for item in self.info["results"]:
            party = item["committee"]["party"]
            contributor_occupation = item["contributor_occupation"]
            contributor_employer = item["contributor_employer"]
            contributor_city = item["contributor_city"]
            contributor_state = item["contributor_state"]
            contributor_zip = item["contributor_zip"]
            # Because there is stupid data in some transactions for ZIP, need to do this for all data to process for bad data
            try:
                if contributor_zip.isnumeric():
                    contributor_zip = int(contributor_zip)
                else:
                    contributor_zip = int("00000")
            except:
                contributor_zip = int("00000")
            current_list = [contributor_occupation, contributor_employer, contributor_city, contributor_state, contributor_zip, party]
            self.complete_list.append(current_list)
        self.last_index = self.info["pagination"]["last_indexes"]["last_index"]
        self.last_contribution_receipt_date = self.info['pagination']["last_indexes"]["last_contribution_receipt_date"]
        return self.complete_list
        



class get_the_data:
    """
        Loops over as many pages as you would like

        Description:
            more_data loops through 1000 pages
            gimmie_data makes sure API request limit isn't exceeded

        Parameters:
            data_fetcher -- The instance of data_fetcher() initialized before calling get_the_data()

        Returns: 
            Nearly all the pages of data in complete_list

        Special Note:
            To test change 1000 in more_data and 1000 in (if little_count ==) in gimmie_data to same number
            and replace (total_pages(starting_url)/1000) and time.sleep in gimmie_data
    """

    def __init__(self, data_fetcher):
        self.data_fetcher = fec
        self.little_count = 0
        self.big_count = 1

    def more_data(self):
        """
            more_data loops through 1000 pages of transactions.
            That is the maximum get requests allowed per hour.
        """
        while self.little_count < 1000:
            fec.get_next_page()
            fec.get_transactions_on_page()
            print(self.little_count)
            self.little_count += 1
            
            


    def gimmie_data(self):
        """
            gimmie_data does it all.
            big_count keeps track of how many times more_data is ran.
            Checks how many pages there are using total_pages(). 
            Divided by the 1000 pages more_data() loops through per hour.
            
            When little_count is 1000,
            starts a clock to wait one hour,
            resets little_count to 1,
            then keeps going until all pages are looped through.
        """
        while self.big_count < (total_pages(starting_url)/1000):
            self.big_count += 1
            if self.little_count == 1000:
                print("waiting 1 hour")
                time.sleep(3600)
                self.little_count = 1
                self.more_data()
            else:
                self.more_data()

# This was a crazy project!

# Sets starting_url
starting_url = make_api_url(api_url)

# Create instance of data_fetcher class class
fec = data_fetcher(starting_url, complete_list)

# Inizialize get_the_data to work
work = get_the_data(fec)

# Starts looping over all transactions
work.gimmie_data()

# Once complete_list has all transaction we create a pandas dataframe 
df = pd.DataFrame(complete_list, columns = ['contributor_occupation', 'contributor_employer', 'contributor_city', 'contributor_state', 'contributor_zip', 'party']) 

# Saves DataFrame as serialized object, will import this to ML program
# Add path and uncommet to save pickled data
#df.to_pickle("./pickled_data.pkl")

# Prints DataFrame, be careful, this can get bigggggg
print(df)

# Thanks for reading my Ted Talk
