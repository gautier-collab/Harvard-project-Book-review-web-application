import requests

ISBN = # INSERT AN ISBN NUMBER HERE (valid ISBN example : 743493915 ; invalid ISBN example: 743493919)

res = requests.get(f"http://127.0.0.1:5000/api/{ISBN}")
print(res.json())
