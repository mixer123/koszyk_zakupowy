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
    # st.write(st.table(df.values))
    
    return df
## Wyświetl wszystko z danej kategorii

##  Ilość produktównw kategorii
def pokaz_kategoria():             
        df = pokaz_df()
        kategorie_unikalne = df['kategoria'].unique()
        kategoria = st.selectbox("Wybierz kategorie:", kategorie_unikalne)
        df_kat=df.loc[df['kategoria'] == kategoria]
        ilosc_prod= df_kat['ilosc'].sum()
        st.write(df_kat)
        st.write(f'W kategorii jest {ilosc_prod} produktów')


'''Wyswietla wszystkie produkty z daną nazwą '''
def pokaz_produkt():       
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
       


if __name__ == "__main__":
    with st.sidebar:        
        select = st.selectbox(
            "Wybierz ",
            [
                "Wprowadź kategorię",
                "Wprowadź produkt",               
                "Pokaz kategorię",
                "Pokaz produkt",
            ],
        )
if select == "Wprowadź kategorię":   
    wprowadz_kategorie()
if select == "Wprowadź produkt":
    # pokaz_kategorie()
    wprowadz_produkt()

if select == "Pokaz kategorię":
    pokaz_kategoria()
if select == "Pokaz produkt":
    pokaz_produkt()

   

    