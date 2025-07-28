#How to connect to an API using python
# Import the requests library to make HTTP requests
import requests

#  This is the base URL for the PokeAPI, an open API that provides Pokémon data in JSON format
base_url = "https://pokeapi.co/api/v2"

def get_pokemon_info(name):
    # This creates the full endpoint URL by appending the Pokémon's name to the API path
    # Example: https://pokeapi.co/api/v2/pokemon/charizard
    url = f"{base_url}/pokemon/{name}"

    # This line sends an HTTP GET request to the constructed URL
    # GET is used to retrieve data from a server
    response = requests.get(url)
    
    # If the server responds with a 200 OK status code, it means the request was successful
    if response.status_code == 200:
        # The response body (in JSON format) is parsed into a Python dictionary
        # This JSON contains all the data about the requested Pokémon
        pokemon_data = response.json()
        return pokemon_data
    else:
        # If the status code is not 200, it means something went wrong (e.g., not found or server error)
        # The specific status code is printed for debugging
        print(f"Failed to retrieve data {response.status_code}")


pokemon_name = "charizard"
pokemon_info = get_pokemon_info(pokemon_name)

if pokemon_info:
    # Accessing fields from the parsed JSON response
    print(f"Name: {pokemon_info['name']}")
    print(f"ID: {pokemon_info['id']}")
    print(f"Height: {pokemon_info['height']}")
    print(f"Weight: {pokemon_info['weight']}")
