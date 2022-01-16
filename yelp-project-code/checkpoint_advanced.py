import json
import urllib3
import requests
from flask import Flask, render_template, request, url_for, flash, redirect, session
from forms import Form, AdvancedFrom

app = Flask(__name__) 
app.config['SECRET_KEY'] = '0b89e2f14c2189a2be7819d640b2075b'
api_key='SxOxKdawqFdhHAKaip1KGaHDNXkNGnFe605QrTccomdvxM2lziawBLaqtqpmk0CdiQArtufkA5ovEJnyAlk9fVkpdgpQhoW6dUGi_itrON7QgupCkyj9WiNgpFOkYXYx'


#all the backend functions:
# database call: return a list of dictionaries, each dictionary is a bunisess

def open_cache():
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 

def construct_unique_key(baseurl, params):
    param_strings = []
    connector = '/'
    for k in params.keys():
        stripedparam=params[k].replace(" ", "")
        param_strings.append(f'{k}={stripedparam}')
    param_strings.sort()
    unique_key = baseurl + connector +  connector.join(param_strings)
    return unique_key

def get_businesses(baseurl, params):
    headers = {'Authorization': 'Bearer %s' % api_key}
    #url = 'https://api.yelp.com/v3/businesses/search'
    data = []
    for offset in range(0, 100, 50):
        params02 = {
            'limit': 50, 
            'location': params['location'].replace(' ', '+'),
            'term': params['term'].replace(' ', '+'),
            'offset': offset
        }

        response = requests.get(baseurl, headers=headers, params=params02) # this is the main
        if response.status_code == 200:
            data += response.json()['businesses'] # I already convert json to python oject
        elif response.status_code == 400:
            print('400 Bad Request')
            break

    return data # so just return the python object

def make_request_with_cache(baseurl, params):
    request_key = construct_unique_key(baseurl, params)
    if request_key in CACHE_DICT.keys():
        print("cache hit!", request_key)
        return CACHE_DICT[request_key]
    else:
        print("cache miss!", request_key)
        CACHE_DICT[request_key] = get_businesses(baseurl, params)
        save_cache(CACHE_DICT)
        return CACHE_DICT[request_key]

# Caching
CACHE_FILENAME = "yelp_cache.json" # I should create a cache for final implementation
CACHE_DICT = {}
CACHE_DICT = open_cache()

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
    
    def printGraph(self, dictionary):
        keys = self.verticies.keys()
        for key in keys:
            vertex=self.getVertex(key)
            dictionary[key]=vertex.neighbors
        return dictionary

    def dfs(self, visited, vertexName):
        if vertexName not in visited:
            print (vertexName)
            visited.add(vertexName)
            for neighbour in self.getVertex(vertexName).neighbors:
                self.dfs(visited,neighbour)         
        return list(visited)[:10]   
            
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
        return visited[:10]   
            
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
                    


@app.route("/", methods=['GET', 'POST'])
def form():
    form = Form()
    return render_template('form.html', title='Form', form=form)


@app.route('/handle_form', methods=['POST'])
def handle_the_form():
    #get user input from form
    advancedForm = AdvancedFrom()
    term = request.form["keyword"]
    location = request.form["location"]
    
    #query user API with user input
    data = query(term, location)
    categories = category(data)
    graph = maincode(data, categories)
    
    #algorithms:
    all_business=graph.getVertices()


    return render_template('response.html', 
        term=term,
        location=location,
        all_business=all_business,
        data=data,
        advancedForm=advancedForm
        )

@app.route('/advanced_handle_form', methods=['POST'])
def advanced_handle_the_form():
    #get user input from form
    advancedForm = AdvancedFrom()
    term = request.form["keyword"]
    location = request.form["location"]
    restaurant01 = request.form["restaurant01"]
    restaurant02 = request.form["restaurant02"]
    restaurant03 = request.form["restaurant03"]
    traversal= request.form["traversal"]
    shortest_path = request.form["shortest_path"]
    
    #query user API with user input
    data = query(term, location)
    categories = category(data)
    graph = maincode(data, categories)
    
    #algorithms:
    if traversal =='BFS':
        visited2 = []
        queue = []  
        traversal_list = graph.bfs(visited2, restaurant01)   
    else:
        visited = set() 
        traversal_list = graph.dfs(visited,restaurant01)

    if shortest_path =='Bellman Ford':
        shortest_path_list = graph.bellmanFord(restaurant02, restaurant03)
    else:
        shortest_path_list = graph.dijkstra(restaurant02, restaurant03)


    return render_template('advanced_response.html', 
        term=term,
        location=location,
        restaurant01=restaurant01,
        restaurant02=restaurant02,
        restaurant03=restaurant03,
        traversal=traversal,
        shortest_path=shortest_path,
        traversal_list=traversal_list,
        shortest_path_list=shortest_path_list,
        data=data,
        advancedForm=advancedForm
        )


if __name__ == '__main__':
    app.run(debug=True)