
import datetime

# Function to save the ID in a text file
def save_id_to_file(full_name, ID_generated, birthday):
    with open("/Users/luisstephan/Desktop/ids.txt", "a") as file:
        file.write(f"{full_name}, {ID_generated}, {birthday}\n")

#Function to read amount of lines
def read_lines():
    with open('/Users/luisstephan/Desktop/ids.txt', 'r') as file:
        lines = file.readlines()
        print(f"\nAnzahl der Zeilen: {len(lines)}")

#Function to create ID and output age
def ID_generation():

    # Input and current time 
    full_name = input("Enter your full name: ")
    birthday_and_month = input("\nEnter your year and month or birth (like this MM/YYYY):")
    current_date = datetime.datetime.now()

    # Full name gets split up and saved in list
    name_list = full_name.split()
    # birthyear and month get split up at the /
    month, year = birthday_and_month.split('/')
    # current year and month get put in int
    current_year = current_date.year
    current_month = current_date.month

    # change in to int
    year = int(year)
    month = int(month)

    # First letter identification through loop
    first_letters = ''.join([name[0] for name in name_list])

    # Letters in ID will be in lower case
    first_letters = first_letters.lower()

    # Creation of new ID
    ID_generated = first_letters + "_" + str(year)[-2:]

    # Calculation of age
    years_old = current_year - year
    months_old = current_month - month

    # Berücksichtigung, falls der Monat noch nicht erreicht wurde
    if months_old < 0:
        years_old -= 1
        months_old += 12

    # Ausgabe
    print(f"Hello {full_name}! This is your new ID: {ID_generated}")
    print(f"Du bist {years_old} Jahre und {months_old} Monate alt.")

    # Save the ID and data to a text file
    save_id_to_file(full_name, ID_generated, birthday_and_month)
    print("Die ID wurde erfolgreich in der Textdatei gespeichert.")


def Eingabe():

    while True:

        wahl = input("\n\n Um eine neue ID zu erstellen: new\n Um die aktuelle Anzahl an IDs abzurufen: check\n Um das Programm zu beenden: exit\n\n")

        if wahl == 'new':
            ID_generation()

        elif wahl == 'check':
            read_lines()

        elif wahl == 'exit':
            print("Programm beendet")
            break

        else:
            print("\nUngültige Eingabe, bitte erneut versuchen.")


Eingabe()