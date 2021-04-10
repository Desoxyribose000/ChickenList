#!/usr/bin/python3

# Autor: Max Nowak
# Version: 0.1
# Programm for Manipulation of ChickenList DB

import psycopg2
import xlwt
import tkinter as tk
import tkinter.filedialog as fdialog
from tksheet import Sheet
from tkinter import ttk
from tkinter import messagebox as msg
import tkcalendar
from datetime import datetime

# establish connection with db // creating db

# for use with postgress
connection = psycopg2.connect("user=#USERNAME# host=#HOST# password=#PASSWORD# dbname=#DBNAME#")

cur = connection.cursor()
cur.execute("""SET SCHEMA 'chickenlist';""")

connection.commit()


# GUI
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)


# preview entire db and Print to xls file in given directory
class P_ViewAllPrintAll(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        labelBox = tk.Frame(master=self)
        labelBox.pack(side="top", fill="x", padx="5", pady="5")
        label = tk.Label(labelBox, text="Vorschau und Drucken", font=55)
        label.pack(fill="x", side="left")

        data = getAll()  # get Data from DB

        self.rahmenoben = tk.Frame(master=self)
        self.rahmenoben.pack(expand=True, fill="both", padx='5', pady='5')

        self.sheet = Sheet(self.rahmenoben,
                           page_up_down_select_row=True,
                           data=data,
                           column_width=100,
                           show_x_scrollbar=False,
                           width=1200)
        self.sheet.pack(fill="both", expand=True)
        self.sheet.column_width(0, width=300)
        self.sheet.column_width(1, width=350)
        self.sheet.column_width(2, width=150)

        self.button = tk.Button(self, text="Als Datei Speichern", command=(lambda: self.selectDir()))
        self.button.pack(side="left", padx="10", pady="10")

    def refresh(self):
        data = getAll()
        self.sheet.data_reference(newdataref=data)
        self.sheet.column_width(0, width=300)
        self.sheet.column_width(1, width=350)
        self.sheet.column_width(2, width=150)
        self.sheet.column_width(4, width=100)
        self.sheet.column_width(5, width=100)

    def show(self):
        self.refresh()
        self.lift()
        root.title("Hühnerliste - Vorschau und Drucken")

    @staticmethod
    def selectDir():
        fname = fdialog.askdirectory()
        printAll(fname)


# add new Owner
class P_Owner(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        labelBox = tk.Frame(master=self)
        labelBox.pack(side="top", fill="x", padx="5", pady="5")
        label = tk.Label(labelBox, text="Einen Neuen Besitzer hinzufügen", font=55)
        label.pack(fill="x", side="left")

        ownerBox = tk.Frame(master=self, borderwidth=2, relief="groove")
        ownerBox.pack(side="top", fill="x", padx="5",
                      pady="5")  # ownerBox = tk.Frame(self, relief="groove").pack(side="top", fill="both", padx="5", pady="5", expand=True)

        NameBox = tk.Frame(ownerBox)
        NameBox.pack(side="top", fill="x", pady=5)

        VNameBox = tk.Frame(NameBox)
        VNameBox.pack(side="left", fill="x")
        L_vname = tk.Label(VNameBox, text="Vorname").pack(side="left", padx="5")
        self.E_vname = tk.Entry(VNameBox)
        self.E_vname.pack(side="left", padx="5")

        NNameBox = tk.Frame(NameBox)
        NNameBox.pack(side="left", fill="x")
        L_nname = tk.Label(NNameBox, text="Nachname *").pack(side="left", padx="5")
        self.E_nname = tk.Entry(NNameBox)
        self.E_nname.pack(side="left", padx="5")

        AdressBox = tk.Frame(ownerBox)
        AdressBox.pack(side="top", fill="x", pady=5)

        PLZBox = tk.Frame(AdressBox)
        PLZBox.pack(side="left", fill="x")
        L_PLZ = tk.Label(PLZBox, text="PLZ *").pack(side="left", padx="5")
        self.E_PLZ = tk.Entry(PLZBox)
        self.E_PLZ.pack(side="left", padx="25")

        OrtBox = tk.Frame(AdressBox)
        OrtBox.pack(side="left", fill="x")
        L_Ort = tk.Label(OrtBox, text="Ort *").pack(side="left", padx="5")
        self.E_Ort = tk.Entry(OrtBox)
        self.E_Ort.pack(side="left", padx="25")

        StrasseBox = tk.Frame(AdressBox)
        StrasseBox.pack(side="left", fill="x")
        L_Strasse = tk.Label(StrasseBox, text="Strasse *").pack(side="left", padx="5")
        self.E_Strasse = tk.Entry(StrasseBox)
        self.E_Strasse.pack(side="left", padx="5")

        HausBox = tk.Frame(AdressBox)
        HausBox.pack(side="left", fill="x")
        L_Haus = tk.Label(HausBox, text="Hausnummer *").pack(side="left", padx="5")
        self.E_Haus = tk.Entry(HausBox)
        self.E_Haus.pack(side="left", padx="5")

        TelBox = tk.Frame(ownerBox)
        TelBox.pack(side="top", fill="x", pady=5)

        L_Tel = tk.Label(TelBox, text="Telefonnummer").pack(side="left", padx="5")
        self.E_Tel = tk.Entry(TelBox)
        self.E_Tel.pack(side="left", padx="5")

        DisclaimerBox = tk.Frame(master=self)
        DisclaimerBox.pack(side="top", fill="x", padx="5", pady="5")
        L_vname = tk.Label(DisclaimerBox, text="* sind Pflichtfelder").pack(side="left", padx="5")

        ButtonBox = tk.Frame(master=self)
        ButtonBox.pack(side="top", fill="x", padx="5", pady="5")

        addDate = tk.IntVar()
        terminBox = tk.Frame(master=self, borderwidth=2, relief="groove")

        DatumBox = tk.Frame(master=terminBox)

        self.thisDate = tk.IntVar()
        self.thisDate.set(1)
        L_Datum = tk.Label(DatumBox, text="Datum: ")
        RB_thisDateTrue = tk.Radiobutton(master=DatumBox, text='heute', value='1', variable=self.thisDate)
        L_Oder = tk.Label(DatumBox, text="oder")
        RB_thisDateFalse = tk.Radiobutton(master=DatumBox, text='anderes Datum', value='0', variable=self.thisDate)
        self.day = tk.IntVar()
        self.day.set(1)
        Sb_day = ttk.Spinbox(DatumBox, from_=1, to=31, textvariable=self.day, width=5)
        self.month = tk.IntVar()
        self.month.set(1)
        Sb_month = ttk.Spinbox(DatumBox, from_=1, to=12, textvariable=self.month, width=5)
        self.year = tk.IntVar()
        self.year.set(2021)
        Sb_year = ttk.Spinbox(DatumBox, from_=2019, to=2030, textvariable=self.year, width=5)

        HuehnerBox = tk.Frame(master=terminBox)
        L_Huehner = tk.Label(HuehnerBox, text="Anzahl der Hühner: ")
        self.E_Huehner = tk.Entry(HuehnerBox)

        PaidBox = tk.Frame(master=terminBox)
        L_Paid = tk.Label(PaidBox, text="bezahlt: ")
        self.paid = tk.IntVar()
        CB_Paid = tk.Checkbutton(PaidBox, text="", variable=self.paid)

        # terminBox.pack(side="top", fill="x", padx="5", pady="5")
        # DatumBox.pack(side="top", fill="x", pady="5")
        # L_Datum.pack(side="left", padx="5")
        # RB_thisDateTrue.pack(side="left", padx="5")
        # L_Oder.pack(side="left", padx="5")
        # RB_thisDateFalse.pack(side="left", padx="5")
        # Sb_day.pack(side="left", padx="5")
        # Sb_month.pack(side="left", padx="5")
        # Sb_year.pack(side="left", padx="5")
        # HuehnerBox.pack(side="top", fill="x", pady="5")
        # L_Huehner.pack(side="left", padx="5")
        # E_Huehner.pack(side="left", padx="5")
        # PaidBox.pack(side="top", fill="x", pady="5")
        # L_Paid.pack(side="left", padx="5")
        # CB_Paid.pack(side="left")

        StatusBox = tk.Frame(master=self)
        StatusBox.pack(side="top", fill="x", padx="5", pady="5")

        self.StatusText = tk.StringVar()
        L_State = tk.Label(StatusBox, textvariable=self.StatusText)
        L_State.pack(side="left", pady="5")

        # terminBox, the outer Box needs to be first
        List = [terminBox, DatumBox, L_Datum, RB_thisDateTrue, L_Oder, RB_thisDateFalse, Sb_day,
                Sb_month, Sb_year, HuehnerBox, L_Huehner, self.E_Huehner, PaidBox, L_Paid, CB_Paid]

        # used to check if Termin shall be displayed, calls funtion to dynamicly pack and unpack it
        CB_addDate = tk.Checkbutton(ButtonBox, text="Ein Impfdatum ebenfalls hinzufügen", variable=addDate,
                                    command=(lambda: self.packTermin(List, addDate.get())))

        B_AddButton = tk.Button(ButtonBox, text="Hinzufügen",
                                command=(lambda: self.testInput(addDate.get())))  # (lambda: addOwner())

        B_AddButton.pack(side="left")
        CB_addDate.pack(side="left")

    # pack or packforget for the List of all Elemnts needed to display Termin
    def packTermin(self, List, isAddDate):
        if isAddDate:
            for i in range(len(List)):
                if i == 0:
                    List[i].pack(side="top", fill="x", padx="5", pady="5")
                    continue
                if isinstance(List[i], tk.Frame):
                    List[i].pack(side="top", fill="x", pady="5")
                else:
                    List[i].pack(side="left", padx="5")
        else:
            for item in List:
                item.pack_forget()

    def testInput(self, isAddDate):
        validInput = True

        if isAddDate == 1:
            if self.day == None:
                validInput = False
            if self.month == None:
                validInput = False
            if self.year == None:
                validInput = False
            Huehner = self.E_Huehner.get()
            Huehner.replace(" ", "")
            if not (Huehner.isnumeric()):
                validInput = False

        PLZ = self.E_PLZ.get()
        PLZ = PLZ.replace(" ", "")
        if not (PLZ.isnumeric()):
            validInput = False

        if len(self.E_Tel.get()) > 0:
            Tel = self.E_Tel.get()
            Tel = Tel.replace(" ", "")
            if not (Tel.isnumeric()):
                validInput = False

        EntryList = [self.E_nname, self.E_PLZ, self.E_Ort, self.E_Strasse, self.E_Haus]

        if isAddDate == 1:
            EntryList.append(self.E_Huehner)
            try:
                dateString = str(self.year.get()) + "-" + str(self.month.get()) + "-" + str(self.day.get())
                Datum = datetime.strptime(dateString, '%Y-%m-%d')
            except Exception as e:
                msg.showerror("Fehlerhaftes Datum!", message="Das von Ihnen eingebene Datum enthält Fehler!\n" + str(e))
                validInput = False

        isEmpty = False
        for Entry in EntryList:
            if len(Entry.get()) == 0:
                isEmpty = True
        if isEmpty:
            self.StatusText.set("Bitte fülle alle Pflichtfelder und achte auf sinnvolle Eingaben!")
            validInput = False

        if validInput:
            # Build Dicttionary of Owner values
            OwnerDict = {
                'Vorname': self.E_vname.get().replace(" ", ""),
                'Nachname': self.E_nname.get().replace(" ", ""),
                'PLZ': self.E_PLZ.get().replace(" ", ""),
                'Ort': self.E_Ort.get().replace(" ", ""),
                'Strasse': self.E_Strasse.get().replace(" ", ""),
                'Hausnummer': self.E_Haus.get().replace(" ", ""),
                'Telefonnummer': self.E_Tel.get().replace(" ", "")
            }

            # Build Dictionary of Termin related values if Termin is true
            if isAddDate == 0:
                TerminDict = None
            else:
                if self.thisDate.get() == 1:
                    dateString = datetime.today().strftime('%Y-%m-%d')
                    Datum = datetime.strptime(dateString, '%Y-%m-%d')
                else:
                    if self.thisDate.get() == 0:
                        dateString = str(self.year.get()) + "-" + str(self.month.get()) + "-" + str(self.day.get())
                        Datum = datetime.strptime(dateString, '%Y-%m-%d')
                TerminDict = {
                    'Datum': Datum,
                    'Huehner': int(self.E_Huehner.get().replace(" ", "")),
                    'bezahlt': bool(self.paid.get())
                }
            self.commitOwner(OwnerDict, isAddDate, TerminDict)
        else:
            self.StatusText.set("Bitte fülle alle Pflichtfelder und achte auf sinnvolle Eingaben!")

    def commitOwner(self, OwnerDict, isAddTermin, TerminDict=None):
        if isAddTermin == 0:
            addOwnerReturnBID(OwnerDict['Nachname'], OwnerDict['PLZ'], OwnerDict['Ort'], OwnerDict['Strasse'],
                              OwnerDict['Hausnummer'], OwnerDict['Vorname'], OwnerDict['Telefonnummer'])
            self.StatusText.set("Besitzer " + str(OwnerDict) + " wurde hinzugefügt!")
        else:
            BID = addOwnerReturnBID(OwnerDict['Nachname'], OwnerDict['PLZ'], OwnerDict['Ort'], OwnerDict['Strasse'],
                                    OwnerDict['Hausnummer'], OwnerDict['Vorname'], OwnerDict['Telefonnummer'])
            if BID == -1:
                raise Exception("Fehler")

            IID = addTerminReturnIID(TerminDict['Datum'], TerminDict['Huehner'], TerminDict['bezahlt'])

            # cur.execute("""SELECT bid FROM besitzer WHERE nachname=%s and plz=%s and ortsname=%s and strassenname=%s and
            #                 hausnummer=%s""",[OwnerDict['Nachname'], OwnerDict['PLZ'], OwnerDict['Ort'],
            #                                   OwnerDict['Strasse'], OwnerDict['Hausnummer']])
            # connection.commit()
            # BID = cur.fetchone()

            # cur.execute("""SELECT iid FROM impftermin WHERE datum=%s and anzahlhuehner=%s and bezahlt=%s""",
            #                 [TerminDict['Datum'],TerminDict['Huehner'],TerminDict['bezahlt']])
            # connection.commit()
            # IID = cur.fetchone()

            cur.execute("""INSERT INTO besitzer_impftermin (BID, IID) VALUES (%s,%s);""",
                        [BID, IID])
            connection.commit()

            self.StatusText.set("Besitzer " + str(OwnerDict) + " wurde hinzugefügt!\n" +
                                "Termin " + str(TerminDict) + " wurde hinzugefügt!\n" +
                                "Besitzer " + str(BID) + " und Termin " + str(IID) + " wurde assoziert!")

    def show(self):
        self.lift()
        root.title("Hühnerliste - Besitzer hinzufügen")


# add appointment for one owner
class P_AddTerminOne(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.isSearch = False
        self.isConfirm = False
        self.isDistinct = None
        self.Owners = None
        self.Owner = None

        labelBox = tk.Frame(master=self)
        labelBox.pack(side="top", fill="x", padx="5", pady="5")
        label = tk.Label(labelBox, text="Einem Besitzer einen neuen Termin hinzufügen", font=55)
        label.pack(fill="x", side="left")

        self.searchBox = tk.Frame(master=self, borderwidth=2, relief="groove")
        self.searchBox.pack(side="top", fill="x", padx="5", pady="5")

        nameBox = tk.Frame(master=self.searchBox)
        nameBox.pack(side="top", fill="x", pady=5)
        L_vname = tk.Label(nameBox, text="Nachname: ").pack(side="left", padx="5")
        self.E_nname = tk.Entry(nameBox)
        self.E_nname.pack(side="left", padx="5")

        plzBox = tk.Frame(master=self.searchBox)
        plzBox.pack(side="top", fill="x", pady=5)
        L_plz = tk.Label(plzBox, text="PLZ: ").pack(side="left", padx="5")
        self.E_plz = tk.Entry(plzBox)
        self.E_plz.pack(side="left", padx="43")

        ButtonBox = tk.Frame(master=self.searchBox)
        ButtonBox.pack(side="top", fill="x", padx="5", pady="5")

        B_SearchButton = tk.Button(ButtonBox, text="Suche", command=(
            lambda: self.search(self.E_nname.get().replace(" ", ""), self.E_plz.get().replace(" ", ""))))
        B_SearchButton.pack(side="left")
        self.SearchStatusText = tk.StringVar()
        self.SearchStatusText.set("")
        L_State = tk.Label(ButtonBox, textvariable=self.SearchStatusText)
        L_State.pack(side="left", pady="5", padx="20")

        self.confirmBox = tk.Frame(master=self.searchBox, borderwidth=2, relief="groove")
        self.confirmLabelBox = tk.Frame(master=self.confirmBox)
        self.L_confirmTitle = tk.Label(self.confirmLabelBox, text="")
        self.confirmOwnersBox = tk.Frame(master=self.confirmBox)
        self.confirmButtonBox = tk.Frame(master=self.confirmBox)
        self.B_ConfirmButton = tk.Button(self.confirmButtonBox, text="Auswählen")

        self.RadiobuttonBoxList = []
        self.RadiobuttonList = []
        self.choosenOwner = tk.IntVar()
        self.choosenOwner.set(0)

        terminBox = tk.Frame(master=self)
        terminBox.pack(side="top", fill="x", padx="5", pady="5")

        ownerBox = tk.Frame(master=terminBox)
        ownerBox.pack(side="top", fill="x", pady=5)
        ownerLabelBox = tk.Frame(master=ownerBox)
        ownerLabelBox.pack(side="top", fill="x", pady=5)
        L_ownerTitle = tk.Label(ownerLabelBox, text="Besitzer: ").pack(side="left", padx="5")
        self.OwnerLabelText = tk.StringVar()
        self.OwnerLabelText.set("unbekannt")
        L_Owner = tk.Label(ownerLabelBox, textvariable=self.OwnerLabelText)
        L_Owner.pack(side="left", pady="10")

        # .pack(side="top", fill="x", padx="5", pady="5")
        # .pack(side="top", fill="x", pady="5")
        # .pack(side="left", padx="5")

        # Termin hinzufügen

        DatumBox = tk.Frame(master=terminBox)
        DatumBox.pack(side="top", fill="x", pady="5")

        self.thisDate = tk.IntVar()
        self.thisDate.set(1)
        L_Datum = tk.Label(DatumBox, text="Datum: ")
        L_Datum.pack(side="left", padx="5")
        RB_thisDateTrue = tk.Radiobutton(master=DatumBox, text='heute', value='1', variable=self.thisDate)
        RB_thisDateTrue.pack(side="left", padx="5")
        L_Oder = tk.Label(DatumBox, text="oder")
        L_Oder.pack(side="left", padx="5")
        RB_thisDateFalse = tk.Radiobutton(master=DatumBox, text='anderes Datum', value='0', variable=self.thisDate)
        RB_thisDateFalse.pack(side="left", padx="5")
        self.day = tk.IntVar()
        self.day.set(1)
        Sb_day = ttk.Spinbox(DatumBox, from_=1, to=31, textvariable=self.day, width=5)
        Sb_day.pack(side="left", padx="5")
        self.month = tk.IntVar()
        self.month.set(1)
        Sb_month = ttk.Spinbox(DatumBox, from_=1, to=12, textvariable=self.month, width=5)
        Sb_month.pack(side="left", padx="5")
        self.year = tk.IntVar()
        self.year.set(2021)
        Sb_year = ttk.Spinbox(DatumBox, from_=2019, to=2030, textvariable=self.year, width=5)
        Sb_year.pack(side="left", padx="5")

        HuehnerBox = tk.Frame(master=terminBox)
        HuehnerBox.pack(side="top", fill="x", pady="5")
        L_Huehner = tk.Label(HuehnerBox, text="Anzahl der Hühner: ")
        L_Huehner.pack(side="left", padx="5")
        self.E_Huehner = tk.Entry(HuehnerBox)
        self.E_Huehner.pack(side="left", padx="5")

        PaidBox = tk.Frame(master=terminBox)
        PaidBox.pack(side="top", fill="x", pady="5")
        L_Paid = tk.Label(PaidBox, text="bezahlt: ")
        L_Paid.pack(side="left", padx="5")
        self.paid = tk.IntVar()
        CB_Paid = tk.Checkbutton(PaidBox, text="", variable=self.paid)
        CB_Paid.pack(side="left", padx="5")

        CommitButtonBox = tk.Frame(master=terminBox)
        CommitButtonBox.pack(side="top", fill="x", padx="5", pady="5")

        self.B_CommitButton = tk.Button(CommitButtonBox, text="Speichern",
                                        command=(lambda: self.testInput(self.Owner[0])))
        self.B_CommitButton.config(state="disabled")
        self.B_CommitButton.pack(side="left")

        StatusBox = tk.Frame(master=self)
        StatusBox.pack(side="top", fill="x", padx="5", pady="5")

        self.StatusText = tk.StringVar()
        L_State = tk.Label(StatusBox, textvariable=self.StatusText)
        L_State.pack(side="left", pady="5")

    def testInput(self, BID):
        validInput = True

        if self.day == None:
            validInput = False
        if self.month == None:
            validInput = False
        if self.year == None:
            validInput = False
        if not (self.E_Huehner.get().replace(" ", "").isnumeric()):
            validInput = False

        isEmpty = False
        if len(self.E_Huehner.get()) == 0:
            isEmpty = True
        if isEmpty:
            self.StatusText.set("Bitte gebe die Anzahl der Hühner an!")
            validInput = False

        try:
            dateString = str(self.year.get()) + "-" + str(self.month.get()) + "-" + str(self.day.get())
            Datum = datetime.strptime(dateString, '%Y-%m-%d')
        except Exception as e:
            msg.showerror("Fehlerhaftes Datum!", message="Das von Ihnen eingebene Datum enthält Fehler!\n" + str(e))
            validInput = False

        if validInput & self.isConfirm:
            # Build Dictionary of Termin related values if Termin is true
            if self.thisDate.get() == 1:
                dateString = datetime.today().strftime('%Y-%m-%d')
                Datum = datetime.strptime(dateString, '%Y-%m-%d')
            else:
                dateString = str(self.year.get()) + "-" + str(self.month.get()) + "-" + str(self.day.get())
                Datum = datetime.strptime(dateString, '%Y-%m-%d')

            TerminDict = {
                'Datum': Datum,
                'Huehner': int(self.E_Huehner.get().replace(" ", "")),
                'bezahlt': bool(self.paid.get())
            }
            self.commitTermin(BID, TerminDict)
        else:
            self.StatusText.set("Bitte prüfe deine Eingabe oder Suche zuerst nach einem Besitzer!")

    def commitTermin(self, BID, TerminDict):
        IID = addTerminReturnIID(TerminDict['Datum'], TerminDict['Huehner'], TerminDict['bezahlt'])
        cur.execute("""INSERT INTO besitzer_impftermin (BID, IID) VALUES (%s,%s);""",
                    [BID, IID])
        connection.commit()

        self.StatusText.set("Termin " + str(TerminDict) + " wurde hinzugefügt!\n" +
                            "Besitzer " + str(BID) + " und Termin " + str(IID) + " wurde assoziert!")

    def search(self, Nachname: str, PLZ: str):
        Nachname = Nachname.replace(" ", "")
        PLZ = PLZ.replace(" ", "")

        cur.execute("""SELECT BID,vorname,nachname,plz,ortsname,strassenname,hausnummer, tel FROM besitzer
                    WHERE nachname = %s AND plz = %s ORDER BY nachname,vorname;""", [Nachname, PLZ])
        connection.commit()
        self.Owners = cur.fetchall()

        if self.Owners == []:
            self.confirmBox.pack_forget()
            self.confirmLabelBox.pack_forget()
            self.L_confirmTitle.pack_forget()
            self.confirmOwnersBox.pack_forget()
            self.B_ConfirmButton.pack_forget()
            self.confirmButtonBox.pack_forget()

            for RadiobuttonBox in self.RadiobuttonBoxList:
                RadiobuttonBox.pack_forget()

            for Radiobutton in self.RadiobuttonList:
                Radiobutton.pack_forget()
            self.SearchStatusText.set(
                "Es ist ein Fehler aufgetreten! Bitte prüfe deine Eingabe und versuche es nochmal")
        else:
            self.SearchStatusText.set("Got: " + str(self.Owners))

            if len(self.Owners) > 1:
                self.isDistinct = False
            if len(self.Owners) == 1:
                self.isDistinct = True
            if self.isDistinct != None:
                self.isSearch == True

            if self.isDistinct == False:
                self.confirmBox.pack_forget()
                self.confirmLabelBox.pack_forget()
                self.L_confirmTitle.pack_forget()
                self.confirmOwnersBox.pack_forget()
                self.B_ConfirmButton.pack_forget()
                self.confirmButtonBox.pack_forget()

                self.L_confirmTitle.config(text=str(len(self.Owners)) + " Besitzer gefunden:")

                self.confirmBox.pack(side="top", fill="x", padx="5", pady="5")
                self.confirmLabelBox.pack(side="top", fill="x", pady="5")
                self.L_confirmTitle.pack(side="left", padx="5")
                self.confirmOwnersBox.pack(side="top", fill="x", pady="5")

                for RadiobuttonBox in self.RadiobuttonBoxList:
                    RadiobuttonBox.pack_forget()

                for Radiobutton in self.RadiobuttonList:
                    Radiobutton.pack_forget()

                self.RadiobuttonBoxList = []
                self.RadiobuttonList = []
                self.choosenOwner = tk.IntVar()
                self.choosenOwner.set(0)

                i = 0
                for Owner in self.Owners:
                    self.RadiobuttonBoxList.append(tk.Frame(master=self.confirmOwnersBox))
                    self.RadiobuttonList.append(
                        tk.Radiobutton(master=self.RadiobuttonBoxList[i], text=str(Owner), variable=self.choosenOwner,
                                       value=i))
                    self.RadiobuttonBoxList[i].pack(side="top", fill="x", pady="5")
                    self.RadiobuttonList[i].pack(side="left", padx="5")
                    i += 1

                self.B_ConfirmButton.configure(command=lambda: self.confirm(self.Owners[self.choosenOwner.get()]))
                self.confirmButtonBox.pack(side="top", fill="x", pady="5")
                self.B_ConfirmButton.pack(side="left", padx="5")

            else:
                self.confirm(self.Owners[0])
                self.confirmBox.pack_forget()
                self.confirmLabelBox.pack_forget()
                self.L_confirmTitle.pack_forget()
                self.confirmOwnersBox.pack_forget()
                self.B_ConfirmButton.pack_forget()
                self.confirmButtonBox.pack_forget()
                for RadiobuttonBox in self.RadiobuttonBoxList:
                    RadiobuttonBox.pack_forget()

                for Radiobutton in self.RadiobuttonList:
                    Radiobutton.pack_forget()

    def confirm(self, Owner):
        self.Owner = Owner
        self.isConfirm = True
        self.B_CommitButton.config(state="normal")
        self.OwnerLabelText.set(str(self.Owner[1]) + " " + str(self.Owner[2]) + ": " +
                                str(self.Owner[3]) + " " + str(self.Owner[4]) + " " + str(self.Owner[5]) + " " +
                                str(self.Owner[6]) + " - " + str(self.Owner[7]))

    def show(self):
        self.lift()
        root.title("Hühnerliste - Termin hinzufügen - Ein Besitzer")


# add appointments of the same day for multiple owners
# TOO DOO Refresh Table on lift
class P_AddTerminMultiple(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        cur.execute("""SELECT * FROM besitzer
                               ORDER BY nachname,vorname;""")
        connection.commit()

        self.owners = cur.fetchall()

        labelBox = tk.Frame(master=self)
        labelBox.pack(side="top", fill="x", padx="5", pady="5")
        label = tk.Label(labelBox, text="Einem Besitzer einen neuen Termin hinzufügen", font=55)
        label.pack(fill="x", side="left")

        DatumBox = tk.Frame(master=self)
        DatumBox.pack(side="top", fill="x", pady="5")

        # get a date
        self.thisDate = tk.IntVar()
        self.thisDate.set(1)
        L_Datum = tk.Label(DatumBox, text="Datum: ")
        L_Datum.pack(side="left", padx="5")
        RB_thisDateTrue = tk.Radiobutton(master=DatumBox, text='heute', value='1', variable=self.thisDate)
        RB_thisDateTrue.pack(side="left", padx="5")
        L_Oder = tk.Label(DatumBox, text="oder")
        L_Oder.pack(side="left", padx="5")
        RB_thisDateFalse = tk.Radiobutton(master=DatumBox, text='anderes Datum', value='0', variable=self.thisDate)
        RB_thisDateFalse.pack(side="left", padx="5")
        self.day = tk.IntVar()
        self.day.set(1)
        Sb_day = ttk.Spinbox(DatumBox, from_=1, to=31, textvariable=self.day, width=5)
        Sb_day.pack(side="left", padx="5")
        self.month = tk.IntVar()
        self.month.set(1)
        Sb_month = ttk.Spinbox(DatumBox, from_=1, to=12, textvariable=self.month, width=5)
        Sb_month.pack(side="left", padx="5")
        self.year = tk.IntVar()
        self.year.set(2021)
        Sb_year = ttk.Spinbox(DatumBox, from_=2019, to=2030, textvariable=self.year, width=5)
        Sb_year.pack(side="left", padx="5")

        # scrollable List of Chechkbuttons for all owners
        scrollContainerFrame = ttk.Frame(self, borderwidth=2, relief="groove")
        canvas = tk.Canvas(scrollContainerFrame, height=400, highlightthickness=0)
        scrollbar = ttk.Scrollbar(scrollContainerFrame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        scrollContainerFrame.pack(side="top", fill="x", padx="5", pady="5")
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # on change of contentlength edit scrollregion
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # tell the canvas to draw the frame as window starting from top-left
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)



        self.checkVarList = []
        self.checkBoxList = []
        self.checkButtonBoxList = []
        self.terminBoxList = []
        self.E_huehnerList = []
        self.L_huehnerList = []
        self.paidVar = []
        self.CB_paidList = []
        self.L_PaidList = []
        self.checkButtonList = []

        i = 0
        for owner in self.owners:
            self.checkVarList.append(tk.IntVar())
            self.checkBoxList.append(tk.Frame(self.scrollable_frame))
            self.checkButtonBoxList.append(tk.Frame(self.checkBoxList[i]))
            self.terminBoxList.append(tk.Frame(self.checkBoxList[i]))
            self.checkButtonList.append(tk.Checkbutton(self.checkButtonBoxList[i],
                                                       text=str(owner[1]) + ", " + str(owner[2]) + ": " + str(
                                                           owner[3]) + " " +
                                                            str(owner[4]) + " " + str(owner[5]) + " " + str(
                                                           owner[6]) + " - " +
                                                            str(owner[7]),
                                                       variable=self.checkVarList[i], onvalue=1, offvalue=0))
            self.L_huehnerList.append(tk.Label(self.terminBoxList[i], text="Hühner: "))
            self.E_huehnerList.append(tk.Entry(self.terminBoxList[i]))
            self.L_PaidList.append(tk.Label(self.terminBoxList[i], text="bezahlt: "))
            self.paidVar.append(tk.IntVar())
            self.CB_paidList.append(tk.Checkbutton(self.terminBoxList[i], text="", variable=self.paidVar[i]))

            self.checkButtonBoxList[i].pack(side="left")
            self.terminBoxList[i].pack(side="right")
            self.checkButtonList[i].pack(side="left")

            self.L_huehnerList[i].pack(side="left", padx="5")
            self.E_huehnerList[i].pack(side="left", padx="5")
            self.L_PaidList[i].pack(side="left", padx="5")
            self.CB_paidList[i].pack(side="left", padx="5")
            self.checkBoxList[i].pack(side="top", fill="x")
            i += 1

        CommitButtonBox = tk.Frame(master=self)
        CommitButtonBox.pack(side="top", fill="x", padx="5", pady="5")

        self.B_CommitButton = tk.Button(CommitButtonBox, text="Füge Termine hinzu!",
                                        command=(lambda: self.prepareData()))
        self.B_CommitButton.pack(side="left")

        if self.owners == []:
            self.B_CommitButton.config(state="disabled")

        # scrollable StatusBox for longStatus
        StatusContainerFrame = ttk.Frame(self, borderwidth=2, relief="groove")
        StatusCanvas = tk.Canvas(StatusContainerFrame, height=400)
        StatusScrollbar = ttk.Scrollbar(StatusContainerFrame, orient="vertical", command=StatusCanvas.yview)
        self.StatusBox = ttk.Frame(StatusCanvas)

        StatusContainerFrame.pack(side="top", fill="x", padx="5", pady="5")
        StatusCanvas.pack(side="left", fill="both", expand=True)
        StatusScrollbar.pack(side="right", fill="y")

        # on change of contentlength edit scrollregion
        self.StatusBox.bind(
            "<Configure>",
            lambda e: StatusCanvas.configure(
                scrollregion=StatusCanvas.bbox("all")
            )
        )

        # tell the canvas to draw the frame as window starting from top-left
        StatusCanvas.create_window((0, 0), window=self.StatusBox, anchor="nw")
        StatusCanvas.configure(yscrollcommand=StatusScrollbar.set)

        self.StatusText = tk.StringVar()
        L_State = tk.Label(self.StatusBox, textvariable=self.StatusText)
        L_State.pack(side="left", pady="5")

    def commitTermine(self, data):
        self.StatusText.set("")

        if self.thisDate.get() == 1:
            dateString = datetime.today().strftime('%Y-%m-%d')
            Datum = datetime.strptime(dateString, '%Y-%m-%d')
        else:
            dateString = str(self.year.get()) + "-" + str(self.month.get()) + "-" + str(self.day.get())
            Datum = datetime.strptime(dateString, '%Y-%m-%d')

        for entry in data:
            IID = str(addTerminReturnIID(Datum, entry[1], bool(entry[2])))
            BID = str(entry[0])
            cur.execute("""INSERT INTO besitzer_impftermin (BID, IID)
                            VALUES (%s,%s);""", [BID, IID])
            connection.commit()
            StatusText = self.StatusText.get()
            self.StatusText.set(StatusText + "\n" + "Besitzer Nr.: " + BID + " wurde ein Termin am " +
                                datetime.strftime(Datum, "%d.%m.%Y") + " für " +
                                str(entry[1]) + " Hühner hinzugefügt!")

    def prepareData(self):
        data = []  # data structure: [[BID,anzahlhuener,bezahlt],...]

        validInput = True

        if self.day == None:
            validInput = False
        if self.month == None:
            validInput = False
        if self.year == None:
            validInput = False

        try:
            dateString = str(self.year.get()) + "-" + str(self.month.get()) + "-" + str(self.day.get())
            Datum = datetime.strptime(dateString, '%Y-%m-%d')
        except Exception as e:
            msg.showerror("Fehlerhaftes Datum!", message="Das von Ihnen eingebene Datum enthält Fehler!\n" + str(e))
            validInput = False

        i = 0
        for checkButton in self.checkButtonList:
            if self.checkVarList[i].get() == 1:

                Huehner = self.E_huehnerList[i].get()
                Huehner = Huehner.replace(" ", "")

                if len(Huehner) == 0:
                    validInput = False

                if not (Huehner.isnumeric()):
                    validInput = False

                data.append([self.owners[i][0], Huehner, self.paidVar[i].get()])
            i += 1

        if validInput:
            self.commitTermine(data)
        else:
            self.StatusText.set("Bitte prüfe deine Eingabe auf vollständigkeit!")

    def show(self):
        self.lift()
        root.title("Hühnerliste - Termin hinzufügen - mehrere Besitzer")


# Page Confirm Payment - user can validate or invalidate a payment of one appointment
class P_ConfirmPayment(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.isSearch = False
        self.isConfirm = False
        self.isDistinct = None
        self.Owners = None
        self.Owner = None

        labelBox = tk.Frame(master=self)
        labelBox.pack(side="top", fill="x", padx="5", pady="5")
        label = tk.Label(labelBox, text="Zahlungen eines Besitzers bearbeiten", font=55)
        label.pack(fill="x", side="left")

        self.searchBox = tk.Frame(master=self, borderwidth=2, relief="groove")
        self.searchBox.pack(side="top", fill="x", padx="5", pady="5")

        nameBox = tk.Frame(master=self.searchBox)
        nameBox.pack(side="top", fill="x", pady=5)
        L_vname = tk.Label(nameBox, text="Nachname: ").pack(side="left", padx="5")
        self.E_nname = tk.Entry(nameBox)
        self.E_nname.pack(side="left", padx="5")

        plzBox = tk.Frame(master=self.searchBox)
        plzBox.pack(side="top", fill="x", pady=5)
        L_plz = tk.Label(plzBox, text="PLZ: ").pack(side="left", padx="5")
        self.E_plz = tk.Entry(plzBox)
        self.E_plz.pack(side="left", padx="43")

        ButtonBox = tk.Frame(master=self.searchBox)
        ButtonBox.pack(side="top", fill="x", padx="5", pady="5")

        B_SearchButton = tk.Button(ButtonBox, text="Suche",
                                   command=(lambda: self.search(self.E_nname.get().replace(" ", ""),
                                                                self.E_plz.get().replace(" ", ""))))
        B_SearchButton.pack(side="left")
        self.SearchStatusText = tk.StringVar()
        self.SearchStatusText.set("")
        L_State = tk.Label(ButtonBox, textvariable=self.SearchStatusText)
        L_State.pack(side="left", pady="5", padx="20")

        self.confirmBox = tk.Frame(master=self.searchBox, borderwidth=2, relief="groove")
        self.confirmLabelBox = tk.Frame(master=self.confirmBox)
        self.L_confirmTitle = tk.Label(self.confirmLabelBox, text="")
        self.confirmOwnersBox = tk.Frame(master=self.confirmBox)
        self.confirmButtonBox = tk.Frame(master=self.confirmBox)
        self.B_ConfirmButton = tk.Button(self.confirmButtonBox, text="Auswählen")

        self.RadiobuttonBoxList = []
        self.RadiobuttonList = []
        self.choosenOwner = tk.IntVar()
        self.choosenOwner.set(0)

        self.TerminBox = tk.Frame(master=self)
        self.TerminBox.pack(side="top", fill="x", padx="5", pady="5")

        ownerBox = tk.Frame(master=self.TerminBox)
        ownerBox.pack(side="top", fill="x", pady=5)
        ownerLabelBox = tk.Frame(master=ownerBox)
        ownerLabelBox.pack(side="top", fill="x", pady=5)
        L_ownerTitle = tk.Label(ownerLabelBox, text="Besitzer: ").pack(side="left", padx="5")
        self.OwnerLabelText = tk.StringVar()
        self.OwnerLabelText.set("unbekannt")
        L_Owner = tk.Label(ownerLabelBox, textvariable=self.OwnerLabelText)
        L_Owner.pack(side="left", pady="10")

        self.TerminRadiobuttonBoxList = []
        self.TerminRadiobuttonList = []
        self.Termine = []
        self.choosenTermin = tk.IntVar()
        self.choosenTermin.set(0)

        PaymentButtonBox = tk.Frame(master=self.TerminBox)
        PaymentButtonBox.pack(side="top", fill="x", padx="5", pady="5")

        self.B_hasPaid = tk.Button(PaymentButtonBox, text="Hat bezahlt!",
                                   command=(lambda: self.hasPaid(self.Termine[self.choosenTermin.get()][0])))
        self.B_hasPaid.config(state="disabled")
        self.B_hasPaid.pack(side="left", padx="10")
        self.B_hasNotPaid = tk.Button(PaymentButtonBox, text="Hat nicht bezahlt!",
                                      command=(lambda: self.hasNotPaid(self.Termine[self.choosenTermin.get()][0])))
        self.B_hasNotPaid.config(state="disabled")
        self.B_hasNotPaid.pack(side="left", padx="10")

        StatusBox = tk.Frame(master=self.TerminBox)
        StatusBox.pack(side="top", fill="x", padx="5", pady="5")

        self.StatusText = tk.StringVar()
        L_State = tk.Label(StatusBox, textvariable=self.StatusText)
        L_State.pack(side="left", pady="5")

    def hasPaid(self, IID):
        cur.execute("""UPDATE impftermin
                        SET bezahlt = true
                        WHERE iid = %s;""", [IID])
        connection.commit()
        self.StatusText.set(self.Owner[2] + " " + self.Owner[1] + " hat bezahlt für den Termin am "
                            + datetime.strftime(self.Termine[self.choosenTermin.get()][1], "%d.%m.%Y"))
        self.printTermin(self.Owner[0])

    def hasNotPaid(self, IID):
        cur.execute("""UPDATE impftermin
                                SET bezahlt = false
                                WHERE iid = %s;""", [IID])
        connection.commit()
        self.StatusText.set(self.Owner[2] + " " + self.Owner[1] + " hat NICHT bezahlt für den Termin am "
                            + datetime.strftime(self.Termine[self.choosenTermin.get()][1], "%d.%m.%Y"))
        self.printTermin(self.Owner[0])

    def printTermin(self, BID):
        cur.execute("""Select * FROM impftermin
                        JOIN besitzer_impftermin bi on impftermin.IID = bi.IID
                        WHERE bi.BID = %s
                        ORDER BY datum,anzahlhuehner;""", [BID])
        connection.commit()

        self.Termine = cur.fetchall()

        if self.Termine != []:
            for TerminRadiobuttonBox in self.TerminRadiobuttonBoxList:
                TerminRadiobuttonBox.pack_forget()

            for TerminRadiobutton in self.TerminRadiobuttonList:
                TerminRadiobutton.pack_forget()

            self.TerminRadiobuttonBoxList = []
            self.TerminRadiobuttonList = []
            self.choosenTermin = tk.IntVar()
            self.choosenTermin.set(0)

            self.B_hasPaid.config(state="normal")
            self.B_hasNotPaid.config(state="normal")

            i = 0
            for Termin in self.Termine:
                self.TerminRadiobuttonBoxList.append(tk.Frame(master=self.TerminBox))
                self.TerminRadiobuttonList.append(tk.Radiobutton(master=self.TerminRadiobuttonBoxList[i],
                                                                 text=Termin[1].strftime("%d.%m.%Y") + ": " + str(
                                                                     Termin[2])
                                                                      + " Hühner, bezahlt: " + str(Termin[3]).replace(
                                                                     "True", "Ja").replace("False", "Nein"),
                                                                 variable=self.choosenTermin,
                                                                 value=i))
                self.TerminRadiobuttonBoxList[i].pack(side="top", fill="x", pady="5")
                self.TerminRadiobuttonList[i].pack(side="left", padx="5")
                i += 1
        else:
            for TerminRadiobuttonBox in self.TerminRadiobuttonBoxList:
                TerminRadiobuttonBox.pack_forget()

            for TerminRadiobutton in self.TerminRadiobuttonList:
                TerminRadiobutton.pack_forget()

            self.TerminRadiobuttonBoxList = []
            self.TerminRadiobuttonList = []
            self.choosenTermin = tk.IntVar()
            self.choosenTermin.set(0)
            self.B_hasPaid.config(state="disabled")
            self.B_hasNotPaid.config(state="disabled")
            self.StatusText.set("Für diesen Besitzer wurden leider keine Termine gefunden!")

    def search(self, Nachname: str, PLZ: str):
        Nachname = Nachname.replace(" ", "")
        PLZ = PLZ.replace(" ", "")

        cur.execute("""SELECT BID,vorname,nachname,plz,ortsname,strassenname,hausnummer, tel FROM besitzer
                    WHERE nachname = %s AND plz = %s ORDER BY nachname,vorname;""", [Nachname, PLZ])
        connection.commit()
        self.Owners = cur.fetchall()

        if self.Owners == []:
            self.confirmBox.pack_forget()
            self.confirmLabelBox.pack_forget()
            self.L_confirmTitle.pack_forget()
            self.confirmOwnersBox.pack_forget()
            self.B_ConfirmButton.pack_forget()
            self.confirmButtonBox.pack_forget()

            for RadiobuttonBox in self.RadiobuttonBoxList:
                RadiobuttonBox.pack_forget()

            for Radiobutton in self.RadiobuttonList:
                Radiobutton.pack_forget()
            self.SearchStatusText.set(
                "Es ist ein Fehler aufgetreten! Bitte prüfe deine Eingabe und versuche es nochmal")
        else:
            self.SearchStatusText.set("Got: " + str(self.Owners))

            if len(self.Owners) > 1:
                self.isDistinct = False
            if len(self.Owners) == 1:
                self.isDistinct = True
            if self.isDistinct != None:
                self.isSearch == True

            if self.isDistinct == False:
                self.confirmBox.pack_forget()
                self.confirmLabelBox.pack_forget()
                self.L_confirmTitle.pack_forget()
                self.confirmOwnersBox.pack_forget()
                self.B_ConfirmButton.pack_forget()
                self.confirmButtonBox.pack_forget()

                self.L_confirmTitle.config(text=str(len(self.Owners)) + " Besitzer gefunden:")

                self.confirmBox.pack(side="top", fill="x", padx="5", pady="5")
                self.confirmLabelBox.pack(side="top", fill="x", pady="5")
                self.L_confirmTitle.pack(side="left", padx="5")
                self.confirmOwnersBox.pack(side="top", fill="x", pady="5")

                for RadiobuttonBox in self.RadiobuttonBoxList:
                    RadiobuttonBox.pack_forget()

                for Radiobutton in self.RadiobuttonList:
                    Radiobutton.pack_forget()

                self.RadiobuttonBoxList = []
                self.RadiobuttonList = []
                self.choosenOwner = tk.IntVar()
                self.choosenOwner.set(0)

                i = 0
                for Owner in self.Owners:
                    self.RadiobuttonBoxList.append(tk.Frame(master=self.confirmOwnersBox))
                    self.RadiobuttonList.append(tk.Radiobutton(master=self.RadiobuttonBoxList[i], text=str(Owner),
                                                               variable=self.choosenOwner,
                                                               value=i))
                    self.RadiobuttonBoxList[i].pack(side="top", fill="x", pady="5")
                    self.RadiobuttonList[i].pack(side="left", padx="5")
                    i += 1

                self.B_ConfirmButton.configure(command=lambda: self.confirm(self.Owners[self.choosenOwner.get()]))
                self.confirmButtonBox.pack(side="top", fill="x", pady="5")
                self.B_ConfirmButton.pack(side="left", padx="5")
            else:
                self.confirm(self.Owners[0])
                self.confirmBox.pack_forget()
                self.confirmLabelBox.pack_forget()
                self.L_confirmTitle.pack_forget()
                self.confirmOwnersBox.pack_forget()
                self.B_ConfirmButton.pack_forget()
                self.confirmButtonBox.pack_forget()
                for RadiobuttonBox in self.RadiobuttonBoxList:
                    RadiobuttonBox.pack_forget()

                for Radiobutton in self.RadiobuttonList:
                    Radiobutton.pack_forget()

    def confirm(self, Owner):
        self.Owner = Owner
        self.isConfirm = True
        self.B_hasPaid.config(state="normal")
        self.B_hasNotPaid.config(state="normal")
        self.printTermin(Owner[0])
        self.OwnerLabelText.set(str(self.Owner[1]) + " " + str(self.Owner[2]) + ": " +
                                str(self.Owner[3]) + " " + str(self.Owner[4]) + " " + str(self.Owner[5]) + " " +
                                str(self.Owner[6]) + " - " + str(self.Owner[7]))

    def show(self):
        self.lift()
        root.title("Hühnerliste - Zahlung bearbeiten")


# Page delete Termin - user can delete a appointment for a choosen owner
class P_DeleteDate(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.isSearch = False
        self.isConfirm = False
        self.isDistinct = None
        self.Owners = None
        self.Owner = None

        labelBox = tk.Frame(master=self)
        labelBox.pack(side="top", fill="x", padx="5", pady="5")
        label = tk.Label(labelBox, text="Termin eines Besitzers löschen", font=55)
        label.pack(fill="x", side="left")

        self.searchBox = tk.Frame(master=self, borderwidth=2, relief="groove")
        self.searchBox.pack(side="top", fill="x", padx="5", pady="5")

        nameBox = tk.Frame(master=self.searchBox)
        nameBox.pack(side="top", fill="x", pady=5)
        L_vname = tk.Label(nameBox, text="Nachname: ").pack(side="left", padx="5")
        self.E_nname = tk.Entry(nameBox)
        self.E_nname.pack(side="left", padx="5")

        plzBox = tk.Frame(master=self.searchBox)
        plzBox.pack(side="top", fill="x", pady=5)
        L_plz = tk.Label(plzBox, text="PLZ: ").pack(side="left", padx="5")
        self.E_plz = tk.Entry(plzBox)
        self.E_plz.pack(side="left", padx="43")

        ButtonBox = tk.Frame(master=self.searchBox)
        ButtonBox.pack(side="top", fill="x", padx="5", pady="5")

        B_SearchButton = tk.Button(ButtonBox, text="Suche",
                                   command=(lambda: self.search(self.E_nname.get(), self.E_plz.get())))
        B_SearchButton.pack(side="left")
        self.SearchStatusText = tk.StringVar()
        self.SearchStatusText.set("")
        L_State = tk.Label(ButtonBox, textvariable=self.SearchStatusText)
        L_State.pack(side="left", pady="5", padx="20")

        self.confirmBox = tk.Frame(master=self.searchBox, borderwidth=2, relief="groove")
        self.confirmLabelBox = tk.Frame(master=self.confirmBox)
        self.L_confirmTitle = tk.Label(self.confirmLabelBox, text="")
        self.confirmOwnersBox = tk.Frame(master=self.confirmBox)
        self.confirmButtonBox = tk.Frame(master=self.confirmBox)
        self.B_ConfirmButton = tk.Button(self.confirmButtonBox, text="Auswählen")

        self.RadiobuttonBoxList = []
        self.RadiobuttonList = []
        self.choosenOwner = tk.IntVar()
        self.choosenOwner.set(0)

        self.TerminBox = tk.Frame(master=self)
        self.TerminBox.pack(side="top", fill="x", padx="5", pady="5")

        ownerBox = tk.Frame(master=self.TerminBox)
        ownerBox.pack(side="top", fill="x", pady=5)
        ownerLabelBox = tk.Frame(master=ownerBox)
        ownerLabelBox.pack(side="top", fill="x", pady=5)
        L_ownerTitle = tk.Label(ownerLabelBox, text="Besitzer: ").pack(side="left", padx="5")
        self.OwnerLabelText = tk.StringVar()
        self.OwnerLabelText.set("unbekannt")
        L_Owner = tk.Label(ownerLabelBox, textvariable=self.OwnerLabelText)
        L_Owner.pack(side="left", pady="10")

        self.TerminRadiobuttonBoxList = []
        self.TerminRadiobuttonList = []
        self.Termine = []
        self.choosenTermin = tk.IntVar()
        self.choosenTermin.set(0)

        DeletionButtonBox = tk.Frame(master=self.TerminBox)
        DeletionButtonBox.pack(side="top", fill="x", padx="5", pady="5")

        self.B_deleteDate = tk.Button(DeletionButtonBox, text="Termin löschen!",
                                      command=(lambda: self.deleteDate(self.Termine[self.choosenTermin.get()][0])))
        self.B_deleteDate.config(state="disabled")
        self.B_deleteDate.pack(side="left")

        StatusBox = tk.Frame(master=self.TerminBox)
        StatusBox.pack(side="top", fill="x", padx="5", pady="5")

        self.StatusText = tk.StringVar()
        L_State = tk.Label(StatusBox, textvariable=self.StatusText)
        L_State.pack(side="left", pady="5")

    def deleteDate(self, IID):
        cur.execute("""DELETE FROM besitzer_impftermin
                                WHERE iid = %s;""", [IID])
        connection.commit()
        cur.execute("""DELETE FROM impftermin
                        WHERE iid = %s;""", [IID])
        connection.commit()
        self.B_deleteDate.config(state="disabled")
        self.StatusText.set("Termin Nummer " + str(IID) + " gelöscht!")
        self.printTermin(self.Owner[0])

    def printTermin(self, BID):
        cur.execute("""Select * FROM impftermin
                        JOIN besitzer_impftermin bi on impftermin.IID = bi.IID
                        WHERE bi.BID = %s
                        ORDER BY datum,anzahlhuehner;""", [BID])
        connection.commit()

        self.Termine = cur.fetchall()

        if self.Termine != []:
            for TerminRadiobuttonBox in self.TerminRadiobuttonBoxList:
                TerminRadiobuttonBox.pack_forget()

            for TerminRadiobutton in self.TerminRadiobuttonList:
                TerminRadiobutton.pack_forget()

            self.TerminRadiobuttonBoxList = []
            self.TerminRadiobuttonList = []
            self.choosenTermin = tk.IntVar()
            self.choosenTermin.set(0)
            self.B_deleteDate.config(state="normal")

            i = 0
            for Termin in self.Termine:
                self.TerminRadiobuttonBoxList.append(tk.Frame(master=self.TerminBox))
                self.TerminRadiobuttonList.append(tk.Radiobutton(master=self.TerminRadiobuttonBoxList[i],
                                                                 text=Termin[1].strftime("%d.%m.%Y") + ": " + str(
                                                                     Termin[2])
                                                                      + " Hühner, bezahlt: " + str(Termin[3]).replace(
                                                                     "True", "Ja").replace("False", "Nein"),
                                                                 variable=self.choosenTermin,
                                                                 value=i))
                self.TerminRadiobuttonBoxList[i].pack(side="top", fill="x", pady="5")
                self.TerminRadiobuttonList[i].pack(side="left", padx="5")
                i += 1
        else:
            for TerminRadiobuttonBox in self.TerminRadiobuttonBoxList:
                TerminRadiobuttonBox.pack_forget()

            for TerminRadiobutton in self.TerminRadiobuttonList:
                TerminRadiobutton.pack_forget()

            self.TerminRadiobuttonBoxList = []
            self.TerminRadiobuttonList = []
            self.choosenTermin = tk.IntVar()
            self.choosenTermin.set(0)
            self.B_deleteDate.config(state="disabled")
            self.StatusText.set("Für diesen Besitzer wurden leider keine Termine gefunden!")

    def search(self, Nachname: str, PLZ: str):
        Nachname = Nachname.replace(" ", "")
        PLZ = PLZ.replace(" ", "")

        cur.execute("""SELECT BID,vorname,nachname,plz,ortsname,strassenname,hausnummer, tel FROM besitzer
                    WHERE nachname = %s AND plz = %s ORDER BY nachname,vorname;""", [Nachname, PLZ])
        connection.commit()
        self.Owners = cur.fetchall()

        if self.Owners == []:
            self.confirmBox.pack_forget()
            self.confirmLabelBox.pack_forget()
            self.L_confirmTitle.pack_forget()
            self.confirmOwnersBox.pack_forget()
            self.B_ConfirmButton.pack_forget()
            self.confirmButtonBox.pack_forget()

            for RadiobuttonBox in self.RadiobuttonBoxList:
                RadiobuttonBox.pack_forget()

            for Radiobutton in self.RadiobuttonList:
                Radiobutton.pack_forget()
            self.SearchStatusText.set(
                "Es ist ein Fehler aufgetreten! Bitte prüfe deine Eingabe und versuche es nochmal")
        else:
            self.SearchStatusText.set("Got: " + str(self.Owners))

            if len(self.Owners) > 1:
                self.isDistinct = False
            if len(self.Owners) == 1:
                self.isDistinct = True
            if self.isDistinct != None:
                self.isSearch == True

            if self.isDistinct == False:
                self.confirmBox.pack_forget()
                self.confirmLabelBox.pack_forget()
                self.L_confirmTitle.pack_forget()
                self.confirmOwnersBox.pack_forget()
                self.B_ConfirmButton.pack_forget()
                self.confirmButtonBox.pack_forget()

                self.L_confirmTitle.config(text=str(len(self.Owners)) + " Besitzer gefunden:")

                self.confirmBox.pack(side="top", fill="x", padx="5", pady="5")
                self.confirmLabelBox.pack(side="top", fill="x", pady="5")
                self.L_confirmTitle.pack(side="left", padx="5")
                self.confirmOwnersBox.pack(side="top", fill="x", pady="5")

                for RadiobuttonBox in self.RadiobuttonBoxList:
                    RadiobuttonBox.pack_forget()

                for Radiobutton in self.RadiobuttonList:
                    Radiobutton.pack_forget()

                self.RadiobuttonBoxList = []
                self.RadiobuttonList = []
                self.choosenOwner = tk.IntVar()
                self.choosenOwner.set(0)

                i = 0
                for Owner in self.Owners:
                    self.RadiobuttonBoxList.append(tk.Frame(master=self.confirmOwnersBox))
                    self.RadiobuttonList.append(tk.Radiobutton(master=self.RadiobuttonBoxList[i], text=str(Owner),
                                                               variable=self.choosenOwner,
                                                               value=i))
                    self.RadiobuttonBoxList[i].pack(side="top", fill="x", pady="5")
                    self.RadiobuttonList[i].pack(side="left", padx="5")
                    i += 1

                self.B_ConfirmButton.configure(command=lambda: self.confirm(self.Owners[self.choosenOwner.get()]))
                self.confirmButtonBox.pack(side="top", fill="x", pady="5")
                self.B_ConfirmButton.pack(side="left", padx="5")
            else:
                self.confirm(self.Owners[0])
                self.confirmBox.pack_forget()
                self.confirmLabelBox.pack_forget()
                self.L_confirmTitle.pack_forget()
                self.confirmOwnersBox.pack_forget()
                self.B_ConfirmButton.pack_forget()
                self.confirmButtonBox.pack_forget()
                for RadiobuttonBox in self.RadiobuttonBoxList:
                    RadiobuttonBox.pack_forget()

                for Radiobutton in self.RadiobuttonList:
                    Radiobutton.pack_forget()

    def confirm(self, Owner):
        self.Owner = Owner
        self.isConfirm = True
        self.B_deleteDate.config(state="normal")
        self.printTermin(Owner[0])
        self.OwnerLabelText.set(str(self.Owner[1]) + " " + str(self.Owner[2]) + ": " +
                                str(self.Owner[3]) + " " + str(self.Owner[4]) + " " + str(self.Owner[5]) + " " +
                                str(self.Owner[6]) + " - " + str(self.Owner[7]))

    def show(self):
        self.lift()
        root.title("Hühnerliste - Termin löschen")


# Page delete Owner - user can delete a
class P_DeleteOwner(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.isSearch = False
        self.isConfirm = False
        self.isDistinct = None
        self.Owners = None
        self.Owner = None

        labelBox = tk.Frame(master=self)
        labelBox.pack(side="top", fill="x", padx="5", pady="5")
        label = tk.Label(labelBox, text="Besitzer löschen", font=55)
        label.pack(fill="x", side="left")

        self.searchBox = tk.Frame(master=self, borderwidth=2, relief="groove")
        self.searchBox.pack(side="top", fill="x", padx="5", pady="5")

        nameBox = tk.Frame(master=self.searchBox)
        nameBox.pack(side="top", fill="x", pady=5)
        L_vname = tk.Label(nameBox, text="Nachname: ").pack(side="left", padx="5")
        self.E_nname = tk.Entry(nameBox)
        self.E_nname.pack(side="left", padx="5")

        plzBox = tk.Frame(master=self.searchBox)
        plzBox.pack(side="top", fill="x", pady=5)
        L_plz = tk.Label(plzBox, text="PLZ: ").pack(side="left", padx="5")
        self.E_plz = tk.Entry(plzBox)
        self.E_plz.pack(side="left", padx="43")

        ButtonBox = tk.Frame(master=self.searchBox)
        ButtonBox.pack(side="top", fill="x", padx="5", pady="5")

        B_SearchButton = tk.Button(ButtonBox, text="Suche",
                                   command=(lambda: self.search(self.E_nname.get(), self.E_plz.get())))
        B_SearchButton.pack(side="left")
        self.SearchStatusText = tk.StringVar()
        self.SearchStatusText.set("")
        L_State = tk.Label(ButtonBox, textvariable=self.SearchStatusText)
        L_State.pack(side="left", pady="5", padx="20")

        self.confirmBox = tk.Frame(master=self.searchBox, borderwidth=2, relief="groove")
        self.confirmLabelBox = tk.Frame(master=self.confirmBox)
        self.L_confirmTitle = tk.Label(self.confirmLabelBox, text="")
        self.confirmOwnersBox = tk.Frame(master=self.confirmBox)
        self.confirmButtonBox = tk.Frame(master=self.confirmBox)
        self.B_ConfirmButton = tk.Button(self.confirmButtonBox, text="Auswählen")

        self.RadiobuttonBoxList = []
        self.RadiobuttonList = []
        self.choosenOwner = tk.IntVar()
        self.choosenOwner.set(0)

        DeleteBox = tk.Frame(master=self)
        DeleteBox.pack(side="top", fill="x", padx="5", pady="5")

        ownerBox = tk.Frame(master=DeleteBox)
        ownerBox.pack(side="top", fill="x", pady=5)
        ownerLabelBox = tk.Frame(master=ownerBox)
        ownerLabelBox.pack(side="top", fill="x", pady=5)
        L_ownerTitle = tk.Label(ownerLabelBox, text="Besitzer: ").pack(side="left", padx="5")
        self.OwnerLabelText = tk.StringVar()
        self.OwnerLabelText.set("unbekannt")
        L_Owner = tk.Label(ownerLabelBox, textvariable=self.OwnerLabelText)
        L_Owner.pack(side="left", pady="10")

        DeletionButtonBox = tk.Frame(master=DeleteBox)
        DeletionButtonBox.pack(side="top", fill="x", padx="5", pady="5")

        self.B_deleteOwner = tk.Button(DeletionButtonBox, text="Besitzer löschen!",
                                       command=(lambda: self.deleteOwner(self.Owner[0])))
        self.B_deleteOwner.config(state="disabled")
        self.B_deleteOwner.pack(side="left")

        StatusBox = tk.Frame(master=DeleteBox)
        StatusBox.pack(side="top", fill="x", padx="5", pady="5")

        self.StatusText = tk.StringVar()
        L_State = tk.Label(StatusBox, textvariable=self.StatusText)
        L_State.pack(side="left", pady="5")

    def deleteOwner(self, BID):
        cur.execute("""SELECT impftermin.IID FROM impftermin
                        JOIN besitzer_impftermin bi on impftermin.IID = bi.IID
                        JOIN besitzer b on b.BID = bi.BID
                        WHERE b.BID = %s;""", [BID])
        connection.commit()
        IIDs = cur.fetchall()

        for IID in IIDs:
            cur.execute("""DELETE FROM besitzer_impftermin
                                            WHERE iid = %s;""", [IID])
            connection.commit()
            cur.execute("""DELETE FROM impftermin
                                            WHERE iid = %s;""", [IID])
            connection.commit()

        cur.execute("""DELETE FROM besitzer
                                WHERE bid = %s;""", [BID])
        connection.commit()

        self.B_deleteOwner.config(state="disabled")
        self.StatusText.set("Besitzer Nummer " + str(BID) + " mit allen Terminen gelöscht!")
        self.search(self.E_nname.get(), self.E_plz.get())

    def search(self, Nachname: str, PLZ: str):
        Nachname = Nachname.replace(" ", "")
        PLZ = PLZ.replace(" ", "")

        cur.execute("""SELECT BID,vorname,nachname,plz,ortsname,strassenname,hausnummer, tel FROM besitzer
                    WHERE nachname = %s AND plz = %s ORDER BY nachname,vorname;""", [Nachname, PLZ])
        connection.commit()
        self.Owners = cur.fetchall()

        if self.Owners == []:
            self.confirmBox.pack_forget()
            self.confirmLabelBox.pack_forget()
            self.L_confirmTitle.pack_forget()
            self.confirmOwnersBox.pack_forget()
            self.B_ConfirmButton.pack_forget()
            self.confirmButtonBox.pack_forget()

            for RadiobuttonBox in self.RadiobuttonBoxList:
                RadiobuttonBox.pack_forget()

            for Radiobutton in self.RadiobuttonList:
                Radiobutton.pack_forget()
            self.SearchStatusText.set(
                "Es ist ein Fehler aufgetreten! Bitte prüfe deine Eingabe und versuche es nochmal")
        else:
            self.SearchStatusText.set("Got: " + str(self.Owners))

            if len(self.Owners) > 1:
                self.isDistinct = False
            if len(self.Owners) == 1:
                self.isDistinct = True
            if self.isDistinct != None:
                self.isSearch == True

            if self.isDistinct == False:
                self.confirmBox.pack_forget()
                self.confirmLabelBox.pack_forget()
                self.L_confirmTitle.pack_forget()
                self.confirmOwnersBox.pack_forget()
                self.B_ConfirmButton.pack_forget()
                self.confirmButtonBox.pack_forget()

                self.L_confirmTitle.config(text=str(len(self.Owners)) + " Besitzer gefunden:")

                self.confirmBox.pack(side="top", fill="x", padx="5", pady="5")
                self.confirmLabelBox.pack(side="top", fill="x", pady="5")
                self.L_confirmTitle.pack(side="left", padx="5")
                self.confirmOwnersBox.pack(side="top", fill="x", pady="5")

                for RadiobuttonBox in self.RadiobuttonBoxList:
                    RadiobuttonBox.pack_forget()

                for Radiobutton in self.RadiobuttonList:
                    Radiobutton.pack_forget()

                self.RadiobuttonBoxList = []
                self.RadiobuttonList = []
                self.choosenOwner = tk.IntVar()
                self.choosenOwner.set(0)

                i = 0
                for Owner in self.Owners:
                    self.RadiobuttonBoxList.append(tk.Frame(master=self.confirmOwnersBox))
                    self.RadiobuttonList.append(tk.Radiobutton(master=self.RadiobuttonBoxList[i], text=str(Owner),
                                                               variable=self.choosenOwner,
                                                               value=i))
                    self.RadiobuttonBoxList[i].pack(side="top", fill="x", pady="5")
                    self.RadiobuttonList[i].pack(side="left", padx="5")
                    i += 1

                self.B_ConfirmButton.configure(command=lambda: self.confirm(self.Owners[self.choosenOwner.get()]))
                self.confirmButtonBox.pack(side="top", fill="x", pady="5")
                self.B_ConfirmButton.pack(side="left", padx="5")
            else:
                self.confirm(self.Owners[0])
                self.confirmBox.pack_forget()
                self.confirmLabelBox.pack_forget()
                self.L_confirmTitle.pack_forget()
                self.confirmOwnersBox.pack_forget()
                self.B_ConfirmButton.pack_forget()
                self.confirmButtonBox.pack_forget()
                for RadiobuttonBox in self.RadiobuttonBoxList:
                    RadiobuttonBox.pack_forget()

                for Radiobutton in self.RadiobuttonList:
                    Radiobutton.pack_forget()

    def confirm(self, Owner):
        self.Owner = Owner
        self.isConfirm = True
        self.B_deleteOwner.config(state="normal")
        self.OwnerLabelText.set(str(self.Owner[1]) + " " + str(self.Owner[2]) + ": " +
                                str(self.Owner[3]) + " " + str(self.Owner[4]) + " " + str(self.Owner[5]) + " " +
                                str(self.Owner[6]) + " - " + str(self.Owner[7]))

    def show(self):
        self.lift()
        root.title("Hühnerliste - Besitzer löschen")


# Content Frame with Menu
class MainView(tk.Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        # Pages define and place
        pVA = P_ViewAllPrintAll(self)
        pO = P_Owner(self)
        pTO = P_AddTerminOne(self)
        pTM = P_AddTerminMultiple(self)
        pC = P_ConfirmPayment(self)
        pDD = P_DeleteDate(self)
        pDO = P_DeleteOwner(self)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        pVA.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        pO.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        pTO.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        pTM.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        pC.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        pDD.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        pDO.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        # Menu for changing pages
        menu = tk.Menu(root)
        root.config(menu=menu)
        pagemenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Funktionen", menu=pagemenu)

        pagemenu.add_command(label="Vorschau und Drucken", command=pVA.show)
        pagemenu.add_separator()

        addmenu = tk.Menu(pagemenu, tearoff=0)
        pagemenu.add_cascade(label="Hinzufügen", menu=addmenu)
        addmenu.add_command(label="Besitzer hinzufügen", command=pO.show)

        terminmenu = tk.Menu(addmenu, tearoff=0)
        addmenu.add_cascade(label="Termin hinzufügen", menu=terminmenu)
        terminmenu.add_command(label="Ein Besitzer", command=pTO.show)
        terminmenu.add_command(label="Mehrere Besitzer", command=pTM.show)
        pagemenu.add_separator()

        deletemenu = tk.Menu(pagemenu, tearoff=0)
        pagemenu.add_cascade(label="Löschen", menu=deletemenu)
        deletemenu.add_command(label="Besitzer löschen", command=pDO.show)
        deletemenu.add_command(label="Termin löschen", command=pDD.show)
        pagemenu.add_separator()

        pagemenu.add_command(label="Zahlung bearbeiten", command=pC.show)

        pVA.show()


# Functions
# Returns formatted data-array fot sheet
def getAll():
    cur.execute("SELECT * FROM besitzer order by nachname, vorname;")
    connection.commit()

    ownersList = cur.fetchall()

    x = 0
    data = [["Name", "Adresse", "Telefonnummer", "Termin-datum", "Hühneranzahl", "Bezahlung"]]

    for owner in ownersList:
        data.append([])
        x = x + 1

        # hohlt sich die Liste der Termine für diesen Besitzer
        BesitzerID = owner[0]
        cur.execute("SELECT datum,anzahlhuehner,bezahlt "
                    "FROM impftermin JOIN besitzer_impftermin bi on impftermin.IID = bi.IID "
                    "WHERE BID = %s ORDER BY datum,anzahlhuehner;", [BesitzerID])
        connection.commit()

        terminList = cur.fetchall()

        # schreibt Daten des Besitzers in Tabelle

        data[x].append(str(owner[1] + ", " + owner[2]))  # Nachname, Vorname
        data[x].append(str(owner[3] + " " + owner[4] + ", " + owner[5] + " " + owner[6]))  # Adresse
        data[x].append((owner[7]))  # Telefonnummer

        if not terminList:  # if no termine for besitzer append empty values instead and jump to next besitzer
            data[x].append("")
            data[x].append("")
            data[x].append("")
            continue

        j = 0
        while j < len(terminList):
            for i in range(3):
                data[x].append(str(terminList[j][i]))

            if j < (len(terminList) - 1):
                x = x + 1
                data.append(["", "", ""])
            j += 1

    return data


# print DB to xls workbook
def printAll(fname):
    # Setup ExcelDatei
    book = xlwt.Workbook()
    sheet = book.add_sheet("Hühnerliste")
    sheet.col(0).width = 256 * 25
    sheet.col(1).width = 256 * 35
    sheet.col(2).width = 256 * 20

    rowNumb = 1

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

    ownersList = cur.fetchall()

    for owner in ownersList:
        # hohlt sich die Liste der Termine für diesen Besitzer
        BesitzerID = owner[0]
        cur.execute("SELECT datum,anzahlhuehner,bezahlt "
                    "FROM impftermin JOIN besitzer_impftermin bi on impftermin.IID = bi.IID "
                    "WHERE BID = %s ORDER BY datum,anzahlhuehner;", [BesitzerID])
        connection.commit()

        terminList = cur.fetchall()

        # schreibt Daten des Besitzers in Tabelle
        row = sheet.row(rowNumb)
        row.write(0, str(owner[1] + ", " + owner[2]))  # Nachname, Vorname
        row.write(1, str(owner[3] + " " + owner[4] + ", " + owner[5] + " " + owner[6]))  # Adresse
        row.write(2, str(owner[7]))  # Telefonnummer

        j = 0
        while j < len(terminList):
            for i in range(3):
                # col = chr(ord(startChar) + (7+(3*j)+i)) #berechnung Buchstaben (start Buchstabe + offsetBesitzer +
                # Anzahl der termine * Offset Termine + aktuelle Stelle)
                row.write(3 + i, str(terminList[j][i]))

            if j < (len(terminList) - 1):
                rowNumb = rowNumb + 1
                row = sheet.row(rowNumb)
            j += 1

        rowNumb = rowNumb + 1  # enable for seperation by empty line for entries

    book.save(fname + "/Hühnerliste.xls")
    msg.showinfo("Erfolgreich gespeichert!", "Die Hühner liste wurde erflogreich unter " +
                 fname + "/Hühnerliste.xls gespeichert.")

    return 1


# add a new Owner to DB
# all arguments have to be given, if unknown vname or tel: give None
def addOwnerReturnBID(nname: str, plz: str, ortsname: str, strassenname: str, hausnummer: str, vname: str = None,
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
                    [nname, vname,plz, ortsname, strassenname, hausnummer, tel])
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


def addTerminReturnIID(datum: datetime, huehner: int, bezahlt: bool):
    cur.execute("""INSERT INTO impftermin (datum, anzahlhuehner, bezahlt)
                    VALUES (%s, %s, %s) RETURNING impftermin.IID;""", [datum, huehner, bezahlt])
    connection.commit()
    iid = cur.fetchone()
    return iid[0]


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Hühnerliste")
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("1280x720")
    root.mainloop()
