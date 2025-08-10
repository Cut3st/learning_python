import requests

def test_openweathermap(api_key, city="Singapore"):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key
    }

    print(f"🔍 Testing OpenWeatherMap API for city: {city}")
    try:
        response = requests.get(url, params=params)
        print("Status code:", response.status_code)

        try:
            data = response.json()
        except ValueError:
            print("❌ Response is not JSON. Raw text:")
            print(response.text)
            return

        # Error handling based on status code
        if response.status_code == 200:
            print("✅ API call successful.")
            print("Weather:", data["weather"][0]["description"])
        elif response.status_code == 401:
            print("🔒 Unauthorized: Invalid API key.")
        elif response.status_code == 404:
            print("📍 City not found or bad request.")
        elif response.status_code == 429:
            print("🚫 Rate limit exceeded.")
            print("Message:", data.get("message", "No message"))
        else:
            print(f"⚠️ Unexpected error: {response.status_code}")
            print("Message:", data.get("message", "No message"))

    except requests.exceptions.RequestException as e:
        print("❌ Network error:", e)

# Example usage
test_openweathermap("", "Singapore")
