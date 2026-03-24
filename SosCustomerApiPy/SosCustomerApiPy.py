import requests
import json
import time
import urllib3
from datetime import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CustomerApiDemo:
    def __init__(self):
        self.base_url = "https://api-customer.sos.sk"
        # Tvoj API kľúč z C# kódu
        self.sos_api_key = "ZGVtbzo5NUtqblNVWkdYU0c3bTdPa2RHTzlrUDhabnp2TTd1UA=="
        self.current_token = None

    def get_basic_headers(self):
        return {
            "Authorization": f"Basic {self.sos_api_key}",
            "Content-Type": "application/json"
        }

    def get_auth_headers(self):
        if not self.current_token:
            return {}
        return {
            "Authorization": f"{self.current_token['token_type']} {self.current_token['access_token']}"
        }

    async def login(self):
        username = input("Username: ")
        password = input("Password: ")
        
        payload = {"username": username, "password": password}
        url = f"{self.base_url}/auth/token/password"
        
        try:
            response = requests.post(url, headers=self.get_basic_headers(), json=payload, verify=False)
            if response.status_code == 200:
                self.current_token = response.json()
                print("Login successful!")
            else:
                print(f"Login failed. Status: {response.status_code}")
        except Exception as e:
            print(f"Error during login: {e}")

    async def check_token_expiry(self):
        if not self.current_token:
            return

        url = f"{self.base_url}/auth/tokeninfo"
        payload = {"access_token": self.current_token['access_token']}
        
        response = requests.post(url, headers=self.get_basic_headers(), json=payload, verify=False)
        if response.status_code == 200:
            info = response.json()
            expires_in = info.get('expires_in', 0)
            
            if expires_in < 300:
                print(f"\n[WARNING] Token is expiring in {expires_in} seconds.")
                choice = input("Would you like to refresh token now? (y/n): ").lower()
                if choice == 'y':
                    await self.refresh_token()

    async def check_token_status(self):
        if not self.current_token:
            print("No active session. Please login first.")
            return

        url = f"{self.base_url}/auth/tokeninfo"
        payload = {"access_token": self.current_token['access_token']}
        
        response = requests.post(url, headers=self.get_basic_headers(), json=payload, verify=False)
        if response.status_code == 200:
            info = response.json()
            exp = info['expires_in']
            minutes = exp // 60
            seconds = exp % 60

            print("--- Token Status ---")
            print("Status: ACTIVE")
            print(f"Remaining time: {exp} seconds ({minutes}m {seconds}s)")
            print(f"Expires at: {info.get('expires_at_date')}")
        else:
            print("Token is INVALID or EXPIRED.")
            self.current_token = None

    async def refresh_token(self):
        if not self.current_token:
            return

        url = f"{self.base_url}/auth/token/refresh"
        payload = {"refresh_token": self.current_token['refresh_token']}
        
        response = requests.post(url, headers=self.get_basic_headers(), json=payload, verify=False)
        if response.status_code == 200:
            self.current_token = response.json()
            print("Token refreshed successfully.")

    async def search_products(self):
        if not self.current_token:
            print("Please login first.")
            return

        query = input("Search query: ")
        url = f"{self.base_url}/products?query={query}"
        
        response = requests.get(url, headers=self.get_auth_headers(), verify=False)
        print(f"Result: {response.text}")

    async def get_product_by_id(self):
        if not self.current_token:
            print("Please login first.")
            return

        item_no = input("Item number: ")
        url = f"{self.base_url}/products/{item_no}"
        
        response = requests.get(url, headers=self.get_auth_headers(), verify=False)
        print(f"Result: {response.text}")

    async def revoke_token(self):
        if not self.current_token:
            return

        url = f"{self.base_url}/auth/revoke"
        payload = {"access_token": self.current_token['access_token']}
        
        response = requests.post(url, headers=self.get_basic_headers(), json=payload, verify=False)
        if response.status_code == 200:
            print("Token revoked.")
            self.current_token = None

    def print_help(self):        
        print("Available commands:");
        print("- login: Authenticate with username and password");
        print("- search: Search products by string");
        print("- item: Get product by item number");
        print("- status: Check token validity and remaining time");
        print("- revoke: Deactivate current access token");
        print("- quit: Revoke token and exit");
        print("- help: ");

async def main():
    demo = CustomerApiDemo()
    print("--- Customer API Demo (Python) ---")
    running = True

    while running:
        await demo.check_token_expiry()
        print("\n(login, search, item, status, revoke, quit, help)")
        cmd = input("Enter command:").lower().strip()

        if cmd == "login": await demo.login()
        elif cmd == "search": await demo.search_products()
        elif cmd == "item": await demo.get_product_by_id()
        elif cmd == "status": await demo.check_token_status()
        elif cmd == "revoke": await demo.revoke_token()
        elif cmd == "help": demo.print_help()
        elif cmd == "quit":
            await demo.revoke_token()
            running = False
            print("Exiting program...")
        else:
            print("Unknown command.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
