# Data Stuctures: Graph

After getting and caching the raw results (JSON), I built an undirected weighted graph data structure from that data. To build this graph, I maintained a Vertex class and a Graph class. Each business is represented as a vertex and is considered connected when two businesses are within the same categories or having the same rating. For example, the restaurants Beehive and Fireside Bar both lie within the ‘Cocktail Bars’ and ‘Lounges' categories so these two restaurants are considered connected. The weight between two connected vertices are defined by the distance between the two businesses. The distance will be calculated by the coordinates. A sample output will be “The Beehive is connected to Fireside Bar with a distance of 2.3638783500528353 miles.”

For my analysis, I would utilize the following algorithms:

### Graph Traversal
- breadth-first search
- depth-first search 
### Shortest Path
- Bellman Ford
- Dijkstra
