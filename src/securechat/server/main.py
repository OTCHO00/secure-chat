import asyncio
from securechat.core.protocol import encode, parse, check_pseudo

clients = {}

async def start_server(client_connect_cb, host=None, port=None, *, limit=65536, **kwds):

    server = await asyncio.start_server(client_connect_cb, host, port, limit=limit, **kwds)
    return server

async def handle_client(reader, writer):

    pseudo = None

    try:

        writer.write("Veuillez renseignez votre pseudo (ne doit pas contenir de caractère spécial, doit faire moins de 20 caractere): \n".encode("utf-8"))
        await writer.drain()

        data_pseudo = await reader.readline()
        if not data_pseudo:
            return

        check_pseudo(data_pseudo.decode("utf-8").strip())
        pseudo = data_pseudo.decode("utf-8").strip()

        if pseudo.lower() in clients:
            writer.write("ERR pseudo déja utilisé\n".encode("utf-8"))
            writer.close()
            pseudo = None
            return 

        message_data = f"* {pseudo} a rejoint le salon\n"
        clients[pseudo.lower()] = writer

        await broadcast(message_data.encode("utf-8"), writer)
        print(f"Client {pseudo} est bien connecté")

        writer.write(f"Merci {pseudo} vôtre pseudo a bien été enregistré\n".encode("utf-8"))
        await writer.drain()

        while True:
            data = await reader.readline()

            if not data:
                break
            if not data.strip():
                continue

            try :

                await broadcast(encode(pseudo, data.decode("utf-8").strip()), writer)

            except ValueError as e:

                writer.write(f"ERR {e}".encode("utf-8"))
                await writer.drain()
                
    except ConnectionResetError:
        pass

    except ValueError as e:
        writer.write(f"ERR {e}\n".encode("utf-8"))
        await writer.drain()

    finally:

        if pseudo is not None:
            if pseudo.lower() in clients:
                del clients[pseudo.lower()]
                message_data = f"* {pseudo} a quitter le salon\n"
                await broadcast(message_data.encode("utf-8"), writer)
                print(f"Client {pseudo} est bien déconnecté")
        writer.close()
        try:
            await writer.wait_closed()
        except ConnectionError:
            pass

async def broadcast(data, writer):

    n_clients = clients.copy()

    for pseudo, w in n_clients.items():

        try:
            if w != writer:                    
                w.write(data)
                await w.drain()

        except ConnectionError:
            pass

async def main():

    server = await start_server(handle_client, '127.0.0.1', 8888)
    
    async with server:
        print("Le serveur est démarré sur port 8888... En attente de clients.")
        await server.serve_forever() 

asyncio.run(main())