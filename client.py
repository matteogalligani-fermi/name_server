import asyncio
import json

async def richiesta(host,porta,diz):
    reader, writer = await asyncio.open_connection(host, porta)
    print("connessione riuscita")
    payload=json.dumps(diz)+'\n'
    writer.write(payload.encode())
    print("dati inviati")
    await writer.drain()

    data=await reader.readline()
    ris=json.loads(data.decode())
    writer.close()
    await writer.wait_closed()
    return ris

async def main():
    while True:
        print("inserisci un servizio tra echo o time")
        ser=await asyncio.to_thread(input)
        porta=6000
        cmd="lookup"
        name= await richiesta("127.0.0.1",porta,{"cmd":cmd,"service":ser})
        print(name)
        if name["status"]=="no":
            print("servizio non trovato")
        else:
            cmd=name["service"]
            porta=name["port"]
            if cmd=="time":
                request= await richiesta("127.0.0.1",porta,{"cmd":cmd})
            if cmd=="echo":
                print("inserisci messaggio")
                mes=await asyncio.to_thread(input)
                request = await richiesta("127.0.0.1", porta, {"cmd": cmd, "text": mes})
            print(request)


if __name__ == "__main__":
    asyncio.run(main())