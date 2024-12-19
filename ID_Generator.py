#Import of library
import datetime

#Input and current time 
full_name = input("\nEnter your full name:\n\n")
birthday_and_month = input("\nEnter your year and month or birth (like this MM/YYYY):\n\n")
current_date = datetime.datetime.now()


#Full name gets split up and saved in list
name_list = full_name.split()
#birthyear and month get split up at the /Ja
month, year = birthday_and_month.split('/')
#current year and month get put in int
current_year = current_date.year
current_month = current_date.month

#change into int
year = int(year)
month = int(month)


#First letter identification through loop. with name[0] we call first letters of every name in name_list
#.join will join every first letter that would be saved in new list and puts that into string
#'' is for the seperation between letters. Here its nothing
first_letters = ''.join([name[0] for name in name_list])


#Letters in ID will be in lower case
first_letters = first_letters.lower()


#Creation of new ID
ID_generated = first_letters + "_" + str(year)[-2:]


# Calculation of age
years_old = current_year - year
months_old = current_month - month


# Berücksichtigung, falls der Monat noch nicht erreicht wurde
if months_old < 0:
    years_old -= 1
    months_old += 12


#Ausgabe
print( f"\nHello {full_name}! This is your new ID: {ID_generated}")


print( f"Du bist {years_old} Jahre und: {months_old} Monate alt.\n")