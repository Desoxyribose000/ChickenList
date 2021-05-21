#!/usr/bin/python3

# Autor: Max Nowak
# Version: 0.5 wip - Cloud Access
# Programm for Manipulation of ChickenList DB
# GUI Controller


import tkinter as tk
import tkinter.filedialog as fdialog
from tksheet import Sheet
from tkinter import ttk
from tkinter import messagebox as msg
from datetime import datetime

import db_access as dba

import pdf

import qr_encrypt


# GUI
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)


# preview entire db and Print to xls file in given directory
class PageViewAllPrintAll(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        label_box = tk.Frame(master=self)
        label_box.pack(side="top", fill="x", padx="5", pady="5")
        label = tk.Label(label_box, text="Vorschau und Drucken", font=55)
        label.pack(fill="x", side="left")

        data = dba.get_all()  # get Data from DB

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

        self.button = tk.Button(self, text="Als Datei Speichern", command=(lambda: self.select_dir()))
        self.button.pack(side="left", padx="10", pady="10")

    def refresh(self):
        data = dba.get_all()
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
    def select_dir():
        fname = fdialog.askdirectory()
        dba.print_all(fname)


# add new Owner
class PageOwner(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        label_box = tk.Frame(master=self)
        label_box.pack(side="top", fill="x", padx="5", pady="5")
        label = tk.Label(label_box, text="Einen Neuen Besitzer hinzufügen", font=55)
        label.pack(fill="x", side="left")

        owner_box = tk.Frame(master=self, borderwidth=2, relief="groove")
        owner_box.pack(side="top", fill="x", padx="5",
                       pady="5")

        name_box = tk.Frame(owner_box)
        name_box.pack(side="top", fill="x", pady=5)

        vname_box = tk.Frame(name_box)
        vname_box.pack(side="left", fill="x")
        tk.Label(vname_box, text="Vorname").pack(side="left", padx="5")
        self.E_vname = tk.Entry(vname_box)
        self.E_vname.pack(side="left", padx="5")

        nname_box = tk.Frame(name_box)
        nname_box.pack(side="left", fill="x")
        tk.Label(nname_box, text="Nachname *").pack(side="left", padx="5")
        self.E_nname = tk.Entry(nname_box)
        self.E_nname.pack(side="left", padx="5")

        adress_box = tk.Frame(owner_box)
        adress_box.pack(side="top", fill="x", pady=5)

        plz_box = tk.Frame(adress_box)
        plz_box.pack(side="left", fill="x")
        tk.Label(plz_box, text="PLZ *").pack(side="left", padx="5")
        self.E_PLZ = tk.Entry(plz_box)
        self.E_PLZ.pack(side="left", padx="25")

        ort_box = tk.Frame(adress_box)
        ort_box.pack(side="left", fill="x")
        tk.Label(ort_box, text="Ort *").pack(side="left", padx="5")
        self.E_Ort = tk.Entry(ort_box)
        self.E_Ort.pack(side="left", padx="25")

        strasse_box = tk.Frame(adress_box)
        strasse_box.pack(side="left", fill="x")
        tk.Label(strasse_box, text="Strasse *").pack(side="left", padx="5")
        self.E_Strasse = tk.Entry(strasse_box)
        self.E_Strasse.pack(side="left", padx="5")

        haus_box = tk.Frame(adress_box)
        haus_box.pack(side="left", fill="x")
        tk.Label(haus_box, text="Hausnummer *").pack(side="left", padx="5")
        self.E_Haus = tk.Entry(haus_box)
        self.E_Haus.pack(side="left", padx="5")

        tel_box = tk.Frame(owner_box)
        tel_box.pack(side="top", fill="x", pady=5)

        tk.Label(tel_box, text="Telefonnummer").pack(side="left", padx="5")
        self.E_Tel = tk.Entry(tel_box)
        self.E_Tel.pack(side="left", padx="5")

        disclaimer_box = tk.Frame(master=self)
        disclaimer_box.pack(side="top", fill="x", padx="5", pady="5")
        tk.Label(disclaimer_box, text="* sind Pflichtfelder").pack(side="left", padx="5")

        button_box = tk.Frame(master=self)
        button_box.pack(side="top", fill="x", padx="5", pady="5")

        add_date = tk.IntVar()
        termin_box = tk.Frame(master=self, borderwidth=2, relief="groove")

        datum_box = tk.Frame(master=termin_box)

        self.thisDate = tk.IntVar()
        self.thisDate.set(1)
        label_datum = tk.Label(datum_box, text="Datum: ")
        radiobutton_this_date_true = tk.Radiobutton(master=datum_box, text='heute', value='1', variable=self.thisDate)
        label_oder = tk.Label(datum_box, text="oder")
        radiobutton_this_date_false = tk.Radiobutton(master=datum_box, text='anderes Datum', value='0',
                                                     variable=self.thisDate)
        self.day = tk.IntVar()
        self.day.set(1)
        spinbox_day = ttk.Spinbox(datum_box, from_=1, to=31, textvariable=self.day, width=5)
        self.month = tk.IntVar()
        self.month.set(1)
        spinbox_month = ttk.Spinbox(datum_box, from_=1, to=12, textvariable=self.month, width=5)
        self.year = tk.IntVar()
        self.year.set(2021)
        spinbox_year = ttk.Spinbox(datum_box, from_=2019, to=2030, textvariable=self.year, width=5)

        huehner_box = tk.Frame(master=termin_box)
        label_huehner = tk.Label(huehner_box, text="Anzahl der Hühner: ")
        self.E_Huehner = tk.Entry(huehner_box)

        paid_box = tk.Frame(master=termin_box)
        label_paid = tk.Label(paid_box, text="bezahlt: ")
        self.paid = tk.IntVar()
        checkbutton_paid = tk.Checkbutton(paid_box, text="", variable=self.paid)

        status_box = tk.Frame(master=self)
        status_box.pack(side="top", fill="x", padx="5", pady="5")

        self.StatusText = tk.StringVar()
        label_state = tk.Label(status_box, textvariable=self.StatusText)
        label_state.pack(side="left", pady="5")

        # terminBox, the outer Box needs to be first
        box_list = [termin_box, datum_box, label_datum, radiobutton_this_date_true, label_oder,
                    radiobutton_this_date_false,
                    spinbox_day,
                    spinbox_month, spinbox_year, huehner_box, label_huehner, self.E_Huehner, paid_box, label_paid,
                    checkbutton_paid]

        # used to check if Termin shall be displayed, calls funtion to dynamicly pack and unpack it
        checkbutton_add_date = tk.Checkbutton(button_box, text="Ein Impfdatum ebenfalls hinzufügen", variable=add_date,
                                              command=(lambda: self.pack_termin(box_list, add_date.get())))

        button_add_button = tk.Button(button_box, text="Hinzufügen",
                                      command=(lambda: self.test_input(add_date.get())))  # (lambda: addOwner())

        button_add_button.pack(side="left")
        checkbutton_add_date.pack(side="left")

    # pack or packforget for the List of all Elemnts needed to display Termin
    @staticmethod
    def pack_termin(box_list, is_add_date):
        if is_add_date:
            for i in range(len(box_list)):
                if i == 0:
                    box_list[i].pack(side="top", fill="x", padx="5", pady="5")
                    continue
                if isinstance(box_list[i], tk.Frame):
                    box_list[i].pack(side="top", fill="x", pady="5")
                else:
                    box_list[i].pack(side="left", padx="5")
        else:
            for item in box_list:
                item.pack_forget()

    def test_input(self, is_add_date):
        valid_input = True

        if is_add_date == 1:
            if self.day is None:
                valid_input = False
            if self.month is None:
                valid_input = False
            if self.year is None:
                valid_input = False
            huehner = self.E_Huehner.get()
            huehner.replace(" ", "")
            if not (huehner.isnumeric()):
                valid_input = False

        plz = self.E_PLZ.get()
        plz = plz.replace(" ", "")
        if not (plz.isnumeric()):
            valid_input = False

        if len(self.E_Tel.get()) > 0:
            tel = self.E_Tel.get()
            tel = tel.replace(" ", "")
            if not (tel.isnumeric()):
                valid_input = False

        entry_list = [self.E_nname, self.E_PLZ, self.E_Ort, self.E_Strasse, self.E_Haus]

        if is_add_date == 1:
            entry_list.append(self.E_Huehner)
            try:
                date_string = str(self.year.get()) + "-" + str(self.month.get()) + "-" + str(self.day.get())
                datetime.strptime(date_string, '%Y-%m-%d')
            except Exception as e:
                msg.showerror("Fehlerhaftes Datum!", message="Das von Ihnen eingebene Datum enthält Fehler!\n" + str(e))
                valid_input = False

        is_empty = False
        for Entry in entry_list:
            if len(Entry.get()) == 0:
                is_empty = True
        if is_empty:
            self.StatusText.set("Bitte fülle alle Pflichtfelder und achte auf sinnvolle Eingaben!")
            valid_input = False

        if valid_input:
            # Build Dicttionary of Owner values
            owner_dict = {
                'Vorname': self.E_vname.get().replace(" ", ""),
                'Nachname': self.E_nname.get().replace(" ", ""),
                'PLZ': self.E_PLZ.get().replace(" ", ""),
                'Ort': self.E_Ort.get().replace(" ", ""),
                'Strasse': self.E_Strasse.get().replace(" ", ""),
                'Hausnummer': self.E_Haus.get().replace(" ", ""),
                'Telefonnummer': self.E_Tel.get().replace(" ", "")
            }

            # Build Dictionary of Termin related values if Termin is true
            if is_add_date == 0:
                termin_dict = None
            else:
                if self.thisDate.get() == 1:
                    date_string = datetime.today().strftime('%Y-%m-%d')
                    datum = datetime.strptime(date_string, '%Y-%m-%d')
                else:
                    # if self.thisDate.get() == 0:
                    date_string = str(self.year.get()) + "-" + str(self.month.get()) + "-" + str(self.day.get())
                    datum = datetime.strptime(date_string, '%Y-%m-%d')
                termin_dict = {
                    'Datum': datum,
                    'Huehner': int(self.E_Huehner.get().replace(" ", "")),
                    'bezahlt': bool(self.paid.get())
                }
            self.commit_owner(owner_dict, is_add_date, termin_dict)
        else:
            self.StatusText.set("Bitte fülle alle Pflichtfelder und achte auf sinnvolle Eingaben!")

    def commit_owner(self, owner_dict, is_add_termin, termin_dict=None):
        if is_add_termin == 0:
            dba.add_owner_return_bid(owner_dict['Nachname'], owner_dict['PLZ'], owner_dict['Ort'],
                                     owner_dict['Strasse'],
                                     owner_dict['Hausnummer'], owner_dict['Vorname'], owner_dict['Telefonnummer'])
            self.StatusText.set("Besitzer " + str(owner_dict) + " wurde hinzugefügt!")
        else:
            bid = dba.add_owner_return_bid(owner_dict['Nachname'], owner_dict['PLZ'], owner_dict['Ort'],
                                           owner_dict['Strasse'],
                                           owner_dict['Hausnummer'], owner_dict['Vorname'], owner_dict['Telefonnummer'])
            if bid == -1:
                raise Exception("Fehler")

            iid = dba.add_termin_return_iid(termin_dict['Datum'], termin_dict['Huehner'], termin_dict['bezahlt'])

            dba.commit_termine(bid, iid)

            self.StatusText.set("Besitzer " + str(owner_dict) + " wurde hinzugefügt!\n" +
                                "Termin " + str(termin_dict) + " wurde hinzugefügt!\n" +
                                "Besitzer " + str(bid) + " und Termin " + str(iid) + " wurde assoziert!")

    def show(self):
        self.lift()
        root.title("Hühnerliste - Besitzer hinzufügen")


# add appointment for one owner
class PageAddTerminOne(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.isSearch = False
        self.isConfirm = False
        self.isDistinct = None
        self.Owners = None
        self.Owner = None

        label_box = tk.Frame(master=self)
        label_box.pack(side="top", fill="x", padx="5", pady="5")
        label = tk.Label(label_box, text="Einem Besitzer einen neuen Termin hinzufügen", font=55)
        label.pack(fill="x", side="left")

        self.searchBox = tk.Frame(master=self, borderwidth=2, relief="groove")
        self.searchBox.pack(side="top", fill="x", padx="5", pady="5")

        name_box = tk.Frame(master=self.searchBox)
        name_box.pack(side="top", fill="x", pady=5)
        tk.Label(name_box, text="Nachname: ").pack(side="left", padx="5")
        self.E_nname = tk.Entry(name_box)
        self.E_nname.pack(side="left", padx="5")

        plz_box = tk.Frame(master=self.searchBox)
        plz_box.pack(side="top", fill="x", pady=5)
        tk.Label(plz_box, text="PLZ: ").pack(side="left", padx="5")
        self.E_plz = tk.Entry(plz_box)
        self.E_plz.pack(side="left", padx="43")

        button_box = tk.Frame(master=self.searchBox)
        button_box.pack(side="top", fill="x", padx="5", pady="5")

        button_search_button = tk.Button(button_box, text="Suche", command=(
            lambda: self.search(self.E_nname.get().replace(" ", ""), self.E_plz.get().replace(" ", ""))))
        button_search_button.pack(side="left")
        self.SearchStatusText = tk.StringVar()
        self.SearchStatusText.set("")
        label_state = tk.Label(button_box, textvariable=self.SearchStatusText)
        label_state.pack(side="left", pady="5", padx="20")

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

        termin_box = tk.Frame(master=self)
        termin_box.pack(side="top", fill="x", padx="5", pady="5")

        owner_box = tk.Frame(master=termin_box)
        owner_box.pack(side="top", fill="x", pady=5)
        owner_label_box = tk.Frame(master=owner_box)
        owner_label_box.pack(side="top", fill="x", pady=5)
        tk.Label(owner_label_box, text="Besitzer: ").pack(side="left", padx="5")
        self.OwnerLabelText = tk.StringVar()
        self.OwnerLabelText.set("unbekannt")
        label_owner = tk.Label(owner_label_box, textvariable=self.OwnerLabelText)
        label_owner.pack(side="left", pady="10")

        # .pack(side="top", fill="x", padx="5", pady="5")
        # .pack(side="top", fill="x", pady="5")
        # .pack(side="left", padx="5")

        # Termin hinzufügen

        datum_box = tk.Frame(master=termin_box)
        datum_box.pack(side="top", fill="x", pady="5")

        self.thisDate = tk.IntVar()
        self.thisDate.set(1)
        label_datum = tk.Label(datum_box, text="Datum: ")
        label_datum.pack(side="left", padx="5")
        radiobutton_this_date_true = tk.Radiobutton(master=datum_box, text='heute', value='1', variable=self.thisDate)
        radiobutton_this_date_true.pack(side="left", padx="5")
        label_oder = tk.Label(datum_box, text="oder")
        label_oder.pack(side="left", padx="5")
        radiobutton_this_date_false = tk.Radiobutton(master=datum_box, text='anderes Datum', value='0',
                                                     variable=self.thisDate)
        radiobutton_this_date_false.pack(side="left", padx="5")
        self.day = tk.IntVar()
        self.day.set(1)
        spinbox_day = ttk.Spinbox(datum_box, from_=1, to=31, textvariable=self.day, width=5)
        spinbox_day.pack(side="left", padx="5")
        self.month = tk.IntVar()
        self.month.set(1)
        spinbox_month = ttk.Spinbox(datum_box, from_=1, to=12, textvariable=self.month, width=5)
        spinbox_month.pack(side="left", padx="5")
        self.year = tk.IntVar()
        self.year.set(2021)
        spinbox_year = ttk.Spinbox(datum_box, from_=2019, to=2030, textvariable=self.year, width=5)
        spinbox_year.pack(side="left", padx="5")

        huehner_box = tk.Frame(master=termin_box)
        huehner_box.pack(side="top", fill="x", pady="5")
        label_huehner = tk.Label(huehner_box, text="Anzahl der Hühner: ")
        label_huehner.pack(side="left", padx="5")
        self.E_Huehner = tk.Entry(huehner_box)
        self.E_Huehner.pack(side="left", padx="5")

        paid_box = tk.Frame(master=termin_box)
        paid_box.pack(side="top", fill="x", pady="5")
        label_paid = tk.Label(paid_box, text="bezahlt: ")
        label_paid.pack(side="left", padx="5")
        self.paid = tk.IntVar()
        checkbutton_paid = tk.Checkbutton(paid_box, text="", variable=self.paid)
        checkbutton_paid.pack(side="left", padx="5")

        commit_button_box = tk.Frame(master=termin_box)
        commit_button_box.pack(side="top", fill="x", padx="5", pady="5")

        self.B_CommitButton = tk.Button(commit_button_box, text="Speichern",
                                        command=(lambda: self.test_input(self.Owner[0])))
        self.B_CommitButton.config(state="disabled")
        self.B_CommitButton.pack(side="left")

        status_box = tk.Frame(master=self)
        status_box.pack(side="top", fill="x", padx="5", pady="5")

        self.StatusText = tk.StringVar()
        label_state = tk.Label(status_box, textvariable=self.StatusText)
        label_state.pack(side="left", pady="5")

    def test_input(self, bid):
        valid_input = True

        if self.day is None:
            valid_input = False
        if self.month is None:
            valid_input = False
        if self.year is None:
            valid_input = False
        if not (self.E_Huehner.get().replace(" ", "").isnumeric()):
            valid_input = False

        is_empty = False
        if len(self.E_Huehner.get()) == 0:
            is_empty = True
        if is_empty:
            self.StatusText.set("Bitte gebe die Anzahl der Hühner an!")
            valid_input = False

        try:
            date_string = str(self.year.get()) + "-" + str(self.month.get()) + "-" + str(self.day.get())
            datetime.strptime(date_string, '%Y-%m-%d')
        except Exception as e:
            msg.showerror("Fehlerhaftes Datum!", message="Das von Ihnen eingebene Datum enthält Fehler!\n" + str(e))
            valid_input = False

        if valid_input & self.isConfirm:
            # Build Dictionary of Termin related values if Termin is true
            if self.thisDate.get() == 1:
                date_string = datetime.today().strftime('%Y-%m-%d')
                datum = datetime.strptime(date_string, '%Y-%m-%d')
            else:
                date_string = str(self.year.get()) + "-" + str(self.month.get()) + "-" + str(self.day.get())
                datum = datetime.strptime(date_string, '%Y-%m-%d')

            termin_dict = {
                'Datum': datum,
                'Huehner': int(self.E_Huehner.get().replace(" ", "")),
                'bezahlt': bool(self.paid.get())
            }
            self.commit_termin(bid, termin_dict)
        else:
            self.StatusText.set("Bitte prüfe deine Eingabe oder Suche zuerst nach einem Besitzer!")

    def commit_termin(self, bid, termin_dict):
        iid = dba.add_termin_return_iid(termin_dict['Datum'], termin_dict['Huehner'], termin_dict['bezahlt'])
        dba.commit_termine(bid, iid)

        self.StatusText.set("Termin " + str(termin_dict) + " wurde hinzugefügt!\n" +
                            "Besitzer " + str(bid) + " und Termin " + str(iid) + " wurde assoziert!")

    def search(self, nachname: str, plz: str):
        nachname = nachname.replace(" ", "")
        plz = plz.replace(" ", "")

        self.Owners = dba.search(nachname, plz)

        if not self.Owners:
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
            if self.isDistinct is not None:
                self.isSearch = True

            if not self.isDistinct:
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

    def confirm(self, owner):
        self.Owner = owner
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
class PageAddTerminMultiple(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.owners = dba.refresh()

        label_box = tk.Frame(master=self)
        label_box.pack(side="top", fill="x", padx="5", pady="5")
        label = tk.Label(label_box, text="Einem Besitzer einen neuen Termin hinzufügen", font=55)
        label.pack(fill="x", side="left")

        datum_box = tk.Frame(master=self)
        datum_box.pack(side="top", fill="x", pady="5")

        # get a date
        self.thisDate = tk.IntVar()
        self.thisDate.set(1)
        label_datum = tk.Label(datum_box, text="Datum: ")
        label_datum.pack(side="left", padx="5")
        radiobutton_this_date_true = tk.Radiobutton(master=datum_box, text='heute', value='1', variable=self.thisDate)
        radiobutton_this_date_true.pack(side="left", padx="5")
        label_oder = tk.Label(datum_box, text="oder")
        label_oder.pack(side="left", padx="5")
        radiobutton_this_date_false = tk.Radiobutton(master=datum_box, text='anderes Datum', value='0',
                                                     variable=self.thisDate)
        radiobutton_this_date_false.pack(side="left", padx="5")
        self.day = tk.IntVar()
        self.day.set(1)
        spinbox_day = ttk.Spinbox(datum_box, from_=1, to=31, textvariable=self.day, width=5)
        spinbox_day.pack(side="left", padx="5")
        self.month = tk.IntVar()
        self.month.set(1)
        spinbox_month = ttk.Spinbox(datum_box, from_=1, to=12, textvariable=self.month, width=5)
        spinbox_month.pack(side="left", padx="5")
        self.year = tk.IntVar()
        self.year.set(2021)
        spinbox_year = ttk.Spinbox(datum_box, from_=2019, to=2030, textvariable=self.year, width=5)
        spinbox_year.pack(side="left", padx="5")

        # scrollable List of Checkbuttons for all owners
        scroll_container_frame = ttk.Frame(self, borderwidth=2, relief="groove")
        canvas = tk.Canvas(scroll_container_frame, height=400, highlightthickness=0)
        scrollbar = ttk.Scrollbar(scroll_container_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        scroll_container_frame.pack(side="top", fill="x", padx="5", pady="5")
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
                                                       text=str(owner[1]) + ", " +
                                                       str(owner[2]) + ": " +
                                                       str(owner[3]) + " " +
                                                       str(owner[4]) + " " +
                                                       str(owner[5]) + " " +
                                                       str(owner[6]) + " - " +
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

        commit_button_box = tk.Frame(master=self)
        commit_button_box.pack(side="top", fill="x", padx="5", pady="5")

        self.B_CommitButton = tk.Button(commit_button_box, text="Füge Termine hinzu!",
                                        command=(lambda: self.prepare_data()))
        self.B_CommitButton.pack(side="left")

        if not self.owners:
            self.B_CommitButton.config(state="disabled")

        # scrollable StatusBox for longStatus
        status_container_frame = ttk.Frame(self, borderwidth=2, relief="groove")
        status_canvas = tk.Canvas(status_container_frame, height=400)
        status_scrollbar = ttk.Scrollbar(status_container_frame, orient="vertical", command=status_canvas.yview)
        self.StatusBox = ttk.Frame(status_canvas)

        status_container_frame.pack(side="top", fill="x", padx="5", pady="5")
        status_canvas.pack(side="left", fill="both", expand=True)
        status_scrollbar.pack(side="right", fill="y")

        # on change of contentlength edit scrollregion
        self.StatusBox.bind(
            "<Configure>",
            lambda e: status_canvas.configure(
                scrollregion=status_canvas.bbox("all")
            )
        )

        # tell the canvas to draw the frame as window starting from top-left
        status_canvas.create_window((0, 0), window=self.StatusBox, anchor="nw")
        status_canvas.configure(yscrollcommand=status_scrollbar.set)

        self.StatusText = tk.StringVar()
        label_state = tk.Label(self.StatusBox, textvariable=self.StatusText)
        label_state.pack(side="left", pady="5")

    def commit_termine(self, data):
        self.StatusText.set("")

        if self.thisDate.get() == 1:
            date_string = datetime.today().strftime('%Y-%m-%d')
            datum = datetime.strptime(date_string, '%Y-%m-%d')
        else:
            date_string = str(self.year.get()) + "-" + str(self.month.get()) + "-" + str(self.day.get())
            datum = datetime.strptime(date_string, '%Y-%m-%d')

        for entry in data:
            iid = str(dba.add_termin_return_iid(datum, entry[1], bool(entry[2])))
            bid = str(entry[0])
            dba.commit_termine(bid, iid)
            status_text = self.StatusText.get()
            self.StatusText.set(status_text + "\n" + "Besitzer Nr.: " + bid + " wurde ein Termin am " +
                                datetime.strftime(datum, "%d.%m.%Y") + " für " +
                                str(entry[1]) + " Hühner hinzugefügt!")

    def prepare_data(self):
        data = []  # data structure: [[BID,anzahlhuener,bezahlt],...]

        valid_input = True

        if self.day is None:
            valid_input = False
        if self.month is None:
            valid_input = False
        if self.year is None:
            valid_input = False

        try:
            date_string = str(self.year.get()) + "-" + str(self.month.get()) + "-" + str(self.day.get())
            datetime.strptime(date_string, '%Y-%m-%d')
        except Exception as e:
            msg.showerror("Fehlerhaftes Datum!", message="Das von Ihnen eingebene Datum enthält Fehler!\n" + str(e))
            valid_input = False

        i = 0
        for _ in self.checkButtonList:
            if self.checkVarList[i].get() == 1:

                huehner = self.E_huehnerList[i].get()
                huehner = huehner.replace(" ", "")

                if len(huehner) == 0:
                    valid_input = False

                if not (huehner.isnumeric()):
                    valid_input = False

                data.append([self.owners[i][0], huehner, self.paidVar[i].get()])
            i += 1

        if valid_input:
            self.commit_termine(data)
        else:
            self.StatusText.set("Bitte prüfe deine Eingabe auf vollständigkeit!")

    def refresh(self):

        self.owners = dba.refresh()

        if self.owners:
            self.B_CommitButton.config(state="normal")

        for item in self.checkButtonBoxList:
            item.pack_forget()

        for item in self.terminBoxList:
            item.pack_forget()

        for item in self.checkButtonList:
            item.pack_forget()

        for item in self.L_huehnerList:
            item.pack_forget()

        for item in self.E_huehnerList:
            item.pack_forget()

        for item in self.L_PaidList:
            item.pack_forget()

        for item in self.CB_paidList:
            item.pack_forget()

        for item in self.checkBoxList:
            item.pack_forget()

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
            self.checkButtonList.append(tk.Checkbutton(self.checkButtonBoxList[i], text=str(owner[1]) + ", " +
                                                            str(owner[2]) + ": " +
                                                            str(owner[3]) + " " +
                                                            str(owner[4]) + " " +
                                                            str(owner[5]) + " " +
                                                            str(owner[6]) + " - " +
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

    def show(self):
        self.refresh()
        self.lift()
        root.title("Hühnerliste - Termin hinzufügen - mehrere Besitzer")


# Page Confirm Payment - user can validate or invalidate a payment of one appointment
class PageConfirmPayment(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.isSearch = False
        self.isConfirm = False
        self.isDistinct = None
        self.Owners = None
        self.Owner = None

        label_box = tk.Frame(master=self)
        label_box.pack(side="top", fill="x", padx="5", pady="5")
        label = tk.Label(label_box, text="Zahlungen eines Besitzers bearbeiten", font=55)
        label.pack(fill="x", side="left")

        self.searchBox = tk.Frame(master=self, borderwidth=2, relief="groove")
        self.searchBox.pack(side="top", fill="x", padx="5", pady="5")

        name_box = tk.Frame(master=self.searchBox)
        name_box.pack(side="top", fill="x", pady=5)
        tk.Label(name_box, text="Nachname: ").pack(side="left", padx="5")
        self.E_nname = tk.Entry(name_box)
        self.E_nname.pack(side="left", padx="5")

        plz_box = tk.Frame(master=self.searchBox)
        plz_box.pack(side="top", fill="x", pady=5)
        tk.Label(plz_box, text="PLZ: ").pack(side="left", padx="5")
        self.E_plz = tk.Entry(plz_box)
        self.E_plz.pack(side="left", padx="43")

        button_box = tk.Frame(master=self.searchBox)
        button_box.pack(side="top", fill="x", padx="5", pady="5")

        button_search_button = tk.Button(button_box, text="Suche",
                                         command=(lambda: self.search(self.E_nname.get().replace(" ", ""),
                                                                      self.E_plz.get().replace(" ", ""))))
        button_search_button.pack(side="left")
        self.SearchStatusText = tk.StringVar()
        self.SearchStatusText.set("")
        label_state = tk.Label(button_box, textvariable=self.SearchStatusText)
        label_state.pack(side="left", pady="5", padx="20")

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

        owner_box = tk.Frame(master=self.TerminBox)
        owner_box.pack(side="top", fill="x", pady=5)
        owner_label_box = tk.Frame(master=owner_box)
        owner_label_box.pack(side="top", fill="x", pady=5)
        tk.Label(owner_label_box, text="Besitzer: ").pack(side="left", padx="5")
        self.OwnerLabelText = tk.StringVar()
        self.OwnerLabelText.set("unbekannt")
        label_owner = tk.Label(owner_label_box, textvariable=self.OwnerLabelText)
        label_owner.pack(side="left", pady="10")

        self.TerminRadiobuttonBoxList = []
        self.TerminRadiobuttonList = []
        self.Termine = []
        self.choosenTermin = tk.IntVar()
        self.choosenTermin.set(0)

        payment_button_box = tk.Frame(master=self.TerminBox)
        payment_button_box.pack(side="top", fill="x", padx="5", pady="5")

        self.B_hasPaid = tk.Button(payment_button_box, text="Hat bezahlt!",
                                   command=(lambda: self.has_paid(self.Termine[self.choosenTermin.get()][0])))
        self.B_hasPaid.config(state="disabled")
        self.B_hasPaid.pack(side="left", padx="10")
        self.B_hasNotPaid = tk.Button(payment_button_box, text="Hat nicht bezahlt!",
                                      command=(lambda: self.has_not_paid(self.Termine[self.choosenTermin.get()][0])))
        self.B_hasNotPaid.config(state="disabled")
        self.B_hasNotPaid.pack(side="left", padx="10")

        status_box = tk.Frame(master=self.TerminBox)
        status_box.pack(side="top", fill="x", padx="5", pady="5")

        self.StatusText = tk.StringVar()
        label_state = tk.Label(status_box, textvariable=self.StatusText)
        label_state.pack(side="left", pady="5")

    def has_paid(self, iid):
        dba.has_paid(iid)
        self.StatusText.set(self.Owner[2] + " " + self.Owner[1] + " hat bezahlt für den Termin am "
                            + datetime.strftime(self.Termine[self.choosenTermin.get()][1], "%d.%m.%Y"))
        self.print_termin(self.Owner[0])

    def has_not_paid(self, iid):
        dba.has_not_paid(iid)
        self.StatusText.set(self.Owner[2] + " " + self.Owner[1] + " hat NICHT bezahlt für den Termin am "
                            + datetime.strftime(self.Termine[self.choosenTermin.get()][1], "%d.%m.%Y"))
        self.print_termin(self.Owner[0])

    def print_termin(self, bid):
        self.Termine = dba.print_termin(bid)

        if self.Termine:
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
                                                                 text=Termin[1].strftime("%d.%m.%Y") + ": " +
                                                                 str(Termin[2]) +
                                                                 " Hühner, bezahlt: " + str(Termin[3]).replace(
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

    def search(self, nachname: str, plz: str):
        nachname = nachname.replace(" ", "")
        plz = plz.replace(" ", "")

        self.Owners = dba.search(nachname, plz)

        if not self.Owners:
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
            if self.isDistinct is not None:
                self.isSearch = True

            if not self.isDistinct:
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

    def confirm(self, owner):
        self.Owner = owner
        self.isConfirm = True
        self.B_hasPaid.config(state="normal")
        self.B_hasNotPaid.config(state="normal")
        self.print_termin(owner[0])
        self.OwnerLabelText.set(str(self.Owner[1]) + " " + str(self.Owner[2]) + ": " +
                                str(self.Owner[3]) + " " + str(self.Owner[4]) + " " + str(self.Owner[5]) + " " +
                                str(self.Owner[6]) + " - " + str(self.Owner[7]))

    def show(self):
        self.lift()
        root.title("Hühnerliste - Zahlung bearbeiten")


# Page delete Termin - user can delete a appointment for a choosen owner
class PageDeleteDate(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.isSearch = False
        self.isConfirm = False
        self.isDistinct = None
        self.Owners = None
        self.Owner = None

        label_box = tk.Frame(master=self)
        label_box.pack(side="top", fill="x", padx="5", pady="5")
        label = tk.Label(label_box, text="Termin eines Besitzers löschen", font=55)
        label.pack(fill="x", side="left")

        self.searchBox = tk.Frame(master=self, borderwidth=2, relief="groove")
        self.searchBox.pack(side="top", fill="x", padx="5", pady="5")

        name_box = tk.Frame(master=self.searchBox)
        name_box.pack(side="top", fill="x", pady=5)
        tk.Label(name_box, text="Nachname: ").pack(side="left", padx="5")
        self.E_nname = tk.Entry(name_box)
        self.E_nname.pack(side="left", padx="5")

        plz_box = tk.Frame(master=self.searchBox)
        plz_box.pack(side="top", fill="x", pady=5)
        tk.Label(plz_box, text="PLZ: ").pack(side="left", padx="5")
        self.E_plz = tk.Entry(plz_box)
        self.E_plz.pack(side="left", padx="43")

        button_box = tk.Frame(master=self.searchBox)
        button_box.pack(side="top", fill="x", padx="5", pady="5")

        button_search_button = tk.Button(button_box, text="Suche",
                                         command=(lambda: self.search(self.E_nname.get(), self.E_plz.get())))
        button_search_button.pack(side="left")
        self.SearchStatusText = tk.StringVar()
        self.SearchStatusText.set("")
        label_state = tk.Label(button_box, textvariable=self.SearchStatusText)
        label_state.pack(side="left", pady="5", padx="20")

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

        owner_box = tk.Frame(master=self.TerminBox)
        owner_box.pack(side="top", fill="x", pady=5)
        owner_label_box = tk.Frame(master=owner_box)
        owner_label_box.pack(side="top", fill="x", pady=5)
        tk.Label(owner_label_box, text="Besitzer: ").pack(side="left", padx="5")
        self.OwnerLabelText = tk.StringVar()
        self.OwnerLabelText.set("unbekannt")
        label_owner = tk.Label(owner_label_box, textvariable=self.OwnerLabelText)
        label_owner.pack(side="left", pady="10")

        self.TerminRadiobuttonBoxList = []
        self.TerminRadiobuttonList = []
        self.Termine = []
        self.choosenTermin = tk.IntVar()
        self.choosenTermin.set(0)

        deletion_button_box = tk.Frame(master=self.TerminBox)
        deletion_button_box.pack(side="top", fill="x", padx="5", pady="5")

        self.B_deleteDate = tk.Button(deletion_button_box, text="Termin löschen!",
                                      command=(lambda: self.delete_date(self.Termine[self.choosenTermin.get()][0])))
        self.B_deleteDate.config(state="disabled")
        self.B_deleteDate.pack(side="left")

        status_box = tk.Frame(master=self.TerminBox)
        status_box.pack(side="top", fill="x", padx="5", pady="5")

        self.StatusText = tk.StringVar()
        label_state = tk.Label(status_box, textvariable=self.StatusText)
        label_state.pack(side="left", pady="5")

    def delete_date(self, iid):
        dba.delete_date(iid)
        self.B_deleteDate.config(state="disabled")
        self.StatusText.set("Termin Nummer " + str(iid) + " gelöscht!")
        self.print_termin(self.Owner[0])

    def print_termin(self, bid):
        self.Termine = dba.print_termin(bid)

        if self.Termine:
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
                                                                 text=Termin[1].strftime("%d.%m.%Y") + ": " +
                                                                 str(Termin[2]) +
                                                                 " Hühner, bezahlt: " +
                                                                 str(Termin[3]).replace("True", "Ja").replace("False",
                                                                                                              "Nein"),
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

    def search(self, nachname: str, plz: str):
        nachname = nachname.replace(" ", "")
        plz = plz.replace(" ", "")

        self.Owners = dba.search(nachname, plz)

        if not self.Owners:
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
            if self.isDistinct is not None:
                self.isSearch = True

            if not self.isDistinct:
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

    def confirm(self, owner):
        self.Owner = owner
        self.isConfirm = True
        self.B_deleteDate.config(state="normal")
        self.print_termin(owner[0])
        self.OwnerLabelText.set(str(self.Owner[1]) + " " + str(self.Owner[2]) + ": " +
                                str(self.Owner[3]) + " " + str(self.Owner[4]) + " " + str(self.Owner[5]) + " " +
                                str(self.Owner[6]) + " - " + str(self.Owner[7]))

    def show(self):
        self.lift()
        root.title("Hühnerliste - Termin löschen")


# Page delete Owner - user can delete a owner
class PageDeleteOwner(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.isSearch = False
        self.isConfirm = False
        self.isDistinct = None
        self.Owners = None
        self.Owner = None

        label_box = tk.Frame(master=self)
        label_box.pack(side="top", fill="x", padx="5", pady="5")
        label = tk.Label(label_box, text="Besitzer löschen", font=55)
        label.pack(fill="x", side="left")

        self.searchBox = tk.Frame(master=self, borderwidth=2, relief="groove")
        self.searchBox.pack(side="top", fill="x", padx="5", pady="5")

        name_box = tk.Frame(master=self.searchBox)
        name_box.pack(side="top", fill="x", pady=5)
        tk.Label(name_box, text="Nachname: ").pack(side="left", padx="5")
        self.E_nname = tk.Entry(name_box)
        self.E_nname.pack(side="left", padx="5")

        plz_box = tk.Frame(master=self.searchBox)
        plz_box.pack(side="top", fill="x", pady=5)
        tk.Label(plz_box, text="PLZ: ").pack(side="left", padx="5")
        self.E_plz = tk.Entry(plz_box)
        self.E_plz.pack(side="left", padx="43")

        button_box = tk.Frame(master=self.searchBox)
        button_box.pack(side="top", fill="x", padx="5", pady="5")

        button_search_button = tk.Button(button_box, text="Suche",
                                         command=(lambda: self.search(self.E_nname.get(), self.E_plz.get())))
        button_search_button.pack(side="left")
        self.SearchStatusText = tk.StringVar()
        self.SearchStatusText.set("")
        label_state = tk.Label(button_box, textvariable=self.SearchStatusText)
        label_state.pack(side="left", pady="5", padx="20")

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

        delete_box = tk.Frame(master=self)
        delete_box.pack(side="top", fill="x", padx="5", pady="5")

        owner_box = tk.Frame(master=delete_box)
        owner_box.pack(side="top", fill="x", pady=5)
        owner_label_box = tk.Frame(master=owner_box)
        owner_label_box.pack(side="top", fill="x", pady=5)
        tk.Label(owner_label_box, text="Besitzer: ").pack(side="left", padx="5")
        self.OwnerLabelText = tk.StringVar()
        self.OwnerLabelText.set("unbekannt")
        label_owner = tk.Label(owner_label_box, textvariable=self.OwnerLabelText)
        label_owner.pack(side="left", pady="10")

        deletion_button_box = tk.Frame(master=delete_box)
        deletion_button_box.pack(side="top", fill="x", padx="5", pady="5")

        self.B_deleteOwner = tk.Button(deletion_button_box, text="Besitzer löschen!",
                                       command=(lambda: self.delete_owner(self.Owner[0])))
        self.B_deleteOwner.config(state="disabled")
        self.B_deleteOwner.pack(side="left")

        status_box = tk.Frame(master=delete_box)
        status_box.pack(side="top", fill="x", padx="5", pady="5")

        self.StatusText = tk.StringVar()
        label_state = tk.Label(status_box, textvariable=self.StatusText)
        label_state.pack(side="left", pady="5")

    def delete_owner(self, bid):
        dba.delete_owner(bid)

        self.B_deleteOwner.config(state="disabled")
        self.StatusText.set("Besitzer Nummer " + str(bid) + " mit allen Terminen gelöscht!")
        self.search(self.E_nname.get(), self.E_plz.get())

    def search(self, nachname: str, plz: str):
        nachname = nachname.replace(" ", "")
        plz = plz.replace(" ", "")

        self.Owners = dba.search(nachname, plz)

        if not self.Owners:
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
            if self.isDistinct is not None:
                self.isSearch = True

            if not self.isDistinct:
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

    def confirm(self, owner):
        self.Owner = owner
        self.isConfirm = True
        self.B_deleteOwner.config(state="normal")
        self.OwnerLabelText.set(str(self.Owner[1]) + " " + str(self.Owner[2]) + ": " +
                                str(self.Owner[3]) + " " + str(self.Owner[4]) + " " + str(self.Owner[5]) + " " +
                                str(self.Owner[6]) + " - " + str(self.Owner[7]))

    def show(self):
        self.lift()
        root.title("Hühnerliste - Besitzer löschen")


# Page alter Owner - user can alter a owner
class PageAlterOwner(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.isSearch = False
        self.isConfirm = False
        self.isDistinct = None
        self.Owners = None
        self.Owner = None

        label_box = tk.Frame(master=self)
        label_box.pack(side="top", fill="x", padx="5", pady="5")
        label = tk.Label(label_box, text="Besitzerdaten ändern", font=55)
        label.pack(fill="x", side="left")

        self.searchBox = tk.Frame(master=self, borderwidth=2, relief="groove")
        self.searchBox.pack(side="top", fill="x", padx="5", pady="5")

        name_box = tk.Frame(master=self.searchBox)
        name_box.pack(side="top", fill="x", pady=5)
        tk.Label(name_box, text="Nachname: ").pack(side="left", padx="5")
        self.entryNName = tk.Entry(name_box)
        self.entryNName.pack(side="left", padx="5")

        plz_box = tk.Frame(master=self.searchBox)
        plz_box.pack(side="top", fill="x", pady=5)
        tk.Label(plz_box, text="PLZ: ").pack(side="left", padx="5")
        self.E_plz = tk.Entry(plz_box)
        self.E_plz.pack(side="left", padx="43")

        button_box = tk.Frame(master=self.searchBox)
        button_box.pack(side="top", fill="x", padx="5", pady="5")

        button_search_button = tk.Button(button_box, text="Suche",
                                         command=(lambda: self.search(self.entryNName.get(), self.E_plz.get())))
        button_search_button.pack(side="left")
        self.SearchStatusText = tk.StringVar()
        self.SearchStatusText.set("")
        label_state = tk.Label(button_box, textvariable=self.SearchStatusText)
        label_state.pack(side="left", pady="5", padx="20")

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

        alter_box = tk.Frame(master=self)
        alter_box.pack(side="top", fill="x", padx="5", pady="5")

        verification_box = tk.Frame(master=alter_box)
        verification_box.pack(side="top", fill="x", pady=5)
        verification_label_box = tk.Frame(master=verification_box)
        verification_label_box.pack(side="top", fill="x", pady=5)
        tk.Label(verification_label_box, text="Besitzer: ").pack(side="left", padx="5")
        self.VerificationLabelText = tk.StringVar()
        self.VerificationLabelText.set("unbekannt")
        label_owner = tk.Label(verification_label_box, textvariable=self.VerificationLabelText)
        label_owner.pack(side="left", pady="10")

        # Ownerdata I/O
        owner_box = tk.Frame(master=self, borderwidth=2, relief="groove")
        owner_box.pack(side="top", fill="x", padx="5",
                       pady="5")

        name_box = tk.Frame(owner_box)
        name_box.pack(side="top", fill="x", pady=5)

        vname_box = tk.Frame(name_box)
        vname_box.pack(side="left", fill="x")
        tk.Label(vname_box, text="Vorname").pack(side="left", padx="5")
        self.entryVName = tk.Entry(vname_box, state='disabled')
        self.entryVName.pack(side="left", padx="5")

        nname_box = tk.Frame(name_box)
        nname_box.pack(side="left", fill="x")
        tk.Label(nname_box, text="Nachname *").pack(side="left", padx="5")
        self.entryONName = tk.Entry(nname_box, state='disabled')
        self.entryONName.pack(side="left", padx="5")

        adress_box = tk.Frame(owner_box)
        adress_box.pack(side="top", fill="x", pady=5)

        plz_box = tk.Frame(adress_box)
        plz_box.pack(side="left", fill="x")
        tk.Label(plz_box, text="PLZ *").pack(side="left", padx="5")
        self.entryPlz = tk.Entry(plz_box, state='disabled')
        self.entryPlz.pack(side="left", padx="25")

        ort_box = tk.Frame(adress_box)
        ort_box.pack(side="left", fill="x")
        tk.Label(ort_box, text="Ort *").pack(side="left", padx="5")
        self.entryOrt = tk.Entry(ort_box, state='disabled')
        self.entryOrt.pack(side="left", padx="25")

        strasse_box = tk.Frame(adress_box)
        strasse_box.pack(side="left", fill="x")
        tk.Label(strasse_box, text="Strasse *").pack(side="left", padx="5")
        self.entryStrasse = tk.Entry(strasse_box, state='disabled')
        self.entryStrasse.pack(side="left", padx="5")

        haus_box = tk.Frame(adress_box)
        haus_box.pack(side="left", fill="x")
        tk.Label(haus_box, text="Hausnummer *").pack(side="left", padx="5")
        self.entryHaus = tk.Entry(haus_box, state='disabled')
        self.entryHaus.pack(side="left", padx="5")

        tel_box = tk.Frame(owner_box)
        tel_box.pack(side="top", fill="x", pady=5)

        tk.Label(tel_box, text="Telefonnummer").pack(side="left", padx="5")
        self.entryTel = tk.Entry(tel_box, state='disabled')
        self.entryTel.pack(side="left", padx="5")

        button_box = tk.Frame(master=owner_box)
        button_box.pack(side="top", fill="x", padx="5", pady="5")

        self.buttonSaveButton = tk.Button(button_box, text="Daten speichern", state='disabled',
                                          command=(lambda: self.test_input()))
        self.buttonSaveButton.pack(side="left")

        status_box = tk.Frame(master=self)
        status_box.pack(side="top", fill="x", padx="5", pady="5")

        self.StatusText = tk.StringVar()
        label_state = tk.Label(status_box, textvariable=self.StatusText)
        label_state.pack(side="left", pady="5")

    def search(self, nachname: str, plz: str):
        nachname = nachname.replace(" ", "")
        plz = plz.replace(" ", "")

        self.Owners = dba.search(nachname, plz)

        self.entryVName.config(state='disabled')
        self.entryONName.config(state='disabled')
        self.entryHaus.config(state='disabled')
        self.entryOrt.config(state='disabled')
        self.entryPlz.config(state='disabled')
        self.entryStrasse.config(state='disabled')
        self.entryTel.config(state='disabled')
        self.buttonSaveButton.config(state='disabled')

        if not self.Owners:
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
            if self.isDistinct is not None:
                self.isSearch = True

            if not self.isDistinct:
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

                self.entryVName.config(state='normal')
                self.entryONName.config(state='normal')
                self.entryHaus.config(state='normal')
                self.entryOrt.config(state='normal')
                self.entryPlz.config(state='normal')
                self.entryStrasse.config(state='normal')
                self.entryTel.config(state='normal')
                self.buttonSaveButton.config(state='normal')

                self.entryVName.delete(0, 'end')
                self.entryONName.delete(0, 'end')
                self.entryHaus.delete(0, 'end')
                self.entryOrt.delete(0, 'end')
                self.entryPlz.delete(0, 'end')
                self.entryStrasse.delete(0, 'end')
                self.entryTel.delete(0, 'end')

                self.entryVName.insert(0, self.Owner[1])
                self.entryONName.insert(0, self.Owner[2])
                self.entryPlz.insert(0, self.Owner[3])
                self.entryOrt.insert(0, self.Owner[4])
                self.entryStrasse.insert(0, self.Owner[5])
                self.entryHaus.insert(0, self.Owner[6])
                self.entryTel.insert(0, self.Owner[7])

    def confirm(self, owner):
        self.Owner = owner
        self.isConfirm = True
        # self.B_deleteOwner.config(state="normal")
        self.VerificationLabelText.set(str(self.Owner[0]) + ": " + str(self.Owner[1]) + " " +
                                       str(self.Owner[2]) + ": " + str(self.Owner[3]) + " " +
                                       str(self.Owner[4]) + ", " + str(self.Owner[5]) + " " +
                                       str(self.Owner[6]) + " - " + str(self.Owner[7]))
        self.entryVName.config(state='normal')
        self.entryONName.config(state='normal')
        self.entryHaus.config(state='normal')
        self.entryOrt.config(state='normal')
        self.entryPlz.config(state='normal')
        self.entryStrasse.config(state='normal')
        self.entryTel.config(state='normal')
        self.buttonSaveButton.config(state='normal')

        self.entryVName.delete(0, 'end')
        self.entryONName.delete(0, 'end')
        self.entryHaus.delete(0, 'end')
        self.entryOrt.delete(0, 'end')
        self.entryPlz.delete(0, 'end')
        self.entryStrasse.delete(0, 'end')
        self.entryTel.delete(0, 'end')

        self.entryVName.insert(0, self.Owner[1])
        self.entryONName.insert(0, self.Owner[2])
        self.entryPlz.insert(0, self.Owner[3])
        self.entryOrt.insert(0, self.Owner[4])
        self.entryStrasse.insert(0, self.Owner[5])
        self.entryHaus.insert(0, self.Owner[6])
        self.entryTel.insert(0, self.Owner[7])

    def test_input(self):
        valid_input = True

        plz = self.entryPlz.get()
        plz = plz.replace(" ", "")
        if not (plz.isnumeric()):
            valid_input = False

        if len(self.entryTel.get()) > 0:
            tel = self.entryTel.get()
            tel = tel.replace(" ", "")
            if not (tel.isnumeric()):
                valid_input = False

        entry_list = [self.entryONName, self.entryPlz, self.entryOrt, self.entryStrasse, self.entryHaus]

        is_empty = False
        for Entry in entry_list:
            if len(Entry.get()) == 0:
                is_empty = True
        if is_empty:
            self.StatusText.set("Bitte fülle alle Pflichtfelder und achte auf sinnvolle Eingaben!")
            valid_input = False

        if valid_input:
            success = dba.alter_owner(self.Owner[0], self.entryONName.get().replace(" ", ""),
                                      self.entryPlz.get().replace(" ", ""), self.entryOrt.get().replace(" ", ""),
                                      self.entryStrasse.get().replace(" ", ""), self.entryHaus.get().replace(" ", ""),
                                      self.entryVName.get().replace(" ", ""), self.entryTel.get().replace(" ", ""))

            if success:
                self.StatusText.set("Erfolgreich geändert!")
            else:
                self.StatusText.set("Fehler beim ändern aufgetreten!")

        else:
            self.StatusText.set("Bitte fülle alle Pflichtfelder und achte auf sinnvolle Eingaben!")

    def show(self):
        self.lift()
        root.title("Hühnerliste - Besitzerdaten ändern")


# Page alter Termin - user can alter a appointment for a choosen owner
class PageAlterDate(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.isSearch = False
        self.isConfirm = False
        self.isDistinct = None
        self.Owners = None
        self.Owner = None

        label_box = tk.Frame(master=self)
        label_box.pack(side="top", fill="x", padx="5", pady="5")
        label = tk.Label(label_box, text="Impftermin ändern", font=55)
        label.pack(fill="x", side="left")

        self.searchBox = tk.Frame(master=self, borderwidth=2, relief="groove")
        self.searchBox.pack(side="top", fill="x", padx="5", pady="5")

        name_box = tk.Frame(master=self.searchBox)
        name_box.pack(side="top", fill="x", pady=5)
        tk.Label(name_box, text="Nachname: ").pack(side="left", padx="5")
        self.entryNName = tk.Entry(name_box)
        self.entryNName.pack(side="left", padx="5")

        plz_box = tk.Frame(master=self.searchBox)
        plz_box.pack(side="top", fill="x", pady=5)
        tk.Label(plz_box, text="PLZ: ").pack(side="left", padx="5")
        self.E_plz = tk.Entry(plz_box)
        self.E_plz.pack(side="left", padx="43")

        button_box = tk.Frame(master=self.searchBox)
        button_box.pack(side="top", fill="x", padx="5", pady="5")

        button_search_button = tk.Button(button_box, text="Suche",
                                         command=(lambda: self.search(self.entryNName.get(), self.E_plz.get())))
        button_search_button.pack(side="left")
        self.SearchStatusText = tk.StringVar()
        self.SearchStatusText.set("")
        label_state = tk.Label(button_box, textvariable=self.SearchStatusText)
        label_state.pack(side="left", pady="5", padx="20")

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

        verification_box = tk.Frame(master=self.TerminBox)
        verification_box.pack(side="top", fill="x", pady=5)
        verification_label_box = tk.Frame(master=verification_box)
        verification_label_box.pack(side="top", fill="x", pady=5)
        tk.Label(verification_label_box, text="Besitzer: ").pack(side="left", padx="5")
        self.VerificationLabelText = tk.StringVar()
        self.VerificationLabelText.set("unbekannt")
        label_owner = tk.Label(verification_label_box, textvariable=self.VerificationLabelText)
        label_owner.pack(side="left", pady="10")

        self.TerminRadiobuttonBoxList = []
        self.TerminRadiobuttonList = []
        self.TerminIid = []
        self.TerminSpinboxDayList = []
        self.TerminSpinboxMonthList = []
        self.TerminSpinboxYearList = []
        self.TerminVarDayList = []
        self.TerminVarMonthList = []
        self.TerminVarYearList = []
        self.TerminEntryHuehnerList = []
        self.TerminCheckbuttonPaidList = []
        self.TerminVarPaidList = []
        self.Termine = []
        self.choosenTermin = tk.IntVar()
        self.choosenTermin.set(0)

        alter_button_box = tk.Frame(master=self.TerminBox)
        alter_button_box.pack(side="top", fill="x", padx="5", pady="5")

        self.button_alter_date = tk.Button(alter_button_box, text="Termin ändern!",
                                           command=(lambda: self.alter_date()))
        self.button_alter_date.config(state="disabled")
        self.button_alter_date.pack(side="left")

        status_box = tk.Frame(master=self)
        status_box.pack(side="top", fill="x", padx="5", pady="5")

        self.StatusText = tk.StringVar()
        label_state = tk.Label(status_box, textvariable=self.StatusText)
        label_state.pack(side="left", pady="5")

    def search(self, nachname: str, plz: str):
        nachname = nachname.replace(" ", "")
        plz = plz.replace(" ", "")

        self.Owners = dba.search(nachname, plz)

        if not self.Owners:
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
            if self.isDistinct is not None:
                self.isSearch = True

            if not self.isDistinct:
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

    def print_termin(self, bid):
        # get all dates for choosen owner given by its bid
        # for each date create a new interactive line

        self.Termine = dba.print_termin(bid)

        if self.Termine:
            self.StatusText.set("")
            self.button_alter_date.config(state="normal")

            for TerminRadiobuttonBox in self.TerminRadiobuttonBoxList:
                TerminRadiobuttonBox.pack_forget()

            for TerminRadiobutton in self.TerminRadiobuttonList:
                TerminRadiobutton.pack_forget()

            for TerminSpinboxDay in self.TerminSpinboxDayList:
                TerminSpinboxDay.pack_forget()

            for TerminSpinboxMonth in self.TerminSpinboxMonthList:
                TerminSpinboxMonth.pack_forget()

            for TerminSpinboxYear in self.TerminSpinboxYearList:
                TerminSpinboxYear.pack_forget()

            for TerminEntryHuehner in self.TerminEntryHuehnerList:
                TerminEntryHuehner.pack_forget()

            for TerminCheckbuttonPaid in self.TerminCheckbuttonPaidList:
                TerminCheckbuttonPaid.pack_forget()

            self.TerminRadiobuttonBoxList = []
            self.TerminRadiobuttonList = []
            self.TerminIid = []
            self.TerminSpinboxDayList = []
            self.TerminSpinboxMonthList = []
            self.TerminSpinboxYearList = []
            self.TerminVarDayList = []
            self.TerminVarMonthList = []
            self.TerminVarYearList = []
            self.TerminEntryHuehnerList = []
            self.TerminCheckbuttonPaidList = []
            self.TerminVarPaidList = []
            self.choosenTermin = tk.IntVar()
            self.choosenTermin.set(0)

            i = 0
            for Termin in self.Termine:
                # generate for all dates a changeable List of dates values
                # Radiobutton, Date, Huehner Anzahl, paid
                self.TerminRadiobuttonBoxList.append(tk.Frame(master=self.TerminBox))
                self.TerminRadiobuttonList.append(tk.Radiobutton(master=self.TerminRadiobuttonBoxList[i],
                                                                 variable=self.choosenTermin,
                                                                 value=i))
                self.TerminIid.append(Termin[0])

                label_date = tk.Label(self.TerminRadiobuttonBoxList[i], text="Date: ")
                self.TerminVarDayList.append(tk.IntVar())
                self.TerminVarDayList[i].set(Termin[1].strftime("%d"))
                self.TerminSpinboxDayList.append(
                    ttk.Spinbox(self.TerminRadiobuttonBoxList[i], from_=1, to=31,
                                textvariable=self.TerminVarDayList[i], width=5))

                self.TerminVarMonthList.append(tk.IntVar())
                self.TerminVarMonthList[i].set(Termin[1].strftime("%m"))
                self.TerminSpinboxMonthList.append(
                    ttk.Spinbox(self.TerminRadiobuttonBoxList[i], from_=1, to=12,
                                textvariable=self.TerminVarMonthList[i], width=5))

                self.TerminVarYearList.append(tk.IntVar())
                self.TerminVarYearList[i].set(Termin[1].strftime("%Y"))
                self.TerminSpinboxYearList.append(
                    ttk.Spinbox(self.TerminRadiobuttonBoxList[i], from_=2019, to=2030,
                                textvariable=self.TerminVarYearList[i], width=5))

                label_huehner = tk.Label(self.TerminRadiobuttonBoxList[i], text="Hühner: ")
                self.TerminEntryHuehnerList.append(tk.Entry(self.TerminRadiobuttonBoxList[i]))
                self.TerminEntryHuehnerList[i].insert(0, Termin[2])

                label_paid = tk.Label(self.TerminRadiobuttonBoxList[i], text="bezahlt: ")
                self.TerminVarPaidList.append(tk.IntVar())
                self.TerminVarPaidList[i].set(Termin[3])
                self.TerminCheckbuttonPaidList.append(tk.Checkbutton(self.TerminRadiobuttonBoxList[i], text="",
                                                                     variable=self.TerminVarPaidList[i]))

                self.TerminRadiobuttonBoxList[i].pack(side="top", fill="x", pady="5")
                self.TerminRadiobuttonList[i].pack(side="left", padx="5")
                label_date.pack(side="left", padx="5")
                self.TerminSpinboxDayList[i].pack(side="left", padx="5")
                self.TerminSpinboxMonthList[i].pack(side="left", padx="5")
                self.TerminSpinboxYearList[i].pack(side="left", padx="5")
                label_huehner.pack(side="left", padx="5")
                self.TerminEntryHuehnerList[i].pack(side="left", padx="5")
                label_paid.pack(side="left", padx="5")
                self.TerminCheckbuttonPaidList[i].pack(side="left", padx="5")

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
            self.button_alter_date.config(state="disabled")
            self.StatusText.set("Für diesen Besitzer wurden leider keine Termine gefunden!")

    def confirm(self, owner):
        # confirm the choosen owner, save it and display it
        self.Owner = owner
        self.isConfirm = True
        self.print_termin(owner[0])
        self.VerificationLabelText.set(str(self.Owner[0]) + ": " + str(self.Owner[1]) + " " +
                                       str(self.Owner[2]) + ": " + str(self.Owner[3]) + " " +
                                       str(self.Owner[4]) + ", " + str(self.Owner[5]) + " " +
                                       str(self.Owner[6]) + " - " + str(self.Owner[7]))

    def alter_date(self):
        # prepare data locally before db access
        valid_input = True

        i = self.choosenTermin.get()

        iid = self.TerminIid[i]
        date_string = str(self.TerminVarYearList[i].get()) + "-" + \
                      str(self.TerminVarMonthList[i].get()) + "-" + \
                      str(self.TerminVarDayList[i].get())
        datum = datetime.strptime(date_string, '%Y-%m-%d')

        huehner = self.TerminEntryHuehnerList[i].get().replace(" ", "")

        # test if huhner is a number and not NULL
        if not huehner.isnumeric() or not len(huehner):
            valid_input = False

        huehner = int(huehner)

        bezahlt = bool(self.TerminVarPaidList[i].get())

        # if input valid try writing to db, disable the button and give controll to a refresh
        # display an error msg to screen if problem ocurred
        if valid_input:
            success = dba.alter_termin(iid, datum, huehner, bezahlt)
            self.button_alter_date.config(state="disable")

            if success:
                self.SearchStatusText.set("Termin Nummer " + str(iid) + " geändert zu: Datum: " + str(datum.date()) +
                                          " Hühner: " + str(huehner) +
                                          " bezahlt: " + str(bezahlt))
                self.print_termin(self.Owner[0])
            else:
                self.SearchStatusText.set("Fehler beim Schreiben in die Datenbank.")

        else:
            self.SearchStatusText.set("Bitte überprüfe deine Eingaben.")

    def show(self):
        self.lift()
        root.title("Hühnerliste - Impftermin ändern")


# Page delete Owner - user can delete a owner
class PagePrintPDF(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.isSearch = False
        self.isConfirm = False
        self.isDistinct = None
        self.Owners = None
        self.Owner = None

        label_box = tk.Frame(master=self)
        label_box.pack(side="top", fill="x", padx="5", pady="5")
        label = tk.Label(label_box, text="Impfnachweis erstellen", font=55)
        label.pack(fill="x", side="left")

        self.searchBox = tk.Frame(master=self, borderwidth=2, relief="groove")
        self.searchBox.pack(side="top", fill="x", padx="5", pady="5")

        name_box = tk.Frame(master=self.searchBox)
        name_box.pack(side="top", fill="x", pady=5)
        tk.Label(name_box, text="Nachname: ").pack(side="left", padx="5")
        self.E_nname = tk.Entry(name_box)
        self.E_nname.pack(side="left", padx="5")

        plz_box = tk.Frame(master=self.searchBox)
        plz_box.pack(side="top", fill="x", pady=5)
        tk.Label(plz_box, text="PLZ: ").pack(side="left", padx="5")
        self.E_plz = tk.Entry(plz_box)
        self.E_plz.pack(side="left", padx="43")

        button_box = tk.Frame(master=self.searchBox)
        button_box.pack(side="top", fill="x", padx="5", pady="5")

        button_search_button = tk.Button(button_box, text="Suche",
                                         command=(lambda: self.search(self.E_nname.get(), self.E_plz.get())))
        button_search_button.pack(side="left")
        self.SearchStatusText = tk.StringVar()
        self.SearchStatusText.set("")
        label_state = tk.Label(button_box, textvariable=self.SearchStatusText)
        label_state.pack(side="left", pady="5", padx="20")

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

        ver_box = tk.Frame(master=self)
        ver_box.pack(side="top", fill="x", padx="5", pady="5")

        owner_box = tk.Frame(master=ver_box)
        owner_box.pack(side="top", fill="x", pady=5)
        owner_label_box = tk.Frame(master=owner_box)
        owner_label_box.pack(side="top", fill="x", pady=5)
        tk.Label(owner_label_box, text="Besitzer: ").pack(side="left", padx="5")
        self.OwnerLabelText = tk.StringVar()
        self.OwnerLabelText.set("unbekannt")
        label_owner = tk.Label(owner_label_box, textvariable=self.OwnerLabelText)
        label_owner.pack(side="left", pady="10")

        create_ver_button_box = tk.Frame(master=ver_box)
        create_ver_button_box.pack(side="top", fill="x", padx="5", pady="5")

        self.B_createVer = tk.Button(create_ver_button_box, text="Nachweis erstellen!",
                                       command=(lambda: self.create_verification(self.Owner)))
        self.B_createVer.config(state="disabled")
        self.B_createVer.pack(side="left")

        self.B_createOwnerVer = tk.Button(create_ver_button_box, text="Besitzer Version erstellen!",
                                     command=(lambda: self.create_owner_version(self.Owner)))
        self.B_createOwnerVer.config(state="disabled")
        self.B_createOwnerVer.pack(side="left", padx="5")

        status_box = tk.Frame(master=ver_box)
        status_box.pack(side="top", fill="x", padx="5", pady="5")

        self.StatusText = tk.StringVar()
        label_state = tk.Label(status_box, textvariable=self.StatusText)
        label_state.pack(side="left", pady="5")

    def create_verification(self, owner):
        bid = owner[0]

        termin_data = dba.get_huehner_date_from_newest_impfdate(bid)

        if termin_data:

            filename = fdialog.asksaveasfilename(filetypes=[('PDF Dokumente', '*.pdf'), ('Alle Dateien', '*')])

            name = owner[1] + " " + owner[2]

            address = owner[5] + " " + owner[6] + ", " + owner[3] + " " + owner[4]
            try:
                pdf.create_official_pdf(filename, name, termin_data[0],
                                        datetime.strftime(termin_data[1], "%d.%m.%Y"), address)
                self.B_createVer.config(state="disabled")
                self.StatusText.set(
                    "Offizieles Dokument für den neuesten Termin von Besitzernummer" + str(bid) + " erstellt!")
                self.search(self.E_nname.get(), self.E_plz.get())
            except Exception as e:
                self.StatusText.set(
                    "Ein Fehler ist aufgetreten: " + str(e))
        else:
            self.B_createVer.config(state="disabled")
            self.B_createOwnerVer.config(state="disabled")
            self.StatusText.set("Dieser Besitzer hatte noch keinen Impftermin!")

    def create_owner_version(self, owner):
        bid = owner[0]

        termin_data = dba.get_newest_impfdate(bid)

        if termin_data:

            date = termin_data[0]
            iid = termin_data[1]

            name = owner[1] + " " + owner[2]

            filename = fdialog.asksaveasfilename(filetypes=[('PDF Dokumente', '*.pdf'), ('Alle Dateien', '*')])

            qr_encrypt.make_qr_url(owner[2], str(iid))

            try:
                pdf.create_owner_pdf(filename, name, datetime.strftime(date, "%d.%m.%Y"))

                self.B_createOwnerVer.config(state="disabled")
                self.StatusText.set("Besitzer Dokument für den neuesten Termin von Besitzernummer" +
                                    str(bid) + " erstellt!")
                self.search(self.E_nname.get(), self.E_plz.get())
            except Exception as e:
                self.StatusText.set(
                    "Ein Fehler ist aufgetreten: " + str(e))

        else:
            self.B_createVer.config(state="disabled")
            self.B_createOwnerVer.config(state="disabled")
            self.StatusText.set("Dieser Besitzer hatte noch keinen Impftermin!")

    def search(self, nachname: str, plz: str):
        nachname = nachname.replace(" ", "")
        plz = plz.replace(" ", "")

        self.Owners = dba.search(nachname, plz)

        if not self.Owners:
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
            if self.isDistinct is not None:
                self.isSearch = True

            if not self.isDistinct:
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

    def confirm(self, owner):
        self.Owner = owner
        self.isConfirm = True
        self.B_createVer.config(state="normal")
        self.B_createOwnerVer.config(state="normal")
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
        page_view_print = PageViewAllPrintAll(self)
        page_owner = PageOwner(self)
        page_termin_one = PageAddTerminOne(self)
        page_termin_multiple = PageAddTerminMultiple(self)
        page_confirm = PageConfirmPayment(self)
        page_delete_date = PageDeleteDate(self)
        page_delete_owner = PageDeleteOwner(self)
        page_alter_owner = PageAlterOwner(self)
        page_alter_date = PageAlterDate(self)
        page_print_pdf = PagePrintPDF(self)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        page_view_print.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        page_owner.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        page_termin_one.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        page_termin_multiple.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        page_confirm.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        page_delete_date.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        page_delete_owner.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        page_alter_owner.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        page_alter_date.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        page_print_pdf.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        # Menu for changing pages
        menu = tk.Menu(root)
        root.config(menu=menu)
        pagemenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Funktionen", menu=pagemenu)

        pagemenu.add_command(label="Vorschau und Drucken", command=page_view_print.show)
        pagemenu.add_separator()

        addmenu = tk.Menu(pagemenu, tearoff=0)
        pagemenu.add_cascade(label="Hinzufügen", menu=addmenu)
        addmenu.add_command(label="Besitzer hinzufügen", command=page_owner.show)

        terminmenu = tk.Menu(addmenu, tearoff=0)
        addmenu.add_cascade(label="Termin hinzufügen", menu=terminmenu)
        terminmenu.add_command(label="Ein Besitzer", command=page_termin_one.show)
        terminmenu.add_command(label="Mehrere Besitzer", command=page_termin_multiple.show)
        pagemenu.add_separator()

        altermenu = tk.Menu(pagemenu, tearoff=0)
        pagemenu.add_cascade(label="Ändern", menu=altermenu)
        altermenu.add_command(label="Besitzerdaten ändern", command=page_alter_owner.show)
        altermenu.add_command(label="Termindaten ändern", command=page_alter_date.show)
        pagemenu.add_separator()

        deletemenu = tk.Menu(pagemenu, tearoff=0)
        pagemenu.add_cascade(label="Löschen", menu=deletemenu)
        deletemenu.add_command(label="Besitzer löschen", command=page_delete_owner.show)
        deletemenu.add_command(label="Termin löschen", command=page_delete_date.show)
        pagemenu.add_separator()

        pagemenu.add_command(label="Zahlung bearbeiten", command=page_confirm.show)
        pagemenu.add_separator()

        pagemenu.add_command(label="PDFs", command=page_print_pdf.show)

        page_view_print.show()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Hühnerliste")
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("1280x720")
    root.mainloop()
