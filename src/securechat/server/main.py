import asyncio

clients = set()

async def start_server(client_connect_cb, host=None, port=None, *, limit=65536, **kwds):

    server = await asyncio.start_server(client_connect_cb, host, port, limit=limit, **kwds)
    return server

async def handle_client(reader, writer):

    clients.add(writer)
    id_client = writer.get_extra_info("peername")

    try:

        print(f"Client {id_client} est bien connecté")

        while True:
            data = await reader.readline()
            if not data:
                break
            if not data.strip():
                continue
            await broadcast(data, writer)

    finally:

        print(f"Client {id_client} s’est bien déconnecté")
        clients.discard(writer)
        writer.close()

async def broadcast(data, writer):

    n_clients = clients.copy()

    for c in n_clients:

        try:
            if c != writer:
                    
                c.write(data)
                await c.drain()

        except ConnectionError:
            clients.discard(c) 
            c.close()

async def main():

    server = await start_server(handle_client, '127.0.0.1', 8888)
    
    async with server:
        print("Le serveur est démarré sur port 8888... En attente de clients.")
        await server.serve_forever() 

asyncio.run(main())