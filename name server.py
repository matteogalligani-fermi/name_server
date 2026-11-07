import asyncio
from datetime import datetime
import json

class Server:
    def __init__(self,host,port):
        self.host = host
        self.port = port

    async def name_server(self,dati,writer):
        print("servizio name server")
        if dati["service"]=="time":
            diz={"status": "ok", "service": "time","host": "127.0.0.1", "port": 6001}
            writer.write((json.dumps(diz) + '\n').encode())
            await writer.drain()
        elif dati["service"]=="echo":
            diz={"status": "ok", "service": "echo","host": "127.0.0.1", "port": 6002}
            writer.write((json.dumps(diz) + '\n').encode())
            await writer.drain()
        else:
            print("nessun servizio")
            diz={"status":"no"}
            writer.write((json.dumps(diz) + '\n').encode())
            await writer.drain()

    async def time_server(self,writer):
        print("servizio time")
        tempo=datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        diz={"status": "ok", "time": tempo}
        writer.write((json.dumps(diz)+'\n').encode())
        await writer.drain()

    async def echo_server(self,dati,writer):
        print("servizio echo")
        testo=dati["text"]
        diz={"status": "ok", "text": testo}
        writer.write((json.dumps(diz)+'\n').encode())
        await writer.drain()

    async def gestisci_client(self,reader, writer):
        while True:
            data = await reader.readline()
            if not data:
                break
            dati=json.loads(data.decode())
            if dati["cmd"]=="lookup" and self.port==6000:
                await self.name_server(dati,writer)
            if dati["cmd"]=="time" and self.port==6001:
                await self.time_server(writer)
            if dati["cmd"]=="echo" and self.port==6002:
                await self.echo_server(dati,writer)


    async def avvio(self):
        server= await asyncio.start_server(self.gestisci_client, self.host, self.port)
        print(f"connessione {self.host}:{self.port}")
        async with server:
            await server.serve_forever()

async def main():
    name= Server("127.0.0.1", 6000)
    time = Server("127.0.0.1", 6001)
    echo = Server("127.0.0.1", 6002)
    await asyncio.gather(
        name.avvio(),
        time.avvio(),
        echo.avvio()
    )

if __name__ == '__main__':
    asyncio.run(main())