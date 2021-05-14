#!/usr/bin/python3

# Autor: Max Nowak
# Version: 0.2
# Programm for Manipulation of ChickenList DB
# main Database Access

import psycopg2
import xlwt
from tkinter import messagebox as msg
from datetime import datetime

# establish connection with db // creating db

# for use with postgress
connection = psycopg2.connect("user=postgres host=localhost password=hC_pGSWYz-b-s762 dbname=postgres")

cur = connection.cursor()
cur.execute("""SET SCHEMA 'chickenlist';""")

connection.commit()


# Functions
# Returns formatted data-array fot sheet
def get_all():
    cur.execute("SELECT * FROM besitzer order by nachname, vorname;")
    connection.commit()

    owners_list = cur.fetchall()

    x = 0
    data = [["Name", "Adresse", "Telefonnummer", "Termin-datum", "Hühneranzahl", "Bezahlung"]]

    for owner in owners_list:
        data.append([])
        x = x + 1

        # hohlt sich die Liste der Termine für diesen Besitzer
        besitzer_id = owner[0]
        cur.execute("SELECT datum,anzahlhuehner,bezahlt "
                    "FROM impftermin JOIN besitzer_impftermin bi on impftermin.IID = bi.IID "
                    "WHERE BID = %s ORDER BY datum,anzahlhuehner;", [besitzer_id])
        connection.commit()

        termin_list = cur.fetchall()

        # schreibt Daten des Besitzers in Tabelle

        data[x].append(str(owner[1] + ", " + owner[2]))  # Nachname, Vorname
        data[x].append(str(owner[3] + " " + owner[4] + ", " + owner[5] + " " + owner[6]))  # Adresse
        data[x].append((owner[7]))  # Telefonnummer

        if not termin_list:  # if no termine for besitzer append empty values instead and jump to next besitzer
            data[x].append("")
            data[x].append("")
            data[x].append("")
            continue

        j = 0
        while j < len(termin_list):
            for i in range(3):
                data[x].append(str(termin_list[j][i]))

            if j < (len(termin_list) - 1):
                x = x + 1
                data.append(["", "", ""])
            j += 1

    return data


# print DB to xls workbook
def print_all(fname):
    # Setup ExcelDatei
    book = xlwt.Workbook()
    sheet = book.add_sheet("Hühnerliste")
    sheet.col(0).width = 256 * 25
    sheet.col(1).width = 256 * 35
    sheet.col(2).width = 256 * 20

    row_numb = 1

    # Kopfzeile
    row = sheet.row(0)
    row.write(0, "Name")
    row.write(1, "Adresse")
    row.write(2, "Telefonnummer")
    row.write(3, "Datum")
    row.write(4, "Anzahl")
    row.write(5, "bezahlt?")

    cur.execute("SELECT * FROM besitzer order by nachname, vorname;")
    connection.commit()

    owners_list = cur.fetchall()

    for owner in owners_list:
        # hohlt sich die Liste der Termine für diesen Besitzer
        besitzer_id = owner[0]
        cur.execute("SELECT datum,anzahlhuehner,bezahlt "
                    "FROM impftermin JOIN besitzer_impftermin bi on impftermin.IID = bi.IID "
                    "WHERE BID = %s ORDER BY datum,anzahlhuehner;", [besitzer_id])
        connection.commit()

        termin_list = cur.fetchall()

        # schreibt Daten des Besitzers in Tabelle
        row = sheet.row(row_numb)
        row.write(0, str(owner[1] + ", " + owner[2]))  # Nachname, Vorname
        row.write(1, str(owner[3] + " " + owner[4] + ", " + owner[5] + " " + owner[6]))  # Adresse
        row.write(2, str(owner[7]))  # Telefonnummer

        j = 0
        while j < len(termin_list):
            for i in range(3):
                # col = chr(ord(startChar) + (7+(3*j)+i)) #berechnung Buchstaben (start Buchstabe + offsetBesitzer +
                # Anzahl der termine * Offset Termine + aktuelle Stelle)
                row.write(3 + i, str(termin_list[j][i]))

            if j < (len(termin_list) - 1):
                row_numb = row_numb + 1
                row = sheet.row(row_numb)
            j += 1

        row_numb = row_numb + 1  # enable for seperation by empty line for entries

    book.save(fname + "/Hühnerliste.xls")
    msg.showinfo("Erfolgreich gespeichert!", "Die Hühner liste wurde erflogreich unter " +
                 fname + "/Hühnerliste.xls gespeichert.")

    return 1


# add a new Owner to DB
# all arguments have to be given, if unknown vname or tel: give None
def add_owner_return_bid(nname: str, plz: str, ortsname: str, strassenname: str, hausnummer: str, vname: str = None,
                         tel: str = None):
    try:  # Test values higher then database constraints
        if (len(nname) > 255) | (len(plz) > 10) | (len(ortsname) > 255) | (len(strassenname) > 255) | (
                len(hausnummer) > 10):
            raise Exception("Wrong Valuesize")
        if vname is not None:
            if len(vname) > 255:
                raise Exception("Wrong Valuesize")
        if tel is not None:
            if len(tel) > 255:
                raise Exception("Wrong Valuesize")
    except Exception as e:
        print(e)
        return -1

    # overloading for unknown vname and tel ( or combinations)
    if (vname is not None) & (tel is not None):
        cur.execute(f"""INSERT INTO besitzer(nachname, vorname, plz, ortsname, strassenname, hausnummer,tel) 
                        VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING bid;""",
                    [nname, vname, plz, ortsname, strassenname, hausnummer, tel])
        connection.commit()
        return cur.fetchone()

    if (vname is None) & (tel is not None):
        cur.execute("""INSERT INTO besitzer (nachname, plz, ortsname, strassenname, hausnummer,tel) 
                        VALUES (%s,%s,%s,%s,%s,%s) RETURNING bid;""",
                    [nname, plz, ortsname, strassenname, hausnummer, tel])
        connection.commit()
        return cur.fetchone()

    if (vname is not None) & (tel is None):
        cur.execute("""INSERT INTO besitzer (nachname, vorname, plz, ortsname, strassenname, hausnummer) 
                        VALUES (%s,%s,%s,%s,%s,%s) RETURNING bid;""",
                    [nname, vname, plz, ortsname, strassenname, hausnummer])
        connection.commit()
        return cur.fetchone()

    if (vname is None) & (tel is None):
        cur.execute("""INSERT INTO besitzer (nachname, plz, ortsname, strassenname, hausnummer) 
                        VALUES (%s,%s,%s,%s,%s) RETURNING bid;""", [nname, plz, ortsname, strassenname, hausnummer])
        connection.commit()
        return cur.fetchone()


def add_termin_return_iid(datum: datetime, huehner: int, bezahlt: bool):
    cur.execute("""INSERT INTO impftermin (datum, anzahlhuehner, bezahlt)
                    VALUES (%s, %s, %s) RETURNING impftermin.IID;""", [datum, huehner, bezahlt])
    connection.commit()
    iid = cur.fetchone()
    return iid[0]
