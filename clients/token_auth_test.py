import requests

def client():
    # credentials = {"username":"admin", "password":"1234567"}
    # response = requests.post("http://127.0.0.1:8000/api/rest-auth/login/", data = credentials)

    token_h = "Token b7bea4db519fcd9066dfc5f54f076b6407bb4f40"
    headers = {"Authorization": token_h}
    response = requests.get("http://127.0.0.1:8000/api/profiles/", headers=headers)


    print("Status Code: ", response.status_code)
    response_data = response.json()
    print(response_data)

if __name__ == "__main__":
    client()