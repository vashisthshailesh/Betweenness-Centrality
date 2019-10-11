#!/usr/bin/env python3

import re
import itertools

ROLLNUM_REGEX = "201[0-9]{4}"

class Graph(object):
    name = "shailesh"
    email = "shailesh18264@iiitd.ac.in"
    roll_num = "2018264"

    def __init__ (self, vertices, edges):
        """
        Initializes object for the class Graph

        Args:
            vertices: List of integers specifying vertices in graph
            edges: List of 2-tuples specifying edges in graph
        """

        self.vertices = vertices
        
        ordered_edges = list(map(lambda x: (min(x), max(x)), edges))
        
        self.edges    = ordered_edges
        
        '''self.validate()'''

        self.adjacencylist = self.make_adjacencylist()

        self.visited = [0] * (len(self.vertices)+1)



    '''def validate(self):
        """
        Validates if Graph if valid or not

        Raises:
            Exception if:
                - Name is empty or not a string
                - Email is empty or not a string
                - Roll Number is not in correct format
                - vertices contains duplicates
                - edges contain duplicates
                - any endpoint of an edge is not in vertices
        """

        if (not isinstance(self.name, str)) or self.name == "":
            raise Exception("Name can't be empty")

        if (not isinstance(self.email, str)) or self.email == "":
            raise Exception("Email can't be empty")

        if (not isinstance(self.roll_num, str)) or (not re.match(ROLLNUM_REGEX, self.roll_num)):
            raise Exception("Invalid roll number, roll number must be a string of form 201XXXX. Provided roll number: {}".format(self.roll_num))

        if not all([isinstance(node, int) for node in self.vertices]):
            raise Exception("All vertices should be integers")

        elif len(self.vertices) != len(set(self.vertices)):
            duplicate_vertices = set([node for node in self.vertices if self.vertices.count(node) > 1])

            raise Exception("Vertices contain duplicates.\nVertices: {}\nDuplicate vertices: {}".format(vertices, duplicate_vertices))

        edge_vertices = list(set(itertools.chain(*self.edges)))

        if not all([node in self.vertices for node in edge_vertices]):
            raise Exception("All endpoints of edges must belong in vertices")

        if len(self.edges) != len(set(self.edges)):
            duplicate_edges = set([edge for edge in self.edges if self.edges.count(edge) > 1])

            raise Exception("Edges contain duplicates.\nEdges: {}\nDuplicate vertices: {}".format(edges, duplicate_edges))'''

    def make_adjacencylist(self):
        '''making a list for neighbours'''
        ngh = []
        for node in self.vertices:
            pado = []
            for k in range(len(self.edges)):
                '''it checks both the sides of the edges and if one vertex is equal to node then node and that other vertices are neighbours'''
                if self.edges[k][0] == node:
                    pado.append(self.edges[k][1])
                if self.edges[k][1] == node:
                    pado.append(self.edges[k][0])
            ngh.append(pado)
        ngh.insert(0, [-1])
        return ngh


    '''def distance (self,snode):
        inf = 9999999999
        distance=[inf]*(len(self.vertices)+1)
        distance[snode] = 0
        p=[snode]
        while len(p)>0:
            for j in self.adjacencylist[p[0]]:
                if (distance [j] == inf ):
                    p.append(j)
                    distance[j]=distance[p[0]]+1
            del p[0]
        return distance'''




    def min_dist(self, start_node, end_node):
        '''
        Finds minimum distance between start_node and end_node

        Args:
            start_node: Vertex to find distance from
            end_node: Vertex to find distance to

        Returns:
            An integer denoting minimum distance between start_node
            and end_node
        '''
        '''here distance also acts as visited as whose distance will be equal to inf is not visited '''
        inf = 9999999999
        distance=[inf]*(len(self.vertices)+1)
        '''the distance at the respective index denote the distance of the respective index'''
        distance[start_node] = 0
        p=[start_node]
        while len(p)>0:
            for j in self.adjacencylist[p[0]]:
                '''checking whether the given list is visited or not'''
                if (distance [j] == inf ):
                    '''appending  all the given elements of the adjacency list in p so as to find their adjacency list  by which entire nodes will be covered'''
                    p.append(j)
                    '''its distance will be +1 of that of p[0] as as p[0] is its parent '''
                    distance[j]=distance[p[0]]+1
            '''once all the elements of the adjacency list are checked  the parent is deleted from the list'''
            del p[0]
        return distance[end_node]


    def dfs(self, start_node, end_node, path):
        '''by using dfs and recurssion  '''
        allpaths = []
        if (start_node == end_node):
            path.append(end_node)
            allpaths.append(path)
            return allpaths
        self.visited[start_node] = 1
        for negibour_node in self.adjacencylist[start_node]:
            if (self.visited[negibour_node] == 0):
                allpaths = allpaths + self.dfs(negibour_node, end_node, path + [start_node])

        self.visited[start_node] = 0
        return allpaths

    def all_shortest_paths(self,start_node, end_node):
        """
        Finds all shortest paths between start_node and end_node

        Args:
            start_node: Starting node for paths
            end_node: Destination node for paths

        Returns:
            A list of path, where each path is a list of integers.
        """

        p = self.all_paths(start_node,end_node,self.min_dist(start_node,end_node),[])
        return p

    def all_paths(self,node, destination, dist, path):
        """
        Finds all paths from node to destination with length = dist

        Args:
            node: Node to find path from
            destination: Node to reach
            dist: Allowed distance of path
            path: path already traversed

        Returns:
            List of path, where each path is list ending on destination

            Returns None if there no paths
        """
        p=self.dfs(node,destination,[])
        t=[]
        for i in p :
            if (len(i)-1==dist):
                t.append(i)
        return t

    def betweenness_centrality(self, node):
        """
        Find betweenness centrality of the given node

        Args:
            node: Node to find betweenness centrality of.

        Returns:
            Single floating point number, denoting betweenness centrality
            of the given node
        """
        z = 0
        for i in range(len(self.vertices) -1):
            for j in range (i+1,len(self.vertices)):
                tot=0
                if ( self.vertices[i] != node and self.vertices[j] != node ):
                    allsh=self.all_shortest_paths(self.vertices[i], self.vertices[j])
                    margya= len(allsh)
                    for i in allsh:
                        if (node in i):
                            tot = tot+1
                    p = tot/margya
                    z=z+p
        return z


    def top_k_betweenness_centrality(self,):
        """
        Find top k nodes based on highest equal betweenness centrality.

        
        Returns:
            List a integer, denoting top k nodes based on betweenness
            centrality.
        """
        tz=[0]
        last=[]
        for i in range(len(self.verices)):
            p=self.betweenness_centrality(self.vertices[i])
            tz.append(p)
        sd=max(tz)
        for i in range(1,len(tz)):
            if(tz[i]==sd):
                last.append(i)
        return last





if __name__ == "__main__":
    vertices = [1, 2, 3, 4, 5, 6]
    vertices.sort()
    edges    = [[1, 2], [1, 5], [2, 3], [2, 5], [3, 4], [4, 5], [4, 6]]

    graph = Graph(vertices, edges)


