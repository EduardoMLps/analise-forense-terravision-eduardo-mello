import time
from pathlib import Path

import requests

urlBase = "https://earthengine.googleapis.com/v1/projects/earthengine-legacy/maps/ade39642daac89ccf4ccc0086ea23f5b-0c19e1f3d8e60874abd07bdc389c4938/tiles/{z}/{x}/{y}"

PASTA = Path("src/websearch/tiles")
PASTA.mkdir(exist_ok=True)

sessao = requests.Session()
sessao.headers["User-Agent"] = "CroplandsResearch/1.0"

zoom = 1
n = 2 ** zoom

for y in range(n):
    for x in range(n):
        novoUrl = urlBase.format(z=zoom, x=x, y=y)
        print(novoUrl)

        destino = PASTA / f"{zoom}_{x}_{y}.png"

        if destino.exists():
            continue

        try:
            resposta = sessao.get(novoUrl, timeout=30)

            if resposta.status_code == 200:
                if resposta.headers.get("Content-Type", "").startswith("image/"):
                    destino.write_bytes(resposta.content)
                    print("Salvo:", destino)
                else:
                    print("Resposta não é imagem:", novoUrl)
            elif resposta.status_code == 404:
                print("Tile inexistente:", x, y)
            else:
                print("HTTP", resposta.status_code, novoUrl)

        except requests.RequestException as erro:
            print("Falha:", erro)

        time.sleep(0.2)