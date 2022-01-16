class Vertex:
    def __init__(self, name, latitude, longitude, rating): # a <vertex object> has id and neighbors
        self.name=name
        self.latitude=latitude
        self.longitude=longitude
        self.rating=rating
        self.neighbors={}    #initialize as an empty dictionary

    def addNeighbor(self, nbr, weight): #nbr is a vertex
        self.neighbors[nbr.name]=weight
    
    def getName(self):
        return self.name
  
    def getWeight(self, nbr):
        return self.neighbors[nbr.name]

    #one hop
    def getNeighbors(self):
        return self.neighbors.keys()

class Graph:
    def __init__(self):
        self.verticies = {} #vertices is a dictionary

    def addVertex(self, vertex):
        self.verticies[vertex.name] = vertex 

    def getVertex(self, name):
        try:
            return self.verticies[name]
        except KeyError:
            return None
    
    def getDistance(self, from_vertex, to_vertex): #this is a vertex
        import geopy.distance
        coords_1 = (from_vertex.latitude, from_vertex.longitude)
        coords_2 = (to_vertex.latitude, to_vertex.longitude)
        return geopy.distance.distance(coords_1, coords_2).miles

    def addEdge(self, from_vertex, to_vertex, distance=0): #this is a vertex
        from_vertex.addNeighbor(to_vertex, distance)
        #directed, one-way

    def getVertices(self):
        keys=[]
        for key in self.verticies:
            keys.append(key)
        return keys

    def dfs(self, visited, vertexName):
        if vertexName not in visited:
            print (vertexName)
            visited.add(vertexName)
            for neighbour in self.getVertex(vertexName).neighbors:
                self.dfs(visited,neighbour)         
        return visited     
            
    def bfs(self,visited, vertexName):
        queue=[]
        queue.append(vertexName)
        visited.append(vertexName)
        while queue:
            s=queue.pop(0)
            print(s)
            for neighbour in self.getVertex(s).neighbors:
                if neighbour not in visited:
                    queue.append(neighbour)
                    visited.append(neighbour)   
        return visited   
            
    def bellmanFord(self, s, t): # graph, source, target
        distance={v:float('inf') for v in self.getVertices()} #{'vertex name': inf}
        distance[s]=0

        paths={v:[] for v in self.getVertices()}
        paths[s]=[s]

        for i in range(len(self.getVertices())-1): # n-1 times iteration
            for u in self.getVertices(): # u: vertex name, v: neighbor name
                vertex= self.getVertex(u)
                for v in vertex.getNeighbors():
                    if distance[u]+vertex.getWeight(self.getVertex(v))<distance[v]:
                        distance[v]=distance[u]+vertex.getWeight(self.getVertex(v))
                        paths[v]=paths[u]+[v]

        for u in self.getVertices():
            vertex= self.getVertex(u)
            for v in vertex.getNeighbors():
                if distance[u]+vertex.getWeight(self.getVertex(v))<distance[v]:
                    return('Graph has a negative-weight cycle')
        
        return paths[t]
    

    def dijkstra(self,s,t): #s: source node name
        import heapq
        visited = set()
        paths={v:[] for v in self.getVertices()}
        paths[s]=[s]
        distance={v:float('inf') for v in self.getVertices()} #{'vertex name': inf}
        distance[s]=0
        pq=[]
        heapq.heappush(pq, s)
        while pq:
            min_node=heapq.heappop(pq) # min_node name
            visited.add(min_node) # min_node name
            vertex= self.getVertex(min_node) # min_node object 
            for v in vertex.getNeighbors(): # v: neighbor name
                if distance[min_node]+ vertex.getWeight(self.getVertex(v))<distance[v]:
                    distance[v]=distance[min_node]+vertex.getWeight(self.getVertex(v))
                    heapq.heappush(pq,v)
                    paths[v]=paths[min_node]+[v]
                     
        return paths[t]



def query(term, location):
    # Modify this part for interative display
    term=term
    location=location

    # base url and parameters
    baseurl= 'https://api.yelp.com/v3/businesses/search'
    params = {'term': term,
            'location': location
            }
    
    data = make_request_with_cache(baseurl, params)
    return data #list of dictionaries

def category(data):
    categories={}
    for business in data:
        cat_1=business['categories'][0]['title']
        if len(business['categories'])>1:
            cat_2=business['categories'][1]['title']
        categories[business['name']]=[cat_1,cat_2]
    return categories

def maincode(data, categories):    
    #create vertices
    vertices=[]
    for business in data:
        vertex = Vertex(business['name'], business['coordinates']['latitude'], business['coordinates']['longitude'], business['rating'] )
        vertices.append(vertex)
    
    #create graph
    graph=Graph()
    ## add vertex
    for vertex in vertices:
        graph.addVertex(vertex)
    ## add edge
    for vertex1 in vertices:
        for vertex2 in vertices:
            if vertex1.name != vertex2.name:
                if (set(categories[vertex1.name])== set(categories[vertex2.name])) or (vertex1.rating==vertex2.rating):
                    distance= graph.getDistance(vertex1,vertex2)
                    graph.addEdge(vertex1, vertex2, distance)
    return graph