#!/usr/bin/python3

# Autor: Max Nowak
# Version: 0.5 wip - Cloud Access
# Programm for Manipulation of ChickenList DB
# main Database Access

import psycopg2
import xlwt
from tkinter import messagebox as msg
from datetime import datetime

import os

# establish connection with db // creating db

# for use with postgress

username = os.environ['DBUSER']
hostname = os.environ['DBHOST']
password = os.environ['DBPASSWD']
name = os.environ['DBNAME']

connection = psycopg2.connect(f"user={username} host={hostname} password={password} dbname={name}")

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


# searches db for owners matching provided data
def search(nachname, plz):
    cur.execute("""SELECT BID,vorname,nachname,plz,ortsname,strassenname,hausnummer, tel FROM besitzer
                    WHERE nachname = %s AND plz = %s ORDER BY nachname,vorname;""", [nachname, plz])
    connection.commit()
    owners = cur.fetchall()

    return owners


# gets all info about owner from db
def refresh():
    cur.execute("""SELECT * FROM besitzer ORDER BY nachname,vorname;""")
    connection.commit()

    owners = cur.fetchall()

    return owners


# enquires for all data in dates
def print_termin(bid):
    cur.execute("""Select * FROM impftermin
                            JOIN besitzer_impftermin bi on impftermin.IID = bi.IID
                            WHERE bi.BID = %s
                            ORDER BY datum,anzahlhuehner;""", [bid])
    connection.commit()

    termine = cur.fetchall()

    return termine


# inserts a connection between an owner a date
def commit_termine(bid, iid):
    cur.execute("""INSERT INTO besitzer_impftermin (BID, IID)
                            VALUES (%s,%s);""", [bid, iid])
    connection.commit()


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


# adds a date to db and returns iid for further usage
def add_termin_return_iid(datum: datetime, huehner: int, bezahlt: bool):
    cur.execute("""INSERT INTO impftermin (datum, anzahlhuehner, bezahlt)
                    VALUES (%s, %s, %s) RETURNING impftermin.IID;""", [datum, huehner, bezahlt])
    connection.commit()
    iid = cur.fetchone()
    return iid[0]


# deletes a date from db
def delete_date(iid):
    cur.execute("""DELETE FROM besitzer_impftermin WHERE iid = %s;""", [iid])
    connection.commit()

    cur.execute("""DELETE FROM impftermin WHERE iid = %s;""", [iid])
    connection.commit()


# deletes a owner from db for given bid
def delete_owner(bid):
    cur.execute("""SELECT impftermin.IID FROM impftermin
                        JOIN besitzer_impftermin bi on impftermin.IID = bi.IID
                        JOIN besitzer b on b.BID = bi.BID
                        WHERE b.BID = %s;""", [bid])
    connection.commit()
    iids = cur.fetchall()

    for IID in iids:
        cur.execute("""DELETE FROM besitzer_impftermin
                                       WHERE iid = %s;""", [IID])
        connection.commit()
        cur.execute("""DELETE FROM impftermin
                                            WHERE iid = %s;""", [IID])
        connection.commit()

    cur.execute("""DELETE FROM besitzer
                                WHERE bid = %s;""", [bid])
    connection.commit()


# alter a existing Owner
# all arguments have to be given, if unknown vname or tel: give None
def alter_owner(bid: int, nname: str, plz: str, ortsname: str, strassenname: str, hausnummer: str, vname: str = None,
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

    try:
        # overloading for unknown vname and tel ( or combinations)
        if (vname is not None) & (tel is not None):
            cur.execute(f"""UPDATE besitzer
                            SET vorname = %s,
                            nachname = %s,
                            plz = %s,
                            ortsname = %s,
                            strassenname = %s,
                            hausnummer = %s,
                            tel = %s
                            WHERE BID = %s;""", [vname, nname, plz, ortsname, strassenname, hausnummer, tel, bid])
            connection.commit()
            return cur.fetchone()

        if (vname is None) & (tel is not None):
            cur.execute(f"""UPDATE besitzer
                                    SET nachname = %s,
                                    plz = %s,
                                    ortsname = %s,
                                    strassenname = %s,
                                    hausnummer = %s,
                                    tel = %s
                                    WHERE BID = %s;""", [nname, plz, ortsname, strassenname, hausnummer, tel, bid])
            connection.commit()
            return cur.fetchone()

        if (vname is not None) & (tel is None):
            cur.execute(f"""UPDATE besitzer
                                    SET vorname = %s,
                                    nachname = %s,
                                    plz = %s,
                                    ortsname = %s,
                                    strassenname = %s,
                                    hausnummer = %s
                                    WHERE BID = %s;""", [vname, nname, plz, ortsname, strassenname, hausnummer, bid])
            connection.commit()
            return cur.fetchone()

        if (vname is None) & (tel is None):
            cur.execute(f"""UPDATE besitzer
                                    SET nachname = %s,
                                    plz = %s,
                                    ortsname = %s,
                                    strassenname = %s,
                                    hausnummer = %s
                                    WHERE BID = %s;""", [nname, plz, ortsname, strassenname, hausnummer, bid])
            connection.commit()
            return cur.fetchone()
        return 0
    except Exception as e:
        print(e)
        return -1


# updates paiment information for given iid
def has_paid(iid):
    cur.execute("""UPDATE impftermin
                            SET bezahlt = true
                            WHERE iid = %s;""", [iid])
    connection.commit()


# updates paiment information for given iid
def has_not_paid(iid):
    cur.execute("""UPDATE impftermin
                                    SET bezahlt = false
                                    WHERE iid = %s;""", [iid])
    connection.commit()


# alter a existing termin
def alter_termin(iid: int, datum: datetime, huehner: int, bezahlt: bool):
    try:
        cur.execute("""UPDATE impftermin
                                SET datum = %s,
                                    anzahlhuehner = %s,
                                    bezahlt = %s
                                WHERE IID = %s;""", [datum, huehner, bezahlt, iid])
        connection.commit()

        return 1
    except Exception as e:
        print(e)
        return 0


# searches for the date of the newest impfdate of a given owner
def get_newest_impfdate(bid: int):
    cur.execute("""SELECT datum, impftermin.iid FROM impftermin
                            JOIN besitzer_impftermin bi on impftermin.IID = bi.IID
                            JOIN besitzer b on b.BID = bi.BID
                            WHERE b.BID = %s and datum = (   SELECT max(datum) FROM impftermin
                                                            JOIN besitzer_impftermin bi on impftermin.IID = bi.IID
                                                            JOIN besitzer b on b.BID = bi.BID
                                                            WHERE b.BID = %s);""", [bid, bid])
    connection.commit()
    date = cur.fetchone()

    return date


# searches for the date and amount of chicken of the newest impfdate of a given owner
def get_huehner_date_from_newest_impfdate(bid: int):
    cur.execute("""SELECT anzahlhuehner, datum FROM impftermin
                            JOIN besitzer_impftermin bi on impftermin.IID = bi.IID
                            JOIN besitzer b on b.BID = bi.BID
                            WHERE b.BID = %s and datum = (   SELECT max(datum) FROM impftermin
                                                            JOIN besitzer_impftermin bi on impftermin.IID = bi.IID
                                                            JOIN besitzer b on b.BID = bi.BID
                                                            WHERE b.BID = %s);""", [bid, bid])
    connection.commit()
    termin_data = cur.fetchone()

    return termin_data
