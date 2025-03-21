
import asyncio
import websockets
import json
from encrypt import enkripsi
# Dictionary to store authentication status for each client
authenticated_clients = {}

async def server_handler(websocket, path):
    print("Client connected")
   
    try:
        client_id = str(websocket.remote_address)

        # Loop untuk menerima pesan dari client
        async for message in websocket:
            if client_id not in authenticated_clients:
                # Parsing pesan autentikasi dalam bentuk JSON
                try:
                    auth_data = json.loads(message)
                except json.JSONDecodeError:
                    print(f"Autentikasi gagal dari {client_id}. Pesan bukan JSON.")
                    await websocket.close()
                    return

                # Memeriksa autentikasi
                if auth_data.get("name") == "Sean" and auth_data.get("password") == "bayar10rb":
                    authenticated_clients[client_id] = True
                    print(f"Koneksi berhasil dari {client_id}")
                    response = "Selamat datang! Anda terautentikasi."
                    await websocket.send(response)
                    break
                else:
                    print(f"Autentikasi gagal dari {client_id}. Data: {auth_data}")
                    await websocket.close()
                    return
        
        # Setelah autentikasi, server mengirim pesan secara berkala
        while client_id in authenticated_clients:
            try:
                # Ganti pesan ini dengan data yang diinginkan atau pesan acak
                #server_message = f"Pesan dari server untuk {client_id}."
                server_message = input("Masukkan pesan disini: ")
                if server_message.lower() == 'exit':
                    break
                server_message = str(enkripsi(server_message))
                print(f"Sending to {client_id}: {server_message}")
                await websocket.send(server_message)

                # Tunggu sejenak sebelum mengirim pesan berikutnya
                await asyncio.sleep(2)
            except websockets.exceptions.ConnectionClosed:
                print(f"Client {client_id} disconnected.")
                break

    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection Closed: {e}")
    finally:
        # Hapus client dari authenticated_clients saat client terputus
        authenticated_clients.pop(client_id, None)
        print(f"Client {client_id} disconnected")

async def start_server():
    server = await websockets.serve(server_handler, "0.0.0.0", 8765)
    print("WebSocket server is running...")
    await server.wait_closed()

asyncio.run(start_server())
