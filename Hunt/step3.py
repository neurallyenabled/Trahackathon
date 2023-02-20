import requests

data = {
  "team-id": "فريق-٧",
  "secret-message": "9f51821de106ca6e998b6f340feec57d"
}

r = requests.post('http://xn--mgbf0g.xn--mgbcpq6gpa1a:9000/decipher/', json=data)

print(r.text, r.headers)
