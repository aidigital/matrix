from main import sort_venues, sort_venues_combinations

# FOR THE VISUALIZATION, RUN THE: dash_develop.py script

# CHANGE THE DEFAULT VALUES OF THE PARAMETERS TO PRINT THE RESULTS IN THE CONSOLE
sort_venues(people_going_out=["John Davis", "Gary Jones", "Robert Webb", "Gavin Coulson", "Alan Allen", "Bobby Robson", "David Lang"],
            venues_open=["El Cantina", "Twin Dynasty", "Spice of life", "The Cambridge", "Wagamama", "Sultan Sofrasi", "Spirit House", "Tally Joe", "Fabrique"],
            explain_reason=False) # PLAY with TRUE/FALSE

sort_venues_combinations(
    people_going_out=["John Davis", "Gary Jones", "Robert Webb", "Gavin Coulson", "Alan Allen", "Bobby Robson", "David Lang"],
    venues_open=["El Cantina", "Twin Dynasty", "Spice of life", "The Cambridge", "Wagamama", "Sultan Sofrasi", "Spirit House", "Tally Joe", "Fabrique"],
    explain_reason=True) # PLAY with TRUE/FALSE