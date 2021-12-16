from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path

graph = [[0,2,3,0],[0,0,0,4],[0,0,0,0],[0,0,0,0]]

graph = csr_matrix(graph)
print(graph)

dist_matrix, predecessors = shortest_path(csgraph=graph, directed=True, indices=0, return_predecessors=True)
print(dist_matrix)
print(predecessors)