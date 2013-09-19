__author__ = 'pawel rychly'

import pygtk
pygtk.require('2.0')
import gtk
import string, time
from graph import *
from verticeview import *
import pickle


class SelectionMode:
    adding_removing_vertices = 0
    adding_removing_edges = 1
    selecting_x = 2
    selecting_y = 3
    selecting_z = 4

class MenuView(gtk.VBox):
    __state = SelectionMode.adding_removing_vertices

    __state_names = {
        '0': "Dodawanie / Usuwanie wierzcholkow",
        '1': "Dodawanie / Usuwanie krawedzi",
        '2': "Zaznaczanie zbioru X",
        '3': "Zaznaczanie zbioru Y",
        '4': "Zaznaczanie zbioru warunkowego Z",
    }
    def __init__(self, graph, label, graph_view):
        self.graph = graph
        self.label = label
        self.graph_view = graph_view
        self.tooltips = gtk.Tooltips()
        super(MenuView, self).__init__(self)

        button = gtk.Button("Wyczysc graf")
        button.connect("clicked", self.reset_graph, None)
        self.pack_start(button, gtk.TRUE, gtk.TRUE, 0)
        button.show()
        self.tooltips.set_tip(button, "Wyczyszczenie grafu.")

        first_button = gtk.RadioButton(None, "Dodawanie / Usuwanie wierzcholkow")
        first_button.connect("toggled", self.radio_button_callback, SelectionMode.adding_removing_vertices)
        self.pack_start(first_button, gtk.TRUE, gtk.TRUE, 0)
        first_button.show()
        self.tooltips.set_tip(first_button, "W tym trybie, mozliwe jest dodawanie lub usuwanie wierzcholkow grafu, za pomoca odpowienio: lewego i prawego przycisku myszy.")


        button = gtk.RadioButton(first_button, "Dodawanie / Usuwanie krawedzi")
        button.connect("toggled", self.radio_button_callback, SelectionMode.adding_removing_edges)
        self.pack_start(button, gtk.TRUE, gtk.TRUE, 0)
        button.show()
        self.tooltips.set_tip(button, "W tym trybie, mozliwe jest dodawanie lub usuwanie krawedzi grafu. Aby dodac krawedz z wierzcholka A do B nalezy zaznaczyc wierzcholek A, a nastepnie wierzcholek B. Usuwanie krawedzi, realizowane jest w sposob analogiczny za pomoca prawego przycisku myszy.")


        button = gtk.RadioButton(first_button, "Zaznaczanie zbioru X \t\t\t  ")
        button.connect("toggled", self.radio_button_callback, SelectionMode.selecting_x)
        hbox = gtk.HBox(False, 30)
        pic = gtk.DrawingArea()
        pic.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(59000, 59000 , 19500))
        hbox.pack_start(button)
        hbox.pack_start(pic)

        self.pack_start(hbox, gtk.TRUE, gtk.TRUE, 0)
        button.show()
        hbox.show()
        self.tooltips.set_tip(button, "W tym trybie realizowane jest zaznaczanie wierzcholkow nalezacych do zbioru X. Zaznaczanie wierzcholkow - Lewy przycisk myszy. Odznaczanie wierzcholkow - prawy przycisk myszy.")


        button = gtk.RadioButton(first_button, "Zaznaczanie zbioru Y \t\t\t\t  ")
        button.connect("toggled", self.radio_button_callback, SelectionMode.selecting_y)

        hbox = gtk.HBox(False, 30)
        pic = gtk.DrawingArea()
        pic.set_size_request(20,20)
        pic.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(45500, 45500 , 65000))
        hbox.pack_start(button)
        hbox.pack_start(pic)

        self.pack_start(hbox, gtk.TRUE, gtk.TRUE, 0)
        button.show()
        hbox.show()
        self.tooltips.set_tip(button, "W tym trybie realizowane jest zaznaczanie wierzcholkow nalezacych do zbioru Y. Zaznaczanie wierzcholkow - Lewy przycisk myszy. Odznaczanie wierzcholkow - prawy przycisk myszy.")


        button = gtk.RadioButton(first_button, "Zaznaczanie zbioru warunkowego Z  ")
        button.connect("toggled", self.radio_button_callback, SelectionMode.selecting_z)
        hbox = gtk.HBox(False, 30)
        pic = gtk.DrawingArea()
        pic.set_size_request(20,20)
        pic.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(19500, 59000 , 19500))
        hbox.pack_start(button)
        hbox.pack_start(pic)

        self.pack_start(hbox, gtk.TRUE, gtk.TRUE, 0)
        button.show()
        hbox.show()

        self.tooltips.set_tip(button, "W tym trybie realizowane jest zaznaczanie wierzcholkow nalezacych do zbioru Z. Zaznaczanie wierzcholkow - Lewy przycisk myszy. Odznaczanie wierzcholkow - prawy przycisk myszy.")


        button = gtk.Button("Uruchom algorytm")
        button.connect("clicked", self.check_d_separation, None)
        self.pack_start(button, gtk.TRUE, gtk.TRUE, 0)
        button.show()
        self.tooltips.set_tip(button, "Uruchomienie algorytmu.")



        #self.label = gtk.Label("")
        #self.label.show()
        #self.pack_start(self.label, gtk.TRUE, gtk.TRUE, 0)


    def check_d_separation(self, widget, data=None):
        self.graph.print_graph()
        if self.graph.validate_sets():
            d_sep = self.graph.check_d_separation()
            if d_sep == True:
                self.label.set_text("Zbior wierzcholkow X jest niezalezny warunkowo od zbioru wierzcholkow Y pod warunkiem wierzcholkow ze zbioru Z.")
            else:
                self.label.set_text("Zbior wierzcholkow X jest zalezny warunkowo od zbioru wierzcholkow Y pod warunkiem wierzcholkow ze zbioru Z  ")
        else:
            self.label.set_text("Wynik nieokreslony. Zbior X lub Y jest pusty.")

    def reset_graph(self, widget, data=None):
        self.graph.reset_graph()
        self.graph_view.reset_graph_area()
        self.graph_view.layout.queue_draw()

    def get_state(self):
        return self.__state

    def radio_button_callback(self, widget, data=None):
        self.graph.set_all_vertices_unselected()
        self.label.set_text("")
        if widget.get_active():
            self.__state = data
            self.label.set_text("Aktualny tryb: " + self.__state_names[str(self.__state)])
            print self.__state
        self.graph_view.queue_draw()


class GraphViewDrawingArea(gtk.DrawingArea):
    def __init__(self, graph):
        super(GraphViewDrawingArea, self).__init__()
        #self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(65000, 65000, 65000))
        self.graph = graph
        self.edges = self.graph.get_adjacency_matrix()
        self.connect("expose-event", self.expose)


    def _draw_direction_arrow(self, cr, from_position, to_position):
        diff_x = from_position['x'] - to_position['x']
        diff_y = from_position['y'] - to_position['y']
        value = 0
        angle = 0.0
        #if diff_x <= 30.0 and diff_x >= -30.0:
        #    d_x = 0.0
        #    if (diff_x * diff_y) > 0:
        #        d_y = 15
        #    else:
        #        d_y = -15
        if diff_x == 0.0:
            diff_x = 0.000001
        tangens = float(diff_y) / float(diff_x)
        angle = math.atan(tangens)
        d_x = math.sqrt(25.0**2 / (1 + tangens**2))
        #d_x = 15.0
        d_y = tangens * d_x

        if diff_x >= 0.0: value = 1.0
        else: value = -1.0

        to_position = {
            'x': to_position['x'] + (value * d_x),
            'y': to_position['y'] + (value * d_y)
        }
        src_x = from_position['x']
        src_y = from_position['y']
        dst_x = to_position['x']
        dst_y = to_position['y']
        cr.move_to(0, 0)
        cr.save()
        cr.move_to(src_x, src_y )
        cr.line_to(dst_x, dst_y)

        arrow_x1 = (math.cos(math.pi/8 + angle) * 15)
        arrow_y1 = (math.sin(math.pi/8 + angle) * 15)
        arrow_x2 = (math.cos(-1.0 * math.pi/8 + angle) * 15)
        arrow_y2 = (math.sin(-1.0 * math.pi/8 + angle) * 15)
        cr.line_to(dst_x + value * arrow_x1, dst_y + value * arrow_y1);
        cr.move_to(dst_x, dst_y)
        cr.line_to(dst_x + value * arrow_x2, dst_y + value * arrow_y2);
        cr.move_to(dst_x, dst_y)
        cr.move_to(0, 0)
        cr.stroke_preserve()
        cr.restore()

    def expose(self, widget, event):
        cr = widget.window.cairo_create()
        cr.set_line_width(1.0)
        cr.set_source_rgb(0.0, 0.0, 0.0)

        for id_from, row in enumerate(self.edges):
            for id_to, col in enumerate(row):
                if col == 1:
                    source = self.graph.get_vertice(id_from)
                    destination = self.graph.get_vertice(id_to)
                    self._draw_direction_arrow(cr, source.get_position(), destination.get_position())
                    #src_x = source.get_position()['x']
                    #src_y = source.get_position()['y']
                    #dst_x = destination.get_position()['x']
                    #dst_y = destination.get_position()['y']
                    #cr.move_to(0, 0)
                    #cr.save()
                    #cr.move_to(src_x, src_y )
                    #cr.line_to(dst_x, dst_y)
                    #cr.stroke_preserve()
                    #cr.move_to(0, 0)
                    #cr.restore()



class GraphView(gtk.Window):

    HEIGHT = 400
    WIDTH = 600
    L_WIDTH = 200
    TARGET_TYPE_TEXT = 80
    fromImage = [ ( "text/plain", 0, TARGET_TYPE_TEXT ) ]
    toCanvas = [ ( "text/plain", 0, TARGET_TYPE_TEXT ) ]
    selected_edge_vertices = []


    def __init__(self, graph):
        super(GraphView, self).__init__()
        self.graph = graph
        labelframe = gtk.Frame("")
        self.label = gtk.Label("")
        self.label.set_justify(gtk.JUSTIFY_LEFT)
        labelframe.add(self.label)

        self.set_title('D-Separacja')
        self.set_size_request(self.WIDTH + 320, self.HEIGHT + 100)
        self.set_position(gtk.WIN_POS_CENTER)
        self.connect("destroy", lambda w: gtk.main_quit())
        layout = self.makeLayout()
        mainbox = gtk.VBox(False,0)
        mainbox.show()
        mainbox.pack_start(layout)
        mainbox.pack_start(labelframe, gtk.TRUE, gtk.TRUE, 5)
        self.add(mainbox)
        self.show_all()

    def layout_resize(self, widget, event):
        x, y, width, height = widget.get_allocation()
        if width > self.lwidth or height > self.lheight:
            self.lwidth = max(width, self.lwidth)
            self.lheight = max(height, self.lheight)
            widget.set_size(self.lwidth, self.lheight)

    def removeVertice(self, widget, id):
        widget.destroy()
        self.graph.delete_vertice(id)
        self.queue_draw()

    def addVertice(self, xd, yd, vertice = None):
        hadj = self.layout.get_hadjustment()
        vadj = self.layout.get_vadjustment()
        if vertice == None:
            vertice = Vertice(int(xd+hadj.value), int(yd+vadj.value))
            self.graph.add_vertice(vertice)
        else:
            vertice.set_position(int(xd+hadj.value), int(yd+vadj.value))

        vertice_event_box = VerticeEventBox(vertice)
        vertice_event_box.connect("drag_data_get", self.sendCallback)
        vertice_event_box.drag_source_set(gtk.gdk.BUTTON1_MASK, self.fromImage,
                               gtk.gdk.ACTION_MOVE)
        vertice_event_box.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        vertice_event_box.connect("button_press_event", self.button_vertice_press_event)

        vertice_event_box.show_all()
        # have to adjust for the scrolling of the layout - event location
        # is relative to the viewable not the layout size
        self.layout.put(vertice_event_box, int(xd+hadj.value-12), int(yd+vadj.value-12))
        self.queue_draw()
        return

    def sendCallback(self, widget, context, selection, targetType, eventTime):
        vertice_id = str(widget.child.vertice.get_id())

        if targetType == self.TARGET_TYPE_TEXT:
            selection.set(selection.target, 8, vertice_id)
            widget.destroy()


    def receiveCallback(self, widget, context, x, y, selection, targetType,
                        time):
        if targetType == self.TARGET_TYPE_TEXT:
            vertice_id = int(selection.data)
            vertice = self.graph.get_vertice(vertice_id)
            self.addVertice(x,y, vertice)

    def makeLayout(self):
        self.lwidth = self.L_WIDTH
        self.lheight = self.HEIGHT

        layout = self.prepare_graph_area()
        self.menu_box = MenuView(self.graph, self.label, self)
        self.menu_box.show()
        box = gtk.HBox(False,20)
        box.show()
        box.pack_start(self.menu_box)
        table = gtk.Table(2, 2, False)
        table.set_size_request(self.WIDTH, self.HEIGHT)
        table.show()

        box.pack_start(table, True, True, 0)

        self.layout = layout
        table.attach(layout, 0, 1, 0, 1, gtk.FILL|gtk.EXPAND,
                     gtk.FILL|gtk.EXPAND, 0, 0)
        # create the scrollbars and pack into the table
        vScrollbar = gtk.VScrollbar(None)
        vScrollbar.show()
        table.attach(vScrollbar, 1, 2, 0, 1, gtk.FILL|gtk.SHRINK,
                     gtk.FILL|gtk.SHRINK, 0, 0)
        hScrollbar = gtk.HScrollbar(None)
        hScrollbar.show()
        table.attach(hScrollbar, 0, 1, 1, 2, gtk.FILL|gtk.SHRINK,
                     gtk.FILL|gtk.SHRINK,
                     0, 0)
        # tell the scrollbars to use the layout widget's adjustments
        vAdjust = layout.get_vadjustment()
        vScrollbar.set_adjustment(vAdjust)
        hAdjust = layout.get_hadjustment()
        hScrollbar.set_adjustment(hAdjust)


        return box

    def reset_graph_area(self):
        #self.layout = self.prepare_graph_area()
        childs = self.layout.get_children()
        for child in childs:
            if child.__class__.__name__ == 'VerticeEventBox':
                child.destroy()

        self.layout.queue_draw()
        return

    def prepare_graph_area(self):
        layout = gtk.Layout()
        layout.set_size(self.WIDTH, self.HEIGHT)
        layout.connect("size-allocate", self.layout_resize)
        drawing_area = GraphViewDrawingArea(self.graph)
        drawing_area.set_size_request(self.WIDTH, self.HEIGHT)
        drawing_area.show()
        layout.add(drawing_area)

        layout.set_name("graph_area")
        layout.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        layout.connect("button_press_event", self.button_graph_area_press_event)
        layout.connect("drag_data_received", self.receiveCallback)
        layout.drag_dest_set(gtk.DEST_DEFAULT_MOTION |
                                  gtk.DEST_DEFAULT_HIGHLIGHT |
                                  gtk.DEST_DEFAULT_DROP,
                                  self.toCanvas, gtk.gdk.ACTION_MOVE)
        layout.show()
        return layout


    def button_graph_area_press_event(self, widget, event):
        if widget.name != "graph_area":
            return
        if self.menu_box.get_state() == SelectionMode.adding_removing_vertices:
            if event.button == 1:
                #self.addImage(gtkxpm.gtk_xpm, event.x, event.y)
                self.addVertice(event.x, event.y)
        elif self.menu_box.get_state() == SelectionMode.adding_removing_edges:
            del self.selected_edge_vertices[:]
            self.graph.set_all_vertices_unselected()
            self.queue_draw()
        return True

    def button_vertice_press_event(self, widget, event):
        if self.menu_box.get_state() == SelectionMode.adding_removing_vertices:
            if event.button == 3:
                self.removeVertice(widget, widget.child.vertice.get_id())
        elif self.menu_box.get_state() == SelectionMode.adding_removing_edges:
            widget.child.vertice.set_selection_state(StateOfVerticeSelection.selected)
            self.queue_draw()
            if len(self.selected_edge_vertices) == 1:
                self.selected_edge_vertices.append(widget.child.vertice.get_id())
                if event.button == 1:
                    if not self.graph.add_edge(self.selected_edge_vertices[0], self.selected_edge_vertices[1]):
                        self.label.set_text("Nie mozna utworzyc krawedzi. Siec bayesowska musi byc skierowanym acyklicznym grafem.")
                    else:
                        self.label.set_text("Utworzono krawedz")
                elif event.button == 3:
                    self.graph.delete_edge(self.selected_edge_vertices[0], self.selected_edge_vertices[1])
                del self.selected_edge_vertices[:]
                self.graph.set_all_vertices_unselected()

            else:
                self.selected_edge_vertices.append(widget.child.vertice.get_id())
        elif self.menu_box.get_state() == SelectionMode.selecting_x:

            if event.button == 1:
                print "selecting x"
                widget.child.vertice.set_selected_set_state(StateOfSetSelection.selectedx)
                self.graph.add_vertice_to_x_set(widget.child.vertice.get_id())
            elif event.button == 3 and widget.child.vertice.get_selected_set_state() == StateOfSetSelection.selectedx:
                print "unselecting x"
                widget.child.vertice.set_selected_set_state(StateOfSetSelection.unselected)
                self.graph.remove_vertice_from_x_set(widget.child.vertice.get_id())
            self.queue_draw()

        elif self.menu_box.get_state() == SelectionMode.selecting_y:
            if event.button == 1:
                print "selecting y"
                widget.child.vertice.set_selected_set_state(StateOfSetSelection.selectedy)
                self.graph.add_vertice_to_y_set(widget.child.vertice.get_id())
            elif event.button == 3 and widget.child.vertice.get_selected_set_state() == StateOfSetSelection.selectedy:
                print "unselecting y"
                widget.child.vertice.set_selected_set_state(StateOfSetSelection.unselected)
                self.graph.remove_vertice_from_y_set(widget.child.vertice.get_id())
            self.queue_draw()
        elif self.menu_box.get_state() == SelectionMode.selecting_z:
            if event.button == 1:
                print "selecting z"
                widget.child.vertice.set_selected_set_state(StateOfSetSelection.selectedz)
                self.graph.add_vertice_to_z_set(widget.child.vertice.get_id())
            elif event.button == 3 and widget.child.vertice.get_selected_set_state() == StateOfSetSelection.selectedz:
                print "unselecting z"
                widget.child.vertice.set_selected_set_state(StateOfSetSelection.unselected)
                self.graph.remove_vertice_from_z_set(widget.child.vertice.get_id())
            self.queue_draw()




        return True
        #if widget.name != "graph_area":
        #    return
        #if self.menu_box.get_state() == 1 and event.button == 1:
        #    #self.addImage(gtkxpm.gtk_xpm, event.x, event.y)
        #    self.addVertice(event.x, event.y)
        #return False


if __name__ == "__main__":
    graph = Graph()
    GraphView(graph)
    gtk.main()
