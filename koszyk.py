import csv
import streamlit as st
import time
import pandas as pd
import os


def wprowadz_kategorie():
        opis = '''To jest funkcja tworząca kategorię produktów'''
        with st.form("kat_form", clear_on_submit=True):
       
            kat = st.text_input("Podaj nazwę kategorii:", key="kategoria_form")
            submitted = st.form_submit_button("Dodaj kategorię")        #
            if submitted:
                if not kat.strip():
                    st.error("❌ Kategoria nie może być pusta!")
                elif kat.lower() == "koniec":
                    st.success("✅ Wprowadzanie zakończone")
                else:
                    with open("kategorie.csv", mode="a", newline="") as csvfile:
                        writer = csv.writer(csvfile, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL)
                        writer.writerow([kat])
                    st.success(f"✅ Dodano kategorię: {kat}")



def czytaj_kategorie():
    kategoria_list =[]
    with  open("kategorie.csv", mode="r", newline="") as csvfile:
        kategoria = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in kategoria:        
            kategoria_list.append(row[0])
    return kategoria_list


def pokaz_kategorie(name_form=None):
    lista_kategorii = czytaj_kategorie()
    if lista_kategorii:
        option = st.selectbox("Wybierz kategorię:", lista_kategorii, key=name_form)        
        return option
    else:
        st.write("Brak kategorii w pliku CSV")
        return None


def wprowadz_produkt():
    lista_nazw_produktow = []  # zawsze inicjalizujemy listę

    # Sprawdzamy, czy plik istnieje i nie jest pusty
    if os.path.exists("produkt.csv") and os.path.getsize("produkt.csv") > 0:
        with open("produkt.csv", mode="r", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                if len(row) < 4:  # pomijamy puste lub niepełne linie
                    continue
                nazwa, kategoria, cena, ilosc = row
                lista_nazw_produktow.append(nazwa.strip().lower())

    # Debug: lista już istniejących produktów
    print(lista_nazw_produktow)

    # Formularz Streamlit
    with st.form("prod_form", clear_on_submit=True):
        produkt = st.text_input("Podaj nazwę produktu:", key="produkt_form").strip()
        kategoria = pokaz_kategorie("prod_form")  # Twoja funkcja do wyboru kategorii
        ilosc = st.number_input("Podaj ilość:", min_value=1, max_value=100, step=1, value=10)
        cena = st.number_input("Podaj cenę:", min_value=1, max_value=1000, step=1, value=5)

        submitted = st.form_submit_button("Dodaj produkt")

        if submitted:
            # Walidacja nazwy
            if not produkt:
                st.error("❌ Produkt nie może być pusty!")
            elif ";" in produkt:
                st.error("❌ Nazwa produktu nie może zawierać średnika ';'")
            elif produkt.lower() == "koniec":
                st.success("✅ Wprowadzanie zakończone")
            elif produkt.lower() in lista_nazw_produktow:
                st.warning("⚠️ Produkt już istnieje")
            else:
                # Zapis do CSV
                with open("produkt.csv", mode="a", newline="") as csvfile:
                    writer = csv.writer(csvfile, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([produkt, kategoria, cena, int(ilosc)])
                st.success(f"✅ Dodano produkt: {produkt}")

           

# Analiza koszyka zakupowego

def pokaz_df():
    # df =pd.read_csv('produkt.csv',header = None, names=["produkt","kategoria","cena","ilosc"], 
    #                 delimiter=';')   
    df =pd.read_csv('produkt.csv',delimiter=';')   
    return df



def pokaz_kategoria(): 
        opis = '''Ilość produktównw kategorii'''            
        df = pokaz_df()
        kategorie_unikalne = df['kategoria'].unique()
        kategoria = st.selectbox("Wybierz kategorie:", kategorie_unikalne)
        df_kat=df.loc[df['kategoria'] == kategoria]
        ilosc_prod= df_kat['ilosc'].sum()
        st.write(df_kat)
        st.write(f'W kategorii jest {ilosc_prod} produktów')



def pokaz_produkt():  
        opis = '''Wyswietla wszystkie produkty z daną nazwą'''   
        df = pokaz_df()
        produkty_unikalne = df['produkt'].unique().tolist()
        produkty_unikalne = ["-- wybierz produkt --"] + produkty_unikalne
        produkt = st.selectbox("Wybierz produkt:", produkty_unikalne, index=0)      
        
        # st.write(df_prod)
        if produkt != '-- wybierz produkt --':
            df_prod = df[df['produkt'] == produkt]
            print(df_prod["ilosc"])
            ilosc_prod= df_prod['ilosc'].sum()
            st.dataframe(df_prod, hide_index=True)
            st.write(f'Produktów jest {ilosc_prod} ') 
            row = df_prod.iloc[0]
            with st.form("edit_form"):
                nowa_nazwa = st.text_input("Nazwa produktu", row["produkt"])
                nowa_kategoria = st.text_input("Kategoria", row["kategoria"])
                nowa_cena = st.number_input("Cena", value=float(row["cena"]), min_value=0.0)
                nowa_ilosc = st.number_input("Ilość", value=int(row["ilosc"]), min_value=0)

                submitted = st.form_submit_button("💾 Zapisz zmiany")

                if submitted:
                    # aktualizacja w DataFrame
                    idx = df[df['produkt'] == produkt].index[0]  # bierzemy pierwszy indeks
                    df.loc[idx, ['produkt', 'kategoria', 'cena', 'ilosc']] = [
                                     nowa_nazwa, nowa_kategoria, nowa_cena, nowa_ilosc
                                                                             ]

                    # nadpisanie pliku CSV
                    df.to_csv("produkt.csv", sep=";", index=False)

                    st.success(f"✅ Produkt '{produkt}' został zaktualizowany")




def prod_max_ilosc(prod):
    opis = '''Maksymalna ilosc produktow'''
    ilosc_max = prod['ilosc']
    return ilosc_max


def koszyk_zakupowy():
    produkty_list = []   
    with open("produkt.csv", mode="r", newline="") as csvfile:
        produkty = csv.reader(csvfile, delimiter=';', quotechar='|')       
        for pr in produkty:
            if len(pr)>0:
                nazwa, kategoria, cena, ilosc = pr
                produkty_list.append({
                    "nazwa": nazwa,
                    "kategoria": kategoria,
                    "cena": float(cena),
                    "ilosc": int(ilosc)
                })

    # Inicjalizacja koszyka
    if "koszyk" not in st.session_state:
        st.session_state.koszyk = {}

    # Lista nazw produktów
    nazwy = [p["nazwa"] for p in produkty_list]
    produkt = st.selectbox("Wybierz produkt:", nazwy)

    # znajdź produkt
    prod = next((p for p in produkty_list if p["nazwa"] == produkt), None)

    if prod:
        # ile już w koszyku
        ilosc_w_koszyku = st.session_state.koszyk.get(produkt, {}).get("ilosc", 0)

        # ile można jeszcze dodać
        ilosc_dostepna = prod["ilosc"] - ilosc_w_koszyku

        if ilosc_dostepna > 0:
            ilosc = st.number_input(
                "Ilość:",
                min_value=1,
                value=1,
                max_value=ilosc_dostepna
            )

            if st.button("➕ Dodaj do koszyka"):
                wartosc = prod["cena"] * ilosc

                if produkt in st.session_state.koszyk:
                    st.session_state.koszyk[produkt]["ilosc"] += ilosc
                    st.session_state.koszyk[produkt]["wartosc"] += wartosc
                else:
                    st.session_state.koszyk[produkt] = {
                        "ilosc": ilosc,
                        "cena": prod["cena"],
                        "wartosc": wartosc
                    }

                st.success(f"Dodano {ilosc} x {produkt} do koszyka")
        else:
            st.warning("⚠️ Nie możesz dodać więcej. Produkt wyczerpany.")
    else:
        st.error("Nie znaleziono produktu w bazie!")

    # Wyświetlenie koszyka
    if st.button("📋 Pokaż koszyk"):
        if st.session_state.koszyk:
            suma = 0
            for k, v in st.session_state.koszyk.items():
                st.write(f'{k}: {v["ilosc"]} szt. × {v["cena"]:.2f} zł = {v["wartosc"]:.2f} zł')
                suma += v["wartosc"]
            st.write(f"💰 **Suma: {suma:.2f} zł**")
        else:
            st.info("Koszyk jest pusty")



# def koszyk_zakupowy():
#     produkty_list = []   
#     with open("produkt.csv", mode="r", newline="") as csvfile:
#         produkty = csv.reader(csvfile, delimiter=';', quotechar='|')       
#         next(produkty)  # jeśli masz nagłówek w CSV
#         for pr in produkty:
#             nazwa, kategoria, cena, ilosc = pr
#             produkty_list.append({
#                 "nazwa": nazwa,
#                 "kategoria": kategoria,
#                 "cena": float(cena),
#                 "ilosc": int(ilosc)
#             })

#     # Inicjalizacja koszyka
#     if "koszyk" not in st.session_state:
#         st.session_state.koszyk = {}

#     # Lista nazw produktów do selectbox
#     nazwy = [p["nazwa"] for p in produkty_list]
#     produkt = st.selectbox("Wybierz produkt:", nazwy)

#     # znajdź produkt w liście
#     prod = next((p for p in produkty_list if p["nazwa"] == produkt), None)

#     if prod:
#         # teraz dopiero można ustawić ilość z max_value
#         ilosc = st.number_input(
#             "Ilość:",
#             min_value=1,
#             value=1,
#             max_value=prod_max_ilosc(prod)
#         )
#     else:
#         st.error("Nie znaleziono produktu w bazie!")
#         ilosc = 1

#     # Dodanie do koszyka
    
#     if st.button("➕ Dodaj do koszyka") and prod:
#         wartosc = prod["cena"] * ilosc

#         if produkt in st.session_state.koszyk:
#             st.session_state.koszyk[produkt]["ilosc"] += ilosc
#             st.session_state.koszyk[produkt]["wartosc"] += wartosc
#         else:
#             st.session_state.koszyk[produkt] = {
#                 "ilosc": ilosc,
#                 "cena": prod["cena"],
#                 "wartosc": wartosc
#             }

#         st.success(f"Dodano {ilosc} x {produkt} do koszyka")

#     # Wyświetlenie koszyka
#     if st.button("📋 Pokaż koszyk"):
#         print(st.session_state.koszyk.items())
#         if st.session_state.koszyk:
#             suma = 0
#             for k, v in st.session_state.koszyk.items():
#                 st.write(f'{k}: {v["ilosc"]} szt. × {v["cena"]:.2f} zł = {v["wartosc"]:.2f} zł')
#                 suma += v["wartosc"]
#                 with open("koszyk.csv", mode="a", newline="") as csvfile:
#                             writer = csv.writer(csvfile, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL)
#                             writer.writerow([k , v["ilosc"], v["cena"],v["wartosc"]])
       
#             st.write(f"💰 **Suma: {suma:.2f} zł**")
           
#         else:
#             st.info("Koszyk jest pusty")
#         # return st.session_state.koszyk
   




         


if __name__ == "__main__":
    with st.sidebar:        
        select = st.selectbox(
            "Wybierz ",
            [
                "Wprowadź kategorię",
                "Wprowadź produkt",               
                "Pokaz kategorię",
                "Pokaz produkt",
                "Dokonaj zakupów",
               
            ],
        )
st.header("Koszyk zakupowy")
if select == "Wprowadź kategorię":   
    wprowadz_kategorie()
if select == "Wprowadź produkt":
    # pokaz_kategorie()
    wprowadz_produkt()

if select == "Pokaz kategorię":
    pokaz_kategoria()
if select == "Pokaz produkt":
    pokaz_produkt()
if select == "Dokonaj zakupów":
    koszyk_zakupowy()


   

    