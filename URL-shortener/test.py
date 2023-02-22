# import random
# import string

# # letter = ["أ","ب",]""
# letters = "أبتثجحخدذرزسشصضطظعغفقكلمنهوي٠١٢٣٤٥٦٧٨٩"
# rand_letters = random.choices(letters, k=3)
# # while True:
# #     rand_letters = random.choices(letters, k=3)
# #     rand_letters = "".join(rand_letters)
# #     short_url = Urls.query.filter_by(short=rand_letters).first()
# #     if not short_url:
# #         return rand_letters

# print(rand_letters)

import unicodedata
url_received = "https://هتا.البحرين/القتلقتل"
url_received = url_received.split("https://")[1].split("/")
normalized_input = unicodedata.normalize('NFC',url_received[0])
url_received = "https://"+normalized_input+"/"+url_received[1]
print(url_received)