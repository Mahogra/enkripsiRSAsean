
import asyncio
import websockets
import json
from encrypt import dekripsi
data = []

async def client_handler():
    uri = "ws://10.250.25.253:8765"  # Ganti dengan alamat server jika diperlukan

    async with websockets.connect(uri) as websocket:
        auth_data = {
            "name": "Sean",
            "password": "bayar10rb"
        }
        first_message = json.dumps(auth_data)
        print(f"Sending to server: {first_message}")
        await websocket.send(first_message)

        response = await websocket.recv()
        print(f"Received from server: {response}")
        data.append(response)

        if "terautentikasi" in response:
            while True:
                try:
                    message = await websocket.recv()
                    print(f"Encrypted Message from server: {message}")
                    message = dekripsi(eval(message))
                    print(f"Decrypted Message from server: {message}")
                    data.append(message)
                except websockets.exceptions.ConnectionClosed:
                    print("Connection closed by server")
                    break

        # Simpan data ke dalam file JSON setelah koneksi ditutup
        with open('client_data.json', 'w') as f:
            json.dump(data, f)

        print("Data saved to client_data.json")

asyncio.run(client_handler())
