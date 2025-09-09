import requests

def get_random_cat() -> str | None:
    url = "https://api.thecatapi.com/v1/images/search"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data and "url" in data[0]:
                return data[0]["url"]
        return None
    except Exception:
        return None

if __name__ == "__main__":
    print(get_random_cat())