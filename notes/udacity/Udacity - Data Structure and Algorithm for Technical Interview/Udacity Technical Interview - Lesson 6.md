> Thu, 3 May 2018 at 0:35:25 MYT

### Lesson 6: Graphs

1. graphs: data structure designed to show relationship between objects. graph also called as "network"
2. graph doesn't really have a root node (like trees do) since it can possibly contain a cycle connection
3. sample of cycle in graph: `A, B, C, D, E, F, A`
4. nodes can be thought as part of graph that store data and edges are the connection between nodes. however, edges can also store data too.
5. edges usually contain data about the strength of the connection
6. similar to trees, graph also has "node" or "vertex". in fact, a tree is just a specific type of graph
7. **directed graph**: graph in which the edges has an additional property to indicates its direction (ie. one-way direction)
8. in a sentence, you may think of a noun as node in graph, and a verb as edges. for example: "from san fransisco, travel to tokyo":
    - san fransisco (noun): node1
    - travel (verb): edge
    - tokyo (node): node2
9. **undirected-graph**: graph without the sense of direction in its edges. ie, graph of people relationship
10. **DAG**: Directed Acyclic Graph; a directed graph with no cycles
11. **Connectivity** == **Graph Theory**
12. **connectivity**: the minimum number of elements that need to be removed for the graph to become disconnected
13. **disconnected graphs**: there is some vertex or group of vertices that have no connection with the rest of the graph.
14. **weakly connected graph**: A directed graph is weakly connected when only replacing all of the directed edges with undirected edges can cause it to be connected. Imagine that your graph has several vertices with one outbound edge, meaning an edge that points from it to some other vertex in the graph. There's no way to reach all of those vertices from any other vertex in the graph, but if those edges were changed to be undirected all vertices would be easily accessible.
15. **connected graph**: there's some path between one vertex and every other vertex
16. **strongly connected**: strongly connected directed graphs must have a path from every node and every other node. So, there must be a path from A to B AND B to A.
17. **edge list**: list of edges (2d list), ie.

    ```py
    [[0,1], [1,2]
     [1,3], [2,3]]
    ```
19. **adjacency list**: a way to represent adjacent graph. the 2d array will contains list of edges in which the index is adjacent to the id of the vertex

    ```py
    [[1], [0,2,3]
     [1,3], [1,2]]
     
    # - edge at index `0` is `[1]`, 
    #   which means that the vertex with id `0` is connected to vertex with id `1`.
    # - at index `1`, we have `[0,2,3]`, 
    #   which means that the vertext with id `1` is connected to vertex 0, 2, and 3
    # - same interpretation is applied to edges at index 2 (`[1,3]`) and 3 (`[1,2]`)
    ```
20. **adjacency matrix**: another way to represent graph using list (2d array). node IDs are mapped to array indices. sample of adjacency matrix:
    
    ```py
         0 1 2 3
    0  [[0,1,0,0]
    1   [1,0,1,1]
    2   [0,1,0,1]
    3   [0,1,1,0]]
    ``` 

> matrix is also known as rectangular array (see, it looks like rectangular!)
