#!/usr/bin/python3

# Autor: Max Nowak
# Version: 0.5 wip - Cloud Access
# Programm for Manipulation of ChickenList DB
# QR Code Creator

import qrcode as qr
import hashlib
import random
import os

host = str(os.environ['WEBHOST'])


# erstellt einen QR
def make_qr_url(last_name, iid):
    # create random string of length 10
    random_string = ''

    for _ in range(10):
        random_i = random.randint(97, 97 + 25)

        # convert to uppercase if flip is set
        flip = random.randint(0, 1)

        random_chr = (chr(random_i))

        if flip:
            random_chr = random_chr.upper()

        random_string += random_chr

    # build hashcode(lastname + iid + random_string) & build a url
    hash_string = hashlib.md5(str(last_name.lower() + str(iid) + random_string).encode()).hexdigest()

    url = f"{host}/besitzer/?hc={hash_string}&rs={random_string}"

    # Testing
    print(url)

    # make a scannable QRCode
    code = qr.QRCode(version=1, box_size=10, border=2)
    code.add_data(url)
    code.make(fit=True)
    img = code.make_image()

    img.save("qrcode.png")


