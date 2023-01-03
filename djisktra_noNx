import random
import heapq

# Classe pour représenter un graphe
class Graph:
  def __init__(self, vertices):
    self.V = vertices
    self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]

  def printSolution(self, dist):
    print("Vertex \t Distance from Source")
    for node in range(self.V):
      print(node, "\t\t", dist[node])

  # Algorithme de Dijkstra
  def dijkstra(self, src):
    row = len(self.graph)
    col = len(self.graph[0])

    # Tableau de distances
    distance = [float("Inf")] * row

    # Tableau de parents
    parent = [-1] * row

    # Marqueur pour les noeuds visités
    visited = [False] * row

    # Initialiser la distance de la source à 0
    distance[src] = 0
    parent[src] = -1

    # Créer une file de priorité
    priority_queue = []

    # Insérer la source dans la file de priorité
    heapq.heappush(priority_queue, [0, src])

    while priority_queue:
      # Récupérer le noeud le plus proche
      current_node = heapq.heappop(priority_queue)[1]
      visited[current_node] = True

      # Mettre à jour les distances des voisins du noeud courant
      for i in range(col):
        if self.graph[current_node][i] > 0 and not visited[i]:
          if distance[i] > distance[current_node] + self.graph[current_node][i]:
            distance[i] = distance[current_node] + self.graph[current_node][i]
            parent[i] = current_node
            heapq.heappush(priority_queue, [distance[i], i])

    self.printSolution(distance)

# Génération aléatoire d'un graphe
def random_graph(vertices, edges):
  graph = Graph(vertices)

  for i in range(edges):
    src = random.randint(0, vertices-1)
    dest = random.randint(0, vertices-1)
    weight = random.randint(1, 10)
    graph.graph[src][dest] = weight
    graph.graph[dest][src] = weight

  return graph

# Exemple d'utilisation
vertices = 6
edges = 9

graph = random_graph(vertices, edges)

# Calculer les plus courts chemins à partir de la source 0
graph.dijkstra(0)
