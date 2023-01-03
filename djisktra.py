import networkx as nx

# Génération aléatoire d'un graphe avec networkx
G = nx.gnm_random_graph(10, 20)

# Conversion du graphe en dictionnaire
G_dict = nx.to_dict_of_dicts(G)

# Classe pour représenter un graphe
class Graph:
  def __init__(self, graph_dict):
    self.graph_dict = graph_dict

  def printSolution(self, dist):
    print("Vertex \t Distance from Source")
    for node in dist:
      print(node, "\t\t", dist[node])

  # Algorithme de Dijkstra
  def dijkstra(self, src):
    row = len(self.graph_dict)
    col = len(self.graph_dict)

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
      for neighbor in self.graph_dict[current_node]:
        if not visited[neighbor]:
          if distance[neighbor] > distance[current_node] + self.graph_dict[current_node][neighbor]['weight']:
            distance[neighbor] = distance[current_node] + self.graph_dict[current_node][neighbor]['weight']
            parent[neighbor] = current_node
            heapq.heappush(priority_queue, [distance[neighbor], neighbor])

    self.printSolution(distance)

# Exemple d'utilisation
graph = Graph(G_dict)


print(G_dict)

# Calculer les plus courts chemins à partir de la source 0
graph.dijkstra(1)
