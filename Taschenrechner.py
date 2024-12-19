

def Addition(decide_number, decide_number2):

    sum = int(decide_number) + int(decide_number2)
    print(f"Das Ergebnis lautet:\n{sum}\n")

def Subtraktion(decide_number, decide_number2):
    
    sum = int(decide_number) - int(decide_number2)
    print(f"Das Ergebnis lautet:\n{sum}\n")

def Multiplikation(decide_number, decide_number2):
    
    sum = int(decide_number) * int(decide_number2)
    print(f"Das Ergebnis lautet:\n{sum}\n")

def Division(decide_number, decide_number2):
    
    sum = int(decide_number) / int(decide_number2)
    print(f"Das Ergebnis lautet:\n{sum}\n")

def Root(decide_number):

    x = int(decide_number)
    root = x/2
    a = x/root
    iteration = 0

    while abs(a - root) >.00001:
        root = (root + a)/2
        a = x/root
        iteration = iteration + 1
    
    print(f"Das Ergebnis lautet:\n{root}\n")

def Eingabe():

    while True:

        wahl =  decide_calculation = input("Entscheiden Sie sich für eine Rechnung.\n 1. Addition\n2. Subraktion\n 3. Multiplikation\n4. Division\n 5. Wurzel annäherung. \nexit um das Programm zu verlassen\n")

        
        if wahl in ['1', '2', '3', '4']:  
            decide_number = input("Geben Sie die erste Zahl ein: ")
            decide_number2 = input("Geben Sie die zweite Zahl ein: ")


            if wahl == '1':
            
                Addition(decide_number, decide_number2)

            elif wahl == '2':
            
                Subtraktion(decide_number, decide_number2)

            elif wahl == '3':
            
                Multiplikation(decide_number, decide_number2)

            elif wahl == '4':
           
                Division(decide_number, decide_number2)
            
        elif wahl == '5':
                decide_number = input("Geben Sie die erste Zahl ein: ")
                Root(decide_number)

        elif wahl == 'exit':
            break
    

        else:
            print("\nUngültige Eingabe, bitte erneut versuchen.")


Eingabe()
