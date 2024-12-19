
'''
def print_cube():
    top = [
        "             +----+----+",
        "             | ** | ** |",
        "             +----+----+",
        "             | ** | ** |",
        "             +----+----+"
    ]
    
    middle = [
        "+----+----+  +----+----+  +----+----+  +----+----+",
        "| %% | %% |  | ## | ## |  | @@ | @@ |  | $$ | $$ |",
        "+----+----+  +----+----+  +----+----+  +----+----+",
        "| %% | %% |  | ## | ## |  | @@ | @@ |  | $$ | $$ |",
        "+----+----+  +----+----+  +----+----+  +----+----+"
    ]
    
    bottom = [
        "             +----+----+",
        "             | && | && |",
        "             +----+----+",
        "             | && | && |",
        "             +----+----+"
    ]

    # Print the cube layers
    for line in top:
        print(line)
    for line in middle:
        print(line)
    for line in bottom:
        print(line)

# Run the function to display the cube
print_cube()
'''

cube = {
    'oben': [['White'] * 2 for _ in range(2)],  # Weiß für die obere Seite
    'unten': [['Yellow'] * 2 for _ in range(2)],  # Gelb für die untere Seite
    'vorne': [['Green'] * 2 for _ in range(2)],  # Grün für die Vorderseite
    'hinten': [['Blue'] * 2 for _ in range(2)],  # Blau für die Rückseite
    'links': [['Orange'] * 2 for _ in range(2)],  # Orange für die linke Seite
    'rechts': [['Red'] * 2 for _ in range(2)],  # Rot für die rechte Seite
}

def print_face(face):
    for row in face:
        print(" ".join(row))

def print_cube(cube):
    # Oben
    print("   ", end="")
    print_face(cube['oben'])
    
    # Linke, vordere, rechte, hintere Seiten nebeneinander
    for i in range(2):
        print(" ".join(cube['links'][i]), end="   ")
        print(" ".join(cube['vorne'][i]), end="   ")
        print(" ".join(cube['rechts'][i]), end="   ")
        print(" ".join(cube['hinten'][i]))
    
    # Unten
    print("   ", end="")
    print_face(cube['unten'])

print_cube(cube)