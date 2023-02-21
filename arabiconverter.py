import unicodedata
import idna


url = input("Enter website : ")

try:
    url_normalized = unicodedata.normalize('NFC',url)
    print(url_normalized)
    url_alabel = idna.encode(url_normalized).decode("ascii")
    print("The ASCII translation of it: " + url_alabel)

    # Here we might can use the url_alabel in a shortening the link.  And then we assign the shortened into a variable ,
    # Then we decode the shortened variable.


    url_ulabel = idna.decode(url_alabel)
    print("ُThe URL is : " + url_ulabel)
except idna.IDNAError as e:
    print(f"URL '{url} is invalid: {e}")
except Exception as e:
    print(f"Error: {e}")
