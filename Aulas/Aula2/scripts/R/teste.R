library(igraph)

G <- graph.atlas(1050)
plot(G, layout = layout_with_kk(G), edge.lty= 4, node.color='orange')
