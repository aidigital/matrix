import json
import requests
from pprint import pprint
from collections import defaultdict
import pandas as pd

# READING THE DATA FROM GITHUB
# url_users = 'https://raw.githubusercontent.com/aidigital/matrix/master/people_venues_json/users.json'
# url_venues = 'https://raw.githubusercontent.com/aidigital/matrix/master/people_venues_json/venues.json'
#
# read_users = requests.get(url_users)
# list_of_users_dicts = json.loads(read_users.text)
#
# read_venues = requests.get(url_venues)
# list_of_venues_dicts = json.loads(read_venues.text)

# READING THE DATA FROM LOCAL MACHINE (FASTER)
url_users = 'C:/AI Python Play/Project_Play/users.json'
url_venues = 'C:/AI Python Play/Project_Play/venues.json'

with open(url_users) as file_open:
    list_of_users_dicts = json.load(file_open)

with open(url_venues) as file_open:
    list_of_venues_dicts = json.load(file_open)


def sort_venues(people_going_out, venues_open, explain_reason=True, returned_message='applicable_venues_message', return_reasons_dataframe=False):
    dict_inapplicable_venues = defaultdict(list)

    # MAIN LOGIC
    for user_dict in list_of_users_dicts:
        if user_dict['name'] in people_going_out:
            this_person_drinks = list(map(lambda x: x.upper(), user_dict['drinks']))
            this_person_doesnt_eat = list(map(lambda x: x.upper(), user_dict['wont_eat']))

            for venue_dict in list_of_venues_dicts:
                if venue_dict['name'] in venues_open:
                    venue_drinks_menu = [x.upper() for x in venue_dict['drinks']] # alternative syntax for uppercase (list comprehension)
                    venue_food_menu = [x.upper() for x in venue_dict['food']]

                    if len(set(this_person_drinks).intersection(venue_drinks_menu) ) == 0:
                        dict_inapplicable_venues[venue_dict['name']].append("No drink for "+user_dict['name'])

                    if len([food for food in venue_food_menu if food not in this_person_doesnt_eat]) == 0:
                        dict_inapplicable_venues[venue_dict['name']].append("No food for " + user_dict['name'])

    #OUTPUT
    inapplicable_venues_message = ' '.join(["There are", str(len(dict_inapplicable_venues.keys())), "inapplicable venues:",', '.join(dict_inapplicable_venues.keys())])
    df_inapplicable_venues = pd.DataFrame([[k, ele] for k, v in dict_inapplicable_venues.items() for ele in v]).rename(columns={0: "Inapplicable Venue", 1: "Reason"})
    if explain_reason is False:
        print(inapplicable_venues_message)

    else:
        print("\nThere are", len(dict_inapplicable_venues.keys()), "inapplicable venues:")
        #df_inapplicable_venues = pd.DataFrame.from_dict(dict_inapplicable_venues, orient='index') # easier alternative of displaying results
        pprint(df_inapplicable_venues)

    applicable_venues = [venue for venue in venues_open if venue not in dict_inapplicable_venues.keys()]
    applicable_venues_message = ' '.join(["There are", str(len(applicable_venues)), "applicable venues:", ', '.join(applicable_venues)])
    print(applicable_venues_message, "\n-----")

    if return_reasons_dataframe==True:
        return df_inapplicable_venues
    else:
        display_message = applicable_venues_message if returned_message == 'applicable_venues_message' else inapplicable_venues_message
        return display_message

# LIST ALL POSSIBLE COMBINATIONS OF PEOPLE GOING OUT
def sort_venues_combinations(people_going_out, venues_open, explain_reason=False):
    print("\n LIST ALL COMBINATIONS\n")
    i = 1
    import itertools
    for length in range(1, len(people_going_out)+1):
        for subset in itertools.combinations(people_going_out, length):
            print(i)
            print(list(subset))
            sort_venues(people_going_out=subset,
                        venues_open=venues_open,
                        explain_reason=explain_reason # True -> Tells Why A Venue Cannot Be Attended
            )
            i = i+1

if __name__ == "__main__":
    sort_venues(people_going_out=["John Davis", "Gary Jones", "Robert Webb", "Gavin Coulson", "Alan Allen", "Bobby Robson", "David Lang"],
                venues_open=["El Cantina", "Twin Dynasty", "Spice of life", "The Cambridge", "Wagamama", "Sultan Sofrasi", "Spirit House", "Tally Joe", "Fabrique"],
                explain_reason=True)

    sort_venues_combinations(people_going_out=["John Davis", "Gary Jones", "Robert Webb", "Gavin Coulson", "Alan Allen", "Bobby Robson", "David Lang"],
                 venues_open=["El Cantina", "Twin Dynasty", "Spice of life", "The Cambridge", "Wagamama", "Sultan Sofrasi", "Spirit House", "Tally Joe", "Fabrique"],
                 explain_reason=True)