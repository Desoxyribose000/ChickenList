#!/usr/bin/python3

# Autor: Max Nowak
# Version: 0.4 wip - PDF Generation
# Programm for Manipulation of ChickenList DB
# QR Code Creator

import qrcode as qr

data = "https://www.google.de"


def make_qr_url(url):
    code = qr.QRCode(version=1, box_size=10, border=2)
    code.add_data(url)
    code.make(fit=True)
    img = code.make_image()

    img.save("qrcode.png")
