library(igraph)

cac_40_v1_edges <- read_csv("~/Desktop/ARA/nets/cac 40 v1 - edges.csv")
G1 <- graph_from_data_frame(cac_40_v1_edges, directed = FALSE)
bipartite_mapping(G1)

from <- unique(cac_40_v1_edges$from)
to <- unique(cac_40_v1_edges$to)
typ <- unlist(bipartite_mapping(G1)['type'])
names(typ)<- c(from,to)
G2 <- make_bipartite_graph(typ,rbind(cac_40_v1_edges$from,cac_40_v1_edges$to))
is_bipartite(G2)
proj <- bipartite_projection(G2)

print(proj[[1]])
print(proj[[2]])
