# INPUT: WHO IS GOING OUT
people_going_out <- c("John Davis", "Gary Jones", "Robert Webb", "Gavin Coulson" ,"Alan Allen", "Bobby Robson", "David Lang")
people_going_out <- lapply(people_going_out, toupper)

# INSTALL THESE LIBRARIES & LOAD THEM
#install.packages("jsonlite")
#install.packages("data.table")
#install.packages("dplyr")
library(jsonlite); library(data.table); library(dplyr)

# READ THE  FILES
users_file <- "C:/Users/adrian.iordache/Desktop/Users to Restaurants/JSON Files/users.json"
users_data <- fromJSON(paste(readLines(users_file), collapse=""))
users <- data.table(users_data)
users_list <- sapply( as.list( as.data.frame(users)[,1]), toupper) #everything is converted to uppercase (otherwise, Soft drinks <> Soft Drinks)  

venues_file <- "C:/Users/adrian.iordache/Desktop/Users to Restaurants/JSON Files/venues.json"
venues_data <- fromJSON(paste(readLines(venues_file), collapse=""))
venues <- data.table(venues_data)
venues_list <- sapply( as.list( as.data.frame(venues)[,1]), toupper)

# CONSTRUCT 2 DATAFRAMES FOR PEOPLE'S DRINKS & NO-FOOD PREFERENCES
what_people_drink <- mutate_all( as.data.frame( users[, list(drinks = unlist(as.list(drinks)) ), by = name ] ), .funs=toupper)
what_people_dont_eat <- mutate_all( as.data.frame(users[, list(wont_eat = unlist(as.list(wont_eat))) , by = name ]), .funs=toupper)

# CONSTRUCT 2 DATAFRAMES  FOR VENUES' DRINKS & FOOD
venues_drinks <- mutate_all( as.data.frame( venues[, list(drinks = unlist(as.list(drinks))), by = name ] ), .funs=toupper)
venues_food <-  mutate_all( as.data.frame(venues[, list(food = unlist(as.list(food))) , by = name ]), .funs=toupper)

# LOGIC OF THE PROGRAM
inapplicable_venues <- list()
for (person in people_going_out) {
    
      this_person_drinks <- as.list(what_people_drink[which(what_people_drink$name == person),][,2])
      this_person_doesnt_eat <- as.list(what_people_dont_eat[which(what_people_dont_eat$name == person),][,2])
      
      for (venue in venues_list) {
           
           venue_drinks <- as.list(venues_drinks[which(venues_drinks$name ==venue),][,2])
           venue_food <- as.list(venues_food[which(venues_food$name ==venue),][,2])
           
           if (length(intersect(venue_drinks, this_person_drinks))==0) # append the reason why this place is not good for this person
                             {inapplicable_venues[[venue]] <- c(inapplicable_venues[[venue]], paste0("Nothing for ", person, " to drink.")) }
           
           if (length(setdiff(venue_food, this_person_doesnt_eat))==0)
                            {inapplicable_venues[[venue]] <- c(inapplicable_venues[[venue]], paste0("Nothing for ", person, " to eat.")) }
      }
#normally, if venue X is eliminated by Person 1, it shouldn't be checked for the other persons (but we want to find all conflicts)
}

#======OUTPUT: DISPLAY THE RESULTS TO USER======
venues_to_avoid <- names(inapplicable_venues) # only the names of the venues to avoid
venues_to_avoid_nr <- sapply(inapplicable_venues, length) # how many conflicts (reasons) are there to avoid each pub
venues_to_avoid_nr_conflicts <- paste0(venues_to_avoid, paste0(" (",venues_to_avoid_nr, " conflicts)") )

if (length(venues_to_avoid)==0)
{paste("No Venue should be avoided. This can be a long night!")} else
{cat( cat("There are", length(venues_to_avoid_nr_conflicts), "venues to avoid, and these are: "), unlist(venues_to_avoid_nr_conflicts), sep="\n")}

venues_to_attend <- setdiff(venues_list, venues_to_avoid)
if (length(venues_to_attend)==0)
{paste("We can't go anywhere, no Venue saties everybody. Booo :(")} else
{cat( cat("There are", length(venues_to_attend), "venues to attend, and these are: "), unlist(venues_to_attend), sep="\n")}


reasons_to_avoid <- data.frame(`Venue To Avoid` = rep(names(inapplicable_venues), sapply(inapplicable_venues, length)),
                                            `Reason To Avoid` = unlist(inapplicable_venues),
                                            row.names = NULL)
print(reasons_to_avoid) # all the reasons why each venue should be avoided (easier to read in this format)