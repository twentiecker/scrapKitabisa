import requests

url = "https://api.publicapis.org/random?category=jobs"

# headers = {
# }

response = requests.request("GET", url)

print(response.text)