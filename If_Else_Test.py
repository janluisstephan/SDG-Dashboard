

def Eingabetest():

    while True:

        wahl = input("\n Um eine neue ID zu erstellen: new\n Um die aktuelle Anzahl an IDs abzurufen: check\n Um das Programm zu beenden: exit\n")

        if wahl == 'new':
            print("Du hast Option 1 gewählt!")
        elif wahl == 'check':
            print("Du hast Option 2 gewählt!")
        elif wahl == 'exit':
            print("Programm beendet")
            break
        else:
            print("Ungültige Eingabe, bitte erneut versuchen.")


Eingabetest()

