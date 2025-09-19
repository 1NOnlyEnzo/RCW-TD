import requests

def main():
    url = "http://127.0.0.1:8000/api/chain"  
    payload = {"message": "Bonjour microservices"}

    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status() 
    except requests.exceptions.RequestException as e:
        print(f" Erreur de connexion : {e}")
        return

    # Afficher le JSON final
    print(" Réponse complète :")
    print(r.json())

if __name__ == "__main__":
    main()
