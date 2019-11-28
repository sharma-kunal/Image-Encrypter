from PIL import Image
import os
import smtplib

from django.http import HttpResponse

from .decrypt import Decrypt
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



class Encrypt:
    def __init__(self, image, text, mail, email=None, password=None, r_email=None):
        self.mail = mail
        self.email = email
        self.password = password
        self.r_email = r_email
        if type(image) != list:
            self.image = Image.open(image, 'r')
            self.data = text
            self.encode_enc(self.image, self.data)
            self.image.save(BASE_DIR + '/output/t1.png', 'PNG')
            print("Sending")
            print("After Encryption")
            print(self.image.size)
            print("Text Encrypted in Image:" + Decrypt(self.image).decode())
            if self.mail == "True":
                self.send_mail(self.email, self.password, 'test.png')
            print("After sending")
            print(self.image.size)
        else:
            self.image = image
            self.text = text
            self.attach_image()

            zf = open(BASE_DIR + "/hello.zip", 'rb')

            if self.mail == "True":
                msg = MIMEMultipart()
                msg['From'] = email
                msg['To'] = r_email
                msg['Subject'] = 'Subject'
                msg.attach(MIMEText("test"))

                part = MIMEBase('application', 'octet-stream')
                part.set_payload(zf.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="test.zip"')
                msg.attach(part)

                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.ehlo()
                s.starttls()
                s.ehlo()
                s.login(email, password)
                print("logged in")
                s.sendmail(email, r_email, msg.as_string())
                print("message sent")
                s.quit()

    # Convert encoding data into 8-bit binary
    # form using ASCII value of characters
    def genData(self, data):
        # list of binary codes
        # of given data
        newd = []

        for i in data:
            newd.append(format(ord(i), '08b'))
        return newd

    # Pixels are modified according to the
    # 8-bit binary data and finally returned
    def modPix(self, pix, data):
        datalist = self.genData(data)
        lendata = len(datalist)
        imdata = iter(pix)

        for i in range(lendata):

            # Extracting 3 pixels at a time
            pix = [value for value in imdata.__next__()[:3] +
                   imdata.__next__()[:3] +
                   imdata.__next__()[:3]]

            # Pixel value should be made
            # odd for 1 and even for 0
            for j in range(0, 8):
                if (datalist[i][j] == '0') and (pix[j] % 2 != 0):

                    if (pix[j] % 2 != 0):
                        pix[j] -= 1

                elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                    pix[j] -= 1

            # Eigh^th pixel of every set tells
            # whether to stop ot read further.
            # 0 means keep reading; 1 means the
            # message is over.
            if (i == lendata - 1):
                if (pix[-1] % 2 == 0):
                    pix[-1] -= 1
            else:
                if (pix[-1] % 2 != 0):
                    pix[-1] -= 1

            pix = tuple(pix)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]

    def encode_enc(self, newimg, data):
        w = newimg.size[0]
        (x, y) = (0, 0)

        for pixel in self.modPix(newimg.getdata(), data):

            # Putting modified pixels in the new image
            newimg.putpixel((x, y), pixel)
            if (x == w - 1):
                x = 0
                y += 1
            else:
                x += 1

    def send_mail(self, email, password, name):
        img = open(os.path.join(os.path.join(BASE_DIR, 'media'), 't1.png'), 'rb').read()
        msg = MIMEMultipart()
        msg['Subject'] = 'subject'
        msg['From'] = email
        msg['To'] = self.r_email

        text = MIMEText("test")
        msg.attach(text)
        image = MIMEImage(img, name=name)
        msg.attach(image)

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(email, password)
        print("logged in")
        s.sendmail(email, self.r_email, msg.as_string())
        print("message sent")
        s.quit()

    def attach_image(self):
        for i, f in enumerate(self.image):
            image = Image.open(f, 'r')
            data = self.text
            self.encode_enc(image, data)
            image.save(BASE_DIR + '/media/send/' + str(f.name), 'PNG')
        shutil.make_archive('hello', 'zip', BASE_DIR + '/media/send')

    def response(self):
        with open(BASE_DIR + '/media/t1.png') as fp:
            response = HttpResponse(fp.read(), content_type='image/jpg')
            response['Content-Disposition'] = 'attachment; filename=encrypted.jpg'
            return response
