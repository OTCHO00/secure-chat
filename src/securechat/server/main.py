import asyncio

async def start_server(client_connect_cb, host=None, port=None, *, limit=65536, **kwds):

    server = await asyncio.start_server(client_connect_cb, host, port, limit=limit, **kwds)
    return server

async def handle_client(reader, writer):

    data = await reader.read(100)
    print(f"Reçu :  {data.decode()}")
    writer.close();
    await writer.wait_closed()

async def main():

    server = await start_server(handle_client, '127.0.0.1', 8888)
    
    async with server:
        print("Le serveur est démarré sur port 8888... En attente de clients.")
        await server.serve_forever() 

asyncio.run(main())