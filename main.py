import heapq
import math

class Cidade:
    def _init_(self, nome, endereco, latitude, longitude):
        self.nome = nome
        self.endereco = endereco
        self.latitude = latitude
        self.longitude = longitude
        self.rotas = []

    def _repr_(self):
        return self.nome

class Grafo:
    def _init_(self):
        self.cidades = {}

    def adicionar_cidade(self, cidade):
        self.cidades[cidade.nome] = cidade

    def adicionar_rota(self, cidade1, cidade2, distancia):
        if cidade1.nome not in self.cidades or cidade2.nome not in self.cidades:
            raise ValueError("Cidade não encontrada")

        cidade1.rotas.append((cidade2, distancia))
        cidade2.rotas.append((cidade1, distancia))

def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distancia = R * c
    return distancia

def dijkstra(grafo, inicio, destino, custo_por_km, velocidade_media):
    heap = [(0, inicio, [])]
    visitados = set()

    while heap:
        (custo, atual, caminho) = heapq.heappop(heap)

        if atual in visitados:
            continue

        visitados.add(atual)

        if atual == destino:
            return custo, caminho

        for vizinho, distancia in grafo.cidades[atual.nome].rotas:
            if vizinho not in visitados:
                tempo_viagem = distancia / velocidade_media
                dias_viagem = math.ceil(tempo_viagem / 24)
                custo_viagem = custo + distancia * custo_por_km * dias_viagem

                nova_caminho = caminho + [(vizinho, distancia, tempo_viagem)]

                # Modificação: Garantir que o caminho siga as rotas diretamente adicionadas
                heapq.heappush(heap, (custo_viagem, vizinho, nova_caminho))

    return float('inf'), []
    
curitiba = Cidade("Curitiba", "EnderecoCuritiba", -25.4295963, -49.2712724)
londrina = Cidade("Londrina", "EnderecoLondrina", -23.3105, -51.1622)
foz_do_iguacu = Cidade("Foz do Iguaçu", "EnderecoFoz", -25.5469, -54.5882)
uniao_da_vitoria = Cidade("União da Vitória", "EnderecoUniao", -26.2444, -51.0759)
joinville = Cidade("Joinville", "EnderecoJoinville", -26.3035, -48.8487)
chapeco = Cidade("Chapecó", "EnderecoChapeco", -27.1004, -52.6152)
porto_alegre = Cidade("Porto Alegre", "EnderecoPortoAlegre", -30.0346, -51.2177)
uruguaiana = Cidade("Uruguaiana", "EnderecoUruguaiana", -29.7641, -57.0842)
pelotas = Cidade("Pelotas", "EnderecoPelotas", -31.7614, -52.3407)

grafo = Grafo()
grafo.adicionar_cidade(curitiba)
grafo.adicionar_cidade(londrina)
grafo.adicionar_cidade(foz_do_iguacu)
grafo.adicionar_cidade(uniao_da_vitoria)
grafo.adicionar_cidade(joinville)
grafo.adicionar_cidade(chapeco)
grafo.adicionar_cidade(porto_alegre)
grafo.adicionar_cidade(uruguaiana)
grafo.adicionar_cidade(pelotas)

grafo.adicionar_rota(curitiba, londrina, 380)
grafo.adicionar_rota(curitiba, joinville, 130)
grafo.adicionar_rota(curitiba, porto_alegre, 700)
grafo.adicionar_rota(londrina, foz_do_iguacu, 640)
grafo.adicionar_rota(foz_do_iguacu, uniao_da_vitoria, 320)
grafo.adicionar_rota(joinville, chapeco, 550)
grafo.adicionar_rota(porto_alegre, uruguaiana, 630)
grafo.adicionar_rota(uruguaiana, pelotas, 410)

cidade_origem = input("Digite a cidade de origem: ")
cidade_destino = input("Digite a cidade de destino: ")

if cidade_origem not in grafo.cidades or cidade_destino not in grafo.cidades:
    print("Cidade de origem ou destino não encontrada.")
else:
    origem = grafo.cidades[cidade_origem]
    destino = grafo.cidades[cidade_destino]
    
    custo, caminho = dijkstra(grafo, origem, destino, custo_por_km=20, velocidade_media=80)

    if custo == float('inf'):
        print("Não há rota disponível.")
    else:
        print("Menor caminho:")
        for i in range(len(caminho) - 1):
            cidade_atual, distancia, tempo_viagem = caminho[i][0].nome, caminho[i][1], caminho[i][2]
            print(f"{cidade_atual} -> ", end="")
        print(destino.nome)

        distancia_percorrida = sum([caminho[i][1] for i in range(len(caminho))])

        print("Distância percorrida:", distancia_percorrida)
        print("Custo total:", custo)
        
        viagem_em_dias = distancia_percorrida / 500
        viagem_em_horas = distancia_percorrida / 80
        
        print("O caminhoneiro demorou ", viagem_em_horas, " horas para fazer essa rota, totalizando ", viagem_em_dias, " dia(s) de viagem")