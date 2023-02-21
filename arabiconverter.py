import unicodedata
import idna

url = input("Enter website : ")

try:
    url_normalized = unicodedata.normalize('NFC',url)
    print(url_normalized)
    url_alabel = idna.encode(url_normalized).decode("ascii")
    print(url_alabel)
    url_ulabel = idna.decode(url_alabel)
    print(url_ulabel)
except idna.IDNAError as e:
    print(f"URL '{url} is invalid: {e}")
except Exception as e:
    print(f"Error: {e}")
