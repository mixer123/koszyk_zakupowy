Zadanie Domowe 2: Analiza koszyka zakupowego,
Celem zadania jest opracowanie prostego systemu analizy koszyka zakupowego w sklepie internetowym. Należy napisać program, który będzie analizował listy zakupowe klientów. Program powinien umożliwiać:,
Wprowadzenie danych:,


Przygotowanie listy produktów, którą będzie można wprowadzić jako dane wejściowe. Każdy produkt powinien być reprezentowany przez krotkę zawierającą:
Nazwę produktu (łańcuch znaków),
Kategorię produktu (łańcuch znaków),
Cenę (liczba zmiennoprzecinkowa),

Analiza danych:,


Utworzenie funkcji, która przyjmuje listę zakupów (listę krotek) i zwraca słownik, w którym kluczem jest nazwa kategorii, a wartością jest lista produktów tej kategorii.,
Utworzenie funkcji, która oblicza i zwraca całkowity koszt zakupów z podziałem na kategorie.,
Utworzenie funkcji, która identyfikuje najdroższy produkt z każdej kategorii.,
Dodanie 3 różnych warunków walidacyjnych.,

Wyniki i raport:,


Wyświetlenie listy wszystkich produktów z podziałem na kategorie.,
Wyświetlenie całkowitego kosztu dla każdej kategorii.,
Wyświetlenie najdroższego produktu w każdej kategorii.,
(Opcjonalnie) Wyświetlenie średniej ceny produktów w każdej kategorii.,
(Opcjonalnie) Zwizualizowanie wyników z wykorzystaniem np. biblioteki Matplotlib.,

Przykładowe dane wejściowe:

produkty = [
    ("Jabłko", "Owoce", 0.5),
    ("Gruszka", "Owoce", 0.7),
    ("Chleb", "Pieczywo", 1.5),
    ("Masło", "Nabiał", 2.0),
    ("Ser", "Nabiał", 2.5),
    ("Pomidor", "Warzywa", 1.0),
]

Wymagania techniczne:

Użycie list, krotek i słowników do organizacji danych.,
Stworzenie funkcji do przetwarzania i analizy danych.,
