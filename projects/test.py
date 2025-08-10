import requests

def test_rate_limit():
    url = "https://api.tomorrow.io/v4/weather/realtime"
    params = {
        "location": "Singapore",
        "apikey": "DjEy6FuDa2mnGkvG1oSjSgZf9Z64ZtY8"
    }

    print("Sending request to Tomorrow.io...")
    try:
        response = requests.get(url, params=params)
        print("Status code:", response.status_code)

        try:
            data = response.json()
            print("Response JSON:", data)

            if response.status_code == 429:
                print("🚫 Rate limit exceeded!")
                print("Message:", data.get("message", "No message"))
            elif response.status_code == 200:
                print("✅ API call successful. You're not rate-limited.")
            else:
                print("⚠️ Unexpected status code:", response.status_code)
        except Exception as e:
            print("❌ Failed to parse JSON:", e)
            print("Raw response:", response.text)

    except requests.exceptions.RequestException as e:
        print("❌ Network error:", e)

test_rate_limit()
