__author__ = 'pawel'

class StateOfVertice:
    unselected = 0
    selected = 1
    selectedz = 2
    selectedx = 3
    selectedy = 4

class Vertice:
    __position = { 'x': 0, 'y': 0}
    __id = 0
    __state = StateOfVertice.unselected

    def __init__(self, x = 0, y = 0):
        self.__id = Vertice.__id
        Vertice.__id = Vertice.__id + 1
        self.__position =  { 'x': x, 'y': y }


    @staticmethod
    def on_delete():
        if Vertice.__id > 0:
            Vertice.__id = Vertice.__id - 1

    def set_id(self, id):
        self.__id = id

    def get_id(self):
        return self.__id

    def get_position(self):
        return self.__position

    def set_position(self, x, y):
        self.__position = { 'x': x, 'y': y}

    def set_state(self, state):
        self.__state = state

    def get_state(self):
        return self.__state



class Graph:
    __adjacency_matrix = []
    __vertices = []

    def __init__(self):
        return

    def add_vertice(self, vertice):
        self.__vertices.append(vertice)
        if len(self.__adjacency_matrix) > 0:
            for row in self.__adjacency_matrix:
                row.append(0)
            self.__adjacency_matrix.append([0 for x in range(len(self.__adjacency_matrix[0]))])
        else:
            self.__adjacency_matrix.append([0])
        self.print_graph()

    def delete_vertice(self, id):
        Vertice.on_delete()
        del(self.__vertices[id])
        for i in range(id, len(self.__vertices)):
            self.__vertices[i].set_id(i)
        for row in self.__adjacency_matrix:
            del(row[id])
        del(self.__adjacency_matrix[id])
        self.print_graph()

    def get_vertice(self, id):
        return self.__vertices[id]

    def add_edge(self, from_id, to_id):
        self.__adjacency_matrix[from_id][to_id] = 1
        self.print_graph()

    def delete_edge(self, from_id, to_id):
        self.__adjacency_matrix[from_id][to_id] = 0
        self.print_graph()

    def print_graph(self):
        print "graph: "
        print self.__adjacency_matrix
        for vertice in self.__vertices:
            print vertice.get_id()
            print vertice.get_position()

    def get_adjacency_matrix(self):
        return self.__adjacency_matrix

    def set_all_vertices_unselected(self):
        for vertice in self.__vertices:
            vertice.set_state(StateOfVertice.unselected)


##test
#a = Graph()

#a.add_vertice(Vertice())
#a.add_vertice(Vertice())
#a.add_vertice(Vertice())
#a.add_vertice(Vertice())
#a.add_edge(1,2)
#a.add_edge(0,2)
#a.add_edge(2,3)
#a.add_edge(3,2)
#a.print_graph()
#a.delete_vertice(2)
#a.print_graph()
