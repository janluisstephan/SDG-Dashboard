import random

def initialize_game():
    capital = 20000
    stocks = {
        "Tesla": 300,
        "Apple": 200,
        "Amazon": 250,
        "Google": 350
    }
    portfolio = {stock: [] for stock in stocks}  # Jede Aktie hat eine Liste von Transaktionen
    trends = {stock: random.choice([-1, 1]) for stock in stocks}
    return capital, stocks, portfolio, trends

# Begrüßung und Regeln
def display_rules():
    print("\n" + "=" * 60)
    print("Willkommen zum Aktienspiel!".center(60))
    print("=" * 60)
    print("\nZiel: Vermehre dein Kapital über 50 Tage.".center(60))
    print("Startkapital: 20.000 €".center(60))
    print("Jeden Tag ändern sich die Aktienpreise.".center(60))
    print("Am Ende des Spiels wird dein Gesamtkapital bewertet.".center(60))
    print("\n" + "=" * 60)


# Preise aktualisieren
# Preise aktualisieren
def update_prices(stocks, trends, current_day, mega_events, historical_prices):
    """
    Aktualisiert die Aktienpreise und berücksichtigt Mega-Events wie Bullen- und Bärenmärkte.

    Parameters:
    - stocks (dict): Aktuelle Aktienpreise.
    - trends (dict): Trends für jede Aktie.
    - current_day (int): Der aktuelle Tag im Spiel.
    - mega_events (list): Liste der geplanten Mega-Events.
    - historical_prices (dict): Historische Preise der Aktien.

    Returns:
    - stocks (dict): Aktualisierte Aktienpreise.
    - trends (dict): Aktualisierte Trends.
    - events (dict): Beschreibung der Ereignisse.
    """
    events = {}

    # Überprüfe, ob ein Mega-Event aktiv ist
    active_mega_event = None
    for event in mega_events:
        if event["start"] <= current_day < event["start"] + event["duration"]:
            active_mega_event = event
            break

    # Ereignisse für jedes Unternehmen mit zufälligen Prozentbereichen
    company_events = {
        "Tesla": [
            ("Tesla veröffentlicht ein neues Modell", (5, 15)),
            ("Tesla stellt Cybertruck vor", (10, 25)),
            ("Elon Musk twittert über Bitcoin", (-15, -5)),
            ("Tesla-Batterie-Problem entdeckt", (-20, -10)),
            ("Tesla erzielt Rekordumsatz", (10, 20)),
            ("Tesla gerät in rechtliche Probleme", (-25, -15)),
            ("Tesla-Fabrikstreik", (-15, -5)),
            ("Tesla gewinnt Innovationspreis", (15, 30)),
            ("Tesla-Produktionsziele übertroffen", (5, 10)),
            ("Tesla führt autonomes Fahren ein", (20, 35)),
        ],
        "Apple": [
            ("Apple veröffentlicht ein neues iPhone", (10, 20)),
            ("Apple verliert Rechtsstreit", (-20, -10)),
            ("Apple startet neuen Streaming-Dienst", (5, 15)),
            ("Apple kündigt Preiserhöhung an", (3, 8)),
            ("Apple stellt revolutionären Chip vor", (15, 25)),
            ("Apple-Geräte haben Sicherheitsprobleme", (-15, -8)),
            ("Apple verfehlt Quartalsziele", (-25, -15)),
            ("Apple-Aktie wird von Analysten empfohlen", (5, 12)),
            ("Apple investiert in erneuerbare Energien", (3, 10)),
            ("Apple kündigt Rückruf von Geräten an", (-10, -5)),
        ],
        "Amazon": [
            ("Amazon erzielt Rekordumsätze im Prime Day", (15, 30)),
            ("Amazon-Lieferprobleme in der Weihnachtszeit", (-15, -8)),
            ("Amazon führt Drohnenlieferungen ein", (10, 20)),
            ("Amazon wird wegen Steuervermeidung kritisiert", (-10, -5)),
            ("Amazon erweitert Cloud-Angebot", (5, 15)),
            ("Amazon verliert Rechtsstreit", (-25, -15)),
            ("Amazon eröffnet neue Logistikzentren", (3, 8)),
            ("Amazon übernimmt ein Tech-Startup", (10, 20)),
            ("Amazon-Arbeiter streiken", (-20, -10)),
            ("Amazon-Serverausfall beeinträchtigt Dienste", (-30, -20)),
        ],
        "Google": [
            ("Google führt KI-Update für Suchmaschine ein", (10, 20)),
            ("Google wird wegen Monopolstellung verklagt", (-20, -15)),
            ("Google investiert in Quantencomputer", (8, 15)),
            ("Google-Serverausfall weltweit", (-25, -20)),
            ("Google kündigt neues Android-Update an", (5, 12)),
            ("Google verfehlt Umsatzprognosen", (-15, -10)),
            ("Google stellt revolutionäre KI vor", (15, 25)),
            ("Google wird von Behörden durchsucht", (-30, -20)),
            ("Google erzielt Rekordgewinne", (20, 30)),
            ("Google investiert in erneuerbare Energien", (5, 15)),
        ],
    }

    # Preise aktualisieren und Ereignisse anwenden
    for stock in stocks:
        # Standardmäßige Preisveränderung ohne Ereignis
        change = trends[stock] * random.randint(1, 10)

        # Mega-Event-Änderung
        if active_mega_event:
            if active_mega_event["type"] == "Bullenmarkt":
                change += random.randint(5, 15)  # Zusätzlicher Preisanstieg
            elif active_mega_event["type"] == "Bärenmarkt":
                change -= random.randint(5, 15)  # Zusätzlicher Preisrückgang

        # Zufälliges Ereignis für diese Aktie
        if random.randint(1, 10) <= 3:  # 30% Chance auf ein Ereignis
            event, effect_range = random.choice(company_events[stock])
            effect = random.uniform(*effect_range)  # Zufälligen Wert aus dem Bereich wählen
            events[stock] = f"{event}. Preis ändert sich um {effect:+.2f}%"
            # Preisveränderung nur durch das Ereignis
            stocks[stock] = max(1, stocks[stock] * (1 + effect / 100))
        else:
            # Normale Preisänderung, wenn kein Ereignis eintritt
            stocks[stock] = max(1, stocks[stock] + change)

        # Historische Preise aktualisieren
        if stock in historical_prices:
            historical_prices[stock].append(stocks[stock])

        # Trendänderung
        if random.randint(1, 5) == 1:
            trends[stock] = random.choice([-1, 1])

    # Mega-Event-Benachrichtigung
    if active_mega_event:
        events["Mega-Event"] = f"Aktiver {active_mega_event['type']} von Tag {active_mega_event['start']} bis {active_mega_event['start'] + active_mega_event['duration']}!"

    return stocks, trends, events





def plan_mega_events(total_days):
    """
    Plant Mega-Events (Bullen- und Bärenmärkte), die sich abwechseln und mindestens zweimal pro Spiel auftreten.

    Parameters:
    - total_days (int): Die Gesamtzahl der Spieltage.

    Returns:
    - mega_events (list): Liste geplanter Mega-Events mit Typ, Starttag und Dauer.
    """
    mega_events = []
    event_types = ["Bullenmarkt", "Bärenmarkt"]  # Abwechslung zwischen Bullen- und Bärenmärkten
    current_type_index = 0  # Start mit Bullenmarkt

    # Mindestens vier Mega-Events (zwei Bullen- und zwei Bärenmärkte)
    num_events = 4
    days_between_events = total_days // (num_events + 1)  # Gleichmäßige Verteilung

    for i in range(num_events):
        start_day = (i + 1) * days_between_events
        duration = random.randint(3, 6)  # Dauer der Mega-Events zwischen 3 und 6 Tagen
        event_type = event_types[current_type_index]

        mega_events.append({
            "type": event_type,
            "start": start_day,
            "duration": duration
        })

        # Abwechseln zwischen Bullen- und Bärenmarkt
        current_type_index = (current_type_index + 1) % 2

    return mega_events



# Prozentuale Änderung berechnen
def percentage_change(new, old):
    return ((new - old) / old) * 100 if old != 0 else 0

# Portfolio anzeigen
# Portfolio anzeigen
def display_portfolio(portfolio, stocks, capital, total_history):
    """
    Zeigt das Portfolio an, einschließlich der aktuellen Verkaufswerte, Gewinne/Verluste,
    und des Index-Verlaufs des Gesamtbesitzes.
    """
    print("\n" + "=" * 60)
    print("PORTFOLIO ÜBERSICHT".center(60))
    print("=" * 60)
    total_value = 0  # Gesamtwert des Portfolios
    total_gain_loss = 0  # Gesamtgewinn oder -verlust

    for stock, transactions in portfolio.items():
        if transactions:
            print(f"\n{stock}:")
            stock_total = 0
            stock_gain_loss = 0
            for transaction in transactions:
                quantity = transaction["quantity"]
                bought_price = transaction["price"]
                current_price = stocks[stock]
                current_value = quantity * current_price
                gain_loss = (current_price - bought_price) * quantity
                stock_total += current_value
                stock_gain_loss += gain_loss

                print(f"  - {quantity} Aktien zu {bought_price:.2f} € gekauft")
                print(f"    Aktueller Wert: {current_value:.2f} € (Gewinn/Verlust: {gain_loss:+.2f} €)")

            print(f"  Gesamtwert dieser Aktie: {stock_total:.2f} €")
            print(f"  Gesamtgewinn/Verlust: {stock_gain_loss:+.2f} €")
            total_value += stock_total
            total_gain_loss += stock_gain_loss

    print("\n" + "=" * 60)
    print(f"Gesamter Portfolio-Wert: {total_value:.2f} €")
    print(f"Kapital: {capital:.2f} €")
    print(f"Gesamter Gewinn/Verlust: {total_gain_loss:+.2f} €")
    print(f"Gesamtbesitz (Kapital + Portfolio): {capital + total_value:.2f} €")
    print("=" * 60 + "\n")

    # Gesamtbesitz-Verlauf anzeigen
    if total_history:
        display_total_index(total_history)

def display_total_index(total_history):
    """
    Zeigt den Verlauf des Gesamtbesitzes im Index-Stil mit Tausenderschritten.
    """
    if not total_history:  # Keine Daten verfügbar
        print("Keine Daten für den Gesamtbesitz verfügbar.")
        return

    # Bestimme den maximalen Besitz für die Y-Achse und runde auf Tausender
    max_total = max(total_history)
    step = 1000  # Schrittweite der Y-Achse in Tausenderschritten
    levels = range(0, int(max_total) + step, step)  # Y-Achse von 0 bis max_total
    levels = list(reversed(levels))  # Von oben nach unten

    # Platz für 50 Tage reservieren (falls nicht genügend Daten vorhanden sind)
    total_days = 50
    padded_totals = total_history + [None] * max(0, total_days - len(total_history))

    print("\n" + "=" * 60)
    print("GESAMTBESITZ-VERLAUF".center(60))
    print("=" * 60)

    # Zeichne das Diagramm von oben (höchster Besitz) nach unten (niedrigster Besitz)
    for level in levels:
        # Konvertiere den Level-Wert in Tausenderdarstellung (z.B. "10k" statt "10000")
        level_label = f"{level // 1000}k"
        line = f"{level_label:>7} |"  # Y-Achsen-Beschriftung
        for total in padded_totals:
            if total is None:  # Keine Daten für diesen Tag
                line += " "
            elif total >= level:  # Besitz liegt über oder auf der aktuellen Ebene
                line += "#"
            else:  # Besitz liegt unter der aktuellen Ebene
                line += " "
        print(line)

    # Zeichne die horizontale Linie unterhalb des Diagramms
    print("        " + "-" * total_days)

    # Abschlusslinie
    print("=" * 60)




# Spieleraktionen
def handle_actions(capital, portfolio, stocks, previous_prices, historical_prices, total_history):
    while True:
        print("\n" + "-" * 60)
        print("AKTIONEN".center(60))
        print("-" * 60)
        print("1: Kaufen")
        print("2: Verkaufen")
        print("3: Portfolio anzeigen")
        print("4: Heutige Preisänderungen anzeigen")
        print("5: Aktienindex anzeigen")
        print("6: Nächster Tag starten")
        print("7: Spiel beenden")
        print("-" * 60)
        
        action = input("Wähle eine Aktion: ").strip()
        print("\n")

        if action == "1":  # Kaufen
            print(f"Aktuelles Kapital: {capital:.2f} €")
            stock = get_stock_input(stocks)

            amount = input(f"Wieviele Aktien von {stock} kaufen?: ").strip()
            if amount.isdigit():
                amount = int(amount)
                cost = amount * stocks[stock]
                if cost <= capital:
                    portfolio[stock].append({"quantity": amount, "price": stocks[stock]})
                    capital -= cost
                    print(f"Gekauft: {amount} {stock}-Aktien für {cost:.2f} €. Verbleibendes Kapital: {capital:.2f} €")
                else:
                    print(f"Nicht genug Geld! Du hast nur {capital:.2f} €.")
            else:
                print("Ungültige Anzahl. Bitte erneut versuchen.")

        elif action == "2":  # Verkaufen
            stock = get_stock_input(stocks)
            if portfolio[stock]:
                print(f"\nDu hast folgende Käufe von {stock}:")
                for i, transaction in enumerate(portfolio[stock], start=1):
                    print(f"{i}: {transaction['quantity']} Aktien zu {transaction['price']:.2f} €")
                choice = input("Wähle die Transaktion zum Verkauf (Nummer): ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(portfolio[stock]):
                    transaction = portfolio[stock][int(choice) - 1]
                    amount = input(f"Wieviele Aktien aus dieser Transaktion verkaufen? (Max: {transaction['quantity']}): ").strip()
                    if amount.isdigit():
                        amount = int(amount)
                        if 0 < amount <= transaction["quantity"]:
                            revenue = amount * stocks[stock]
                            transaction["quantity"] -= amount
                            capital += revenue
                            print(f"Verkauft: {amount} {stock}-Aktien für {revenue:.2f} €. Neues Kapital: {capital:.2f} €")
                            if transaction["quantity"] == 0:
                                portfolio[stock].remove(transaction)
                        else:
                            print("Ungültige Anzahl!")
                    else:
                        print("Ungültige Eingabe!")
                else:
                    print("Ungültige Transaktionsnummer!")
            else:
                print("Du besitzt keine Aktien von dieser Firma.")

        elif action == "3":  # Portfolio anzeigen
            display_portfolio(portfolio, stocks, capital, total_history)

        elif action == "4":  # Heutige Preisänderungen anzeigen
            display_daily_prices(stocks, previous_prices)

        elif action == "5":  # Aktienindex anzeigen
            print("\nWähle eine Aktie, um den Index zu sehen:")
            for i, stock in enumerate(stocks.keys(), start=1):
                print(f"{i}: {stock}")
            choice = input("Gib die Nummer oder den Namen der Aktie ein: ").strip()

            if choice.isdigit() and 1 <= int(choice) <= len(stocks):
                stock_name = list(stocks.keys())[int(choice) - 1]
            elif choice in stocks:
                stock_name = choice
            else:
                print("Ungültige Eingabe. Bitte erneut versuchen.")
                return capital  # Zurück zur Kapitalanzeige

            if stock_name in historical_prices:
                display_stock_index(stock_name, historical_prices[stock_name])
            else:
                print(f"Keine historischen Daten für {stock_name} verfügbar.")

        elif action == "6":  # Nächster Tag starten
            return capital

        elif action == "7":  # Spiel beenden
            print("Spiel wird beendet. Vielen Dank fürs Spielen!")
            exit()  # Beendet das Programm sofort

        else:
            print("Ungültige Eingabe. Bitte erneut versuchen.")





# Tagespreise anzeigen
def display_daily_prices(stocks, previous_prices):
    print("\n" + "-" * 60)
    print("HEUTIGE PREISÄNDERUNGEN".center(60))
    print("-" * 60)
    for stock, price in stocks.items():
        change = percentage_change(price, previous_prices[stock])
        print(f"{stock}: {price:.2f} € ({change:+.2f}%)")
    print("-" * 60 + "\n")

def display_stock_index(stock_name, stock_prices):
    """
    Zeigt den Aktienindex in der Konsole mit korrekten historischen Preisen.

    Parameters:
    - stock_name (str): Name der Aktie.
    - stock_prices (list): Historische Preise der Aktie.
    """
    if not stock_prices:  # Keine Daten verfügbar
        print("Keine Daten für den Aktienindex verfügbar.")
        return

    # Bestimme den maximalen Preis für die Y-Achse
    max_price = max(stock_prices)
    step = 20  # Schrittweite der Y-Achse (z. B. 20er-Schritte)
    levels = range(0, int(max_price) + step, step)  # Y-Achse von 0 bis max_price
    levels = list(reversed(levels))  # Von oben nach unten

    # Platz für 50 Tage reservieren (falls nicht genügend Daten vorhanden sind)
    total_days = 50
    padded_prices = stock_prices + [None] * max(0, total_days - len(stock_prices))

    print("\n" + "=" * 60)
    print(f"Preisverlauf für {stock_name}".center(60))
    print("=" * 60)

    # Zeichne das Diagramm von oben (höchster Preis) nach unten (niedrigster Preis)
    for level in levels:
        line = f"{level:>4} |"  # Y-Achsen-Beschriftung
        for price in padded_prices:
            if price is None:  # Keine Daten für diesen Tag
                line += " "
            elif price >= level:  # Preis liegt über oder auf der aktuellen Ebene
                line += "#"
            else:  # Preis liegt unter der aktuellen Ebene
                line += " "
        print(line)

    # Zeichne die horizontale Linie unterhalb des Diagramms
    print("     " + "-" * total_days)

    # Abschlusslinie
    print("=" * 60)




# Aktie auswählen
def get_stock_input(stocks):
    """
    Ermöglicht die Auswahl einer Aktie durch Eingabe einer Nummer oder des Namens.
    """
    while True:
        print("\nWähle eine Aktie:")
        for i, stock in enumerate(stocks.keys(), start=1):
            print(f"{i}: {stock}")
        choice = input("Gib die Nummer oder den Namen der Aktie ein: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(stocks):
            return list(stocks.keys())[int(choice) - 1]
        elif choice in stocks:
            return choice
        else:
            print("Ungültige Eingabe. Bitte erneut versuchen.")


# Endauswertung
def end_game(capital, portfolio, stocks):
    total_value = capital + sum(
        transaction["quantity"] * stocks[stock]
        for stock, transactions in portfolio.items()
        for transaction in transactions
    )
    print("\n--- Spielende ---")
    print(f"Dein Gesamtwert beträgt: {total_value:.2f} €")
    display_portfolio(portfolio, stocks)


#Ausführung des Spiels
def main():
    total_days = 50  
    capital, stocks, portfolio, trends = initialize_game()
    display_rules()
    previous_prices = stocks.copy()
    historical_prices = {stock: [price] for stock, price in stocks.items()}  # Initialisierung der historischen Preise

    total_history = [capital + sum(
        transaction["quantity"] * stocks[stock]
        for stock, transactions in portfolio.items()
        for transaction in transactions
    )]

    # Planen der Mega-Events
    mega_events = plan_mega_events(total_days)

    for day in range(1, total_days + 1):
        print("\n" + "=" * 60)
        print(f"=== TAG {day} ===".center(60))
        print("=" * 60)

        # Preise aktualisieren mit Mega-Events
        stocks, trends, events = update_prices(stocks, trends, day, mega_events, historical_prices)

        # Ereignisse anzeigen
        if events:
            print("\nEreignisse:")
            for key, event in events.items():
                print(f"{key}: {event}")
            print("-" * 60)

        # Tagespreise anzeigen
        display_daily_prices(stocks, previous_prices)

        # Spieleraktionen
        capital = handle_actions(capital, portfolio, stocks, previous_prices, historical_prices, total_history)

        # Vorherige Preise aktualisieren
        previous_prices = stocks.copy()

        # Gesamtbesitz berechnen und speichern
        total_value = sum(
            transaction["quantity"] * stocks[stock]
            for stock, transactions in portfolio.items()
            for transaction in transactions
        )
        total_history.append(capital + total_value)

    # Endauswertung
    end_game(capital, portfolio, stocks)



# Spiel starten
if __name__ == "__main__":
    main()