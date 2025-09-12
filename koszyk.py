import csv
import streamlit as st
import time
import pandas as pd


def wprowadz_kategorie():
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
        with st.form("prod_form", clear_on_submit=True):
       
            produkt = st.text_input("Podaj nazwę produktu:", key="produkt_form")
            produkt=produkt.strip()
            kategoria = pokaz_kategorie("prod_form")
            
            ilosc = st.number_input(
                    "Podaj ilość:",
                    min_value=0,     # minimalna wartość
                    max_value=100,   # maksymalna wartość (opcjonalnie)
                    step=1,          # krok (1 → tylko liczby całkowite)
                    value=10         # domyślna wartość
                )
            cena = st.number_input(
                    "Podaj cenę:",
                    min_value=1,     # minimalna wartość
                    max_value=1000,   # maksymalna wartość (opcjonalnie)
                    step=1,          # krok (1 → tylko liczby całkowite)
                    value=5         # domyślna wartość
                )
            submitted = st.form_submit_button("Dodaj produkt")  
            ilosc = int(ilosc)
            if submitted:
                if not produkt.strip():
                    st.error("❌ Produkt nie może być pusty!")
                elif produkt.lower() == "koniec":
                    st.success("✅ Wprowadzanie zakończone")
                else:
                    with open("produkt.csv", mode="a", newline="") as csvfile:
                        writer = csv.writer(csvfile, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL)
                        writer.writerow([produkt , kategoria, cena,ilosc])
                    st.success(f"✅ Dodano produkt: {produkt}")
    
 
       
           

# Analiza koszyka zakupowego

def pokaz_df():
    df =pd.read_csv('produkt.csv',header = None, names=["produkt","kategoria","cena","ilosc"], 
                    delimiter=';')   
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
        df_prod=df[df['produkt'] == produkt]
        ilosc_prod= df_prod['ilosc'].sum()
        # st.write(df_prod)
        if produkt != '-- wybierz produkt --':
            st.dataframe(df_prod, hide_index=True)
            st.write(f'Produktów jest {ilosc_prod} ')   


def prod_max_ilosc(prod):
    opis = '''Maksymalna ilosc produktow'''
    ilosc_max = prod['ilosc']
    return ilosc_max

def koszyk_zakupowy():
    produkty_list = []   
    with open("produkt.csv", mode="r", newline="") as csvfile:
        produkty = csv.reader(csvfile, delimiter=';', quotechar='|')       
        next(produkty)  # jeśli masz nagłówek w CSV
        for pr in produkty:
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

    # Lista nazw produktów do selectbox
    nazwy = [p["nazwa"] for p in produkty_list]
    produkt = st.selectbox("Wybierz produkt:", nazwy)

    # znajdź produkt w liście
    prod = next((p for p in produkty_list if p["nazwa"] == produkt), None)

    if prod:
        # teraz dopiero można ustawić ilość z max_value
        ilosc = st.number_input(
            "Ilość:",
            min_value=1,
            value=1,
            max_value=prod_max_ilosc(prod)
        )
    else:
        st.error("Nie znaleziono produktu w bazie!")
        ilosc = 1

    # Dodanie do koszyka
    if st.button("➕ Dodaj do koszyka") and prod:
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


   

    