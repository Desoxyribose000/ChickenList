#!/usr/bin/python3

# Autor: Max Nowak
# Version: 0.4 wip - PDF Generation
# Programm for Manipulation of ChickenList DB
# PDF Creator


from fpdf import FPDF


class PDF(FPDF):
    title = "title"
    sub_title = "sub_title"

    def set_title(self, title):
        self.title = title

    def set_sub_title(self, sub_title):
        self.sub_title = sub_title

    def header(self):
        self.set_font('Arial', 'B', 15)
        # Calculate width of title and position
        w = self.get_string_width(self.title) + 6
        self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        self.set_draw_color(255, 255, 255)
        self.set_fill_color(255, 255, 255)
        self.set_text_color(0, 0, 0)
        # Thickness of frame (1 mm)
        self.set_line_width(1)
        # Title
        self.cell(w, 9, self.title, 1, 1, 'C', 1)
        # Subtitle
        self.set_font('Arial', '', 8)
        w = self.get_string_width(self.sub_title) + 6
        self.set_x((210 - w) / 2)
        self.cell(w, 9, "(" + self.sub_title + ")", 1, 1, 'C', 1)
        # Line break
        self.ln(10)

    def data_layout(self, key, data):
        # Arial 12
        self.set_font('Arial', '', 12)
        # Background color
        self.set_fill_color(255, 255, 255)
        # Title
        self.cell(0, 6, '%s : %s' % (key, data), 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def auth(self):
        # Select Arial italic 8
        self.set_font('Arial', '', 12)
        # Print centered page number
        self.cell(0, 10, 'Unterschrift und Stempel: ', 0, 0, 'L')

    def print_qrcode(self):
        self.set_font('Arial', '', 12)
        self.cell(0, 10, 'Bitte Scannen Sie den QR-Code mit Ihrem Handy.', 0, 2, 'R')
        self.cell(0, 10, 'Anschließend öffnet sich eine Webseite, die Ihnen zeigt,', 0, 2, 'R')
        self.cell(0, 10, 'wann sie das nächste mal zu impfen müssen.', 0, 2, 'R')

        self.set_xy(6, 50)
        self.image("qrcode.png", type='', h=70, w=70)

    def print_data(self, key, data):
        self.data_layout(key, data)


def create_official_pdf(filename, name, huehner, date, address):
    pdf = PDF(orientation='L', unit='mm', format='A5')
    pdf.set_title("Impfschutzverordnung")
    pdf.set_sub_title("gemäß Geflügelpest-Verordnung")
    pdf.add_page()
    pdf.print_data("Besitzer", name)
    pdf.print_data("Anschrift", address)
    pdf.print_data("Tierart", "Zuchttiere")
    pdf.print_data("Anzahl", str(huehner))
    pdf.print_data("Datum der Impfung", str(date))
    pdf.print_data("Verwendeter Impfstoff", "Nobilis© ND Hitcher")
    pdf.auth()
    pdf.output(filename + ".pdf", 'F')


def create_owner_pdf(filename, name, date):
    pdf = PDF(orientation='L', unit='mm', format='A5')
    pdf.set_title("Impfdatum Erinnerung")
    pdf.set_sub_title(name)
    pdf.add_page()
    pdf.print_data("Letztes Impfdatum", str(date))

    pdf.print_qrcode()
    pdf.output(filename + ".pdf", 'F')
