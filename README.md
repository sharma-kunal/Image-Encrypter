# Image-Encrypter 

This is a simple Image-Encrypter tool which will help you in hiding some text inside the image and send it to someone via gmail.

Image-Encrypter has been made in python using Django (a web-development python framework).

You can encrypt single file as well as multiple files. 

* For a single file the encrypted image will be sent as `.png` file. 
* For mulitple files, all the files would first be encrypted and then zipped before sending mail.


# Install and Run

Run the command 

```
pip3 install requirements.txt
```

to install all the required dependencies.


Then run the command 

```
python3 manage.py runserver
```

and go to your favourite browser and type 

```
127.0.0.1:8000
```

Congratulations your server is up and running 

---
**NOTE**

Please make sure you have Enabled `Allow Less Secure Apps` functionality in your gmail settings (from which you are willing to send mail).
If not you can do so by following the steps given on [Allow Less Sucure Apps](https://www.dev2qa.com/how-do-i-enable-less-secure-apps-on-gmail/)

---
