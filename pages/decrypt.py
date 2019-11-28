from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


class Decrypt:
    def __init__(self, img):
        self.img = img

    def decode(self):
        if isinstance(self.img, InMemoryUploadedFile):
            image = Image.open(self.img, 'r')
        else:
            image = self.img
        data = ''
        imgdata = iter(image.getdata())

        while True:
            pixels = [value for value in imgdata.__next__()[:3] +
                      imgdata.__next__()[:3] +
                      imgdata.__next__()[:3]]
            # string of binary data
            binstr = ''

            for i in pixels[:8]:
                if i % 2 == 0:
                    binstr += '0'
                else:
                    binstr += '1'

            data += chr(int(binstr, 2))
            if pixels[-1] % 2 != 0:
                return data