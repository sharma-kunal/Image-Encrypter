from django.shortcuts import render

from .encrypt import Encrypt
from .decrypt import Decrypt
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import shutil
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
enc = ""


# Home Page
def homePageView(request):
    # return HttpResponse('Hello, World!')
    return render(request, 'homepage.html')


# Encrypt Page
def encrypt(request):
    if request.method == 'POST':
        files = request.FILES.getlist('document')
        text = request.POST['text-to-encrypt']
        mail = request.POST.get('mail')
        email = request.POST['email']
        password = request.POST['password']
        r_email = request.POST['r_email']
        submit = request.POST['submit']
        if files is None or text is None or mail is None:
            messages.error(request, "Some fields are missing.")
        elif mail == "True" and not (email or password or r_email):
            messages.error(request, "Please provide email and password")
        else:
            uploaded_file = []
            for f in files:
                uploaded_file.append(f)
            if len(uploaded_file) == 1:
                uploaded_file = uploaded_file[0]
                fs = FileSystemStorage()
                fs.save(uploaded_file.name, uploaded_file)
            else:
                create_dir(uploaded_file)
            Encrypt(uploaded_file, text, mail, email, password, r_email)
            if mail == "True":
                messages.success(request, "Mailed Successfully")
    return render(request, 'encrypt.html')


# Decrypt Page
def decrypt(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['decrypt-image']
        decrypted_value = Decrypt(uploaded_file).decode()
        context = {
            'decrypted_value': decrypted_value
        }
        return render(request, 'decrypt.html', context)
    else:
        return render(request, 'decrypt.html')


def create_dir(uploaded_file):
    if os.path.exists(BASE_DIR + '/media/send'):
        shutil.rmtree(BASE_DIR + '/media/send')
    else:
        os.mkdir(BASE_DIR + '/media/send')
    fs = FileSystemStorage(location=BASE_DIR + '/media/send')
    for f in uploaded_file:
        fs.save(f.name, f)