import requests

print(requests.__version__)
print(requests.get("http://www.google.com"))
print(requests.get("https://raw.githubusercontent.com/amandanguyeen/cmput-404/main/lab-1/lab1.py").text)
