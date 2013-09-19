__author__ = 'pawel'

import copy

class StateOfVerticeSelection:
    unselected = 0
    selected = 1
    
class StateOfSetSelection:
    unselected = 0
    selectedz = 1
    selectedx = 2
    selectedy = 3

class Vertice:
    __position = { 'x': 0, 'y': 0}
    __id = 0
    __selection_state = StateOfVerticeSelection.unselected
    __selected_set_state = StateOfSetSelection.unselected

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

    def set_selection_state(self, state):
        self.__selection_state = state

    def get_selection_state(self):
        return self.__selection_state

    def set_selected_set_state(self, state):
        self.__selected_set_state = state

    def get_selected_set_state(self):
        return self.__selected_set_state



class Graph:
    __adjacency_matrix = []
    __vertices = []
    __x_set = []
    __y_set = []
    __z_set = []

    def __init__(self):
        return

    def reset_graph(self):
        while len(self.__vertices) > 0:
            self.delete_vertice(0)
        del self.__adjacency_matrix[:]
        self.reset_all_sets()
        self.print_graph()


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
        #self.remove_vertice_from_all_sets(id)
        del(self.__vertices[id])
        for i in range(id, len(self.__vertices)):
            self.__vertices[i].set_id(i)
        for row in self.__adjacency_matrix:
            del(row[id])
        del(self.__adjacency_matrix[id])
        self.reset_all_sets()
        self.print_graph()

    def get_vertice(self, id):
        return self.__vertices[id]


    def add_edge(self, from_id, to_id):
        matrix = copy.deepcopy(self.__adjacency_matrix)
        matrix[from_id][to_id] = 1
        if self.is_acyclic_graph(matrix):
            self.__adjacency_matrix[from_id][to_id] = 1
            self.print_graph()
            return True
        else:
            return False

    def delete_edge(self, from_id, to_id):
        self.__adjacency_matrix[from_id][to_id] = 0
        self.print_graph()

    def reset_all_sets(self):
        del self.__x_set[:]
        del self.__y_set[:]
        del self.__z_set[:]
        for vertice in self.__vertices:
            if vertice.get_selected_set_state() == StateOfSetSelection.selectedx:
                self.add_vertice_to_x_set(vertice.get_id())
            elif vertice.get_selected_set_state() == StateOfSetSelection.selectedy:
                self.add_vertice_to_y_set(vertice.get_id())
            elif vertice.get_selected_set_state() == StateOfSetSelection.selectedz:
                self.add_vertice_to_z_set(vertice.get_id())

    def print_graph(self):
        print "graph: "
        print self.__adjacency_matrix
        print [x.get_id() for x in self.__vertices ]
        print "set x: " + str(self.__x_set)
        print "set y: " + str(self.__y_set)
        print "set z: " + str(self.__z_set)
        #for vertice in self.__vertices:
        #    print vertice.get_id()
            #print vertice.get_position()

    def get_adjacency_matrix(self):
        return self.__adjacency_matrix

    def set_all_vertices_unselected(self):
        for vertice in self.__vertices:
            vertice.set_selection_state(StateOfVerticeSelection.unselected)

    def add_vertice_to_z_set(self, id):
        self.remove_vertice_from_all_sets(id)
        self.__z_set.append(id)
        self.print_graph()

    def remove_vertice_from_z_set(self, id):
        try:
            self.__z_set.remove(id)
            self.print_graph()
        except:
            print "id is not in list"

    def add_vertice_to_x_set(self, id):
        self.remove_vertice_from_all_sets(id)
        self.__x_set.append(id)
        self.print_graph()

    def remove_vertice_from_x_set(self, id):
        try:
            self.__x_set.remove(id)
            self.print_graph()
        except:
            print "id is not in list"

    def add_vertice_to_y_set(self, id):
        self.remove_vertice_from_all_sets(id)
        self.__y_set.append(id)
        self.print_graph()

    def remove_vertice_from_y_set(self, id):
        try:
            self.__y_set.remove(id)
            self.print_graph()
        except:
            print "id is not in list"

    def remove_vertice_from_all_sets(self, id):
        try:
            self.__x_set.remove(id)
        except:
            print 'wrong id'
        try:
            self.__y_set.remove(id)
        except:
            print 'wrong id'

        try:
            self.__z_set.remove(id)
        except:
            print 'wrong id'
        self.print_graph()

    def validate_sets(self):
        if len(self.__x_set) == 0 or len(self.__y_set) == 0:
            return False
        else:
            return True

    def check_d_separation(self):
        for x in self.__x_set:
            for y in self.__y_set:
                if self.is_d_separated(x,y) == False:
                    print "X is not d-separated Y"
                    return False

        print "X is d-separated Y"
        return True

    def is_d_separated(self, x, y):
        num_of_vertices = len(self.__vertices)
        prev_blocked = [0 for v_prev in range(num_of_vertices)]
        next_blocked = [0 for v_next in range(num_of_vertices)]
        stack = []
        x_prev = (x, 1)
        x_next = (x, -1)
        stack.append(x_prev)
        stack.append(x_next)
        next_blocked[x] = 1
        prev_blocked[x] = 1

        while len(stack) > 0:
            current = stack.pop()
            v = current[0]
            subscript = current[1]
            if subscript < 0:
                for i in range(num_of_vertices):
                    if self.__adjacency_matrix[i][v] == 1:
                        if (next_blocked[i] == 0) and (self.__z_set.count(i) == 0):
                            next_blocked[i] = 1;
                            vertice_next = (i, -1);
                            stack.append(vertice_next)

                for j in range(num_of_vertices):
                    if self.__adjacency_matrix[v][j] == 1:
                        if not prev_blocked[j]:
                            prev_blocked[j] = 1
                            vertice_prev = (j, 1)
                            stack.append(vertice_prev)
                    prev_blocked[v] = 1
            else:
                if self.__z_set.count(v) > 0:
                    for i in range(num_of_vertices):
                        if self.__adjacency_matrix[i][v] == 1:
                            if self.__z_set.count(i) == 0 and next_blocked[i] == 0:
                                next_blocked[i] = 1
                                vertice_next = (i, -1)
                                stack.append(vertice_next)
                else:
                    for j in range(num_of_vertices):
                        if self.__adjacency_matrix[v][j] == 1:
                            if prev_blocked[j] == 0:
                                prev_blocked[j] = 1
                                prev_vertice = (j, 1)
                                stack.append(prev_vertice)
        if prev_blocked[y] or next_blocked[y]:
            return False
        else:
            return True


    #znajdz nieodwidzony wierzcholek posiadajacy jedynie krawedzie wychodzace
    def __find_start_vertice(self, visited, matrix):
        for col_id in range(len(matrix)):
            if visited[col_id] == 0:
                is_ok = True
                for row in matrix:
                    if row[col_id] == 1:
                        is_ok = False
                        break
                if is_ok:
                    return col_id
        return -1

    def __find_cycle(self, node, visited, stack, matrix):
        visited[node] = 1
        stack.append(node)
        for vertice_id in range(len(matrix)):
            if matrix[node][vertice_id] == 1:
                if stack.count(vertice_id) > 0:
                    return True
                elif visited[vertice_id] == 0:
                    result = self.__find_cycle(vertice_id, visited, stack, matrix)
                    stack.pop()
                    if result:
                        return True
        return False

    def is_acyclic_graph(self, matrix):
        visited = [0 for x in matrix]

        while visited.count(0) > 0:
            stack = []
            start_vertice = self.__find_start_vertice(visited, matrix)
            if start_vertice < 0:
                return False
            if self.__find_cycle(start_vertice, visited, stack, matrix):
                return False
        return True




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
