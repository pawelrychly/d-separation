__author__ = 'pawel rychly'

import pygtk
pygtk.require('2.0')
import gtk
import string, time
import gtkxpm
from graph import *
from verticeview import *


class SelectionMode:
    adding_removing_vertices = 0
    moving_vertices = 1
    adding_removing_edges = 2
    selecting_x = 3
    selecting_y = 4
    selecting_z = 5

class MenuView(gtk.VBox):
    __state = SelectionMode.adding_removing_vertices
    def __init__(self):
        super(MenuView, self).__init__(self)
        first_button = gtk.RadioButton(None, "Adding / Removing vertices")
        first_button.connect("toggled", self.radio_button_callback, SelectionMode.adding_removing_vertices)
        self.pack_start(first_button, gtk.TRUE, gtk.TRUE, 0)
        first_button.show()

        button = gtk.RadioButton(first_button, "Moving vertices")
        button.connect("toggled", self.radio_button_callback, SelectionMode.moving_vertices)
        self.pack_start(button, gtk.TRUE, gtk.TRUE, 0)
        button.show()

        button = gtk.RadioButton(first_button, "Adding / Removing edges")
        button.connect("toggled", self.radio_button_callback, SelectionMode.adding_removing_edges)
        self.pack_start(button, gtk.TRUE, gtk.TRUE, 0)
        button.show()

        button = gtk.RadioButton(first_button, "Selecting Z")
        button.connect("toggled", self.radio_button_callback, SelectionMode.selecting_z)
        self.pack_start(button, gtk.TRUE, gtk.TRUE, 0)
        button.show()

        button = gtk.RadioButton(first_button, "Selecting Y")
        button.connect("toggled", self.radio_button_callback, SelectionMode.selecting_y)
        self.pack_start(button, gtk.TRUE, gtk.TRUE, 0)
        button.show()

        button = gtk.RadioButton(first_button, "Selecting X")
        button.connect("toggled", self.radio_button_callback, SelectionMode.selecting_x)
        self.pack_start(button, gtk.TRUE, gtk.TRUE, 0)
        button.show()

        button = gtk.Button("Start")
        self.pack_start(button, gtk.TRUE, gtk.TRUE, 0)
        button.show()

    def get_state(self):
        return self.__state

    def radio_button_callback(self, widget, data=None):
        if widget.get_active():
            self.__state = data
            print self.__state


class GraphViewDrawingArea(gtk.DrawingArea):
    def __init__(self, graph):
        super(GraphViewDrawingArea, self).__init__()
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0, 0, 0))
        self.graph = graph
        self.connect("expose-event", self.expose)


    def expose(self, widget, event):
        cr = widget.window.cairo_create()


class GraphView(gtk.Window):

    HEIGHT = 400
    WIDTH = 600
    L_WIDTH = 200
    TARGET_TYPE_PIXMAP = 81
    fromImage = [ ( "image/x-xpixmap", 0, TARGET_TYPE_PIXMAP ) ]
    toCanvas = [ ( "image/x-xpixmap", 0, TARGET_TYPE_PIXMAP ) ]

    def __init__(self, graph):
        super(GraphView, self).__init__()
        self.graph = graph
        self.menu_box = MenuView()
        self.menu_box.show()
        self.set_title('D-Separation')
        self.set_size_request(self.WIDTH + 250, self.HEIGHT)
        self.set_position(gtk.WIN_POS_CENTER)
        self.connect("destroy", lambda w: gtk.main_quit())
        layout = self.makeLayout()
        self.add(layout)
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

    def addVertice(self, xd, yd):
        hadj = self.layout.get_hadjustment()
        vadj = self.layout.get_vadjustment()
        vertice = Vertice(int(xd+hadj.value), int(yd+vadj.value))
        self.graph.add_vertice(vertice)
        vertice_event_box = VerticeEventBox(vertice)
        vertice_event_box.connect("drag_data_get", self.sendCallback)
        vertice_event_box.drag_source_set(gtk.gdk.BUTTON1_MASK, self.fromImage,
                               gtk.gdk.ACTION_COPY)
        vertice_event_box.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        vertice_event_box.connect("button_press_event", self.button_vertice_press_event)

        vertice_event_box.show_all()
        # have to adjust for the scrolling of the layout - event location
        # is relative to the viewable not the layout size
        self.layout.put(vertice_event_box, int(xd+hadj.value), int(yd+vadj.value))
        self.queue_draw()
        return


    def addImage(self, xpm, xd, yd):
        hadj = self.layout.get_hadjustment()
        vadj = self.layout.get_vadjustment()
        style = self.get_style()
        pixmap, mask = gtk.gdk.pixmap_create_from_xpm_d(
            self.window, style.bg[gtk.STATE_NORMAL], xpm)
        image = gtk.Image()
        image.set_from_pixmap(pixmap, mask)
        button = gtk.EventBox()
        button.add(image)
        button.connect_after("drag_data_get", self.sendCallback)
        button.drag_source_set(gtk.gdk.BUTTON1_MASK, self.fromImage,
                               gtk.gdk.ACTION_COPY)
        button.show_all()
        # have to adjust for the scrolling of the layout - event location
        # is relative to the viewable not the layout size
        self.layout.put(button, int(xd+hadj.value), int(yd+vadj.value))
        return

    def sendCallback(self, widget, context, selection, targetType, eventTime):
        if targetType == self.TARGET_TYPE_PIXMAP:
            selection.set(selection.target, 8,
                          string.join(gtkxpm.gtk_xpm, '\n'))

    def receiveCallback(self, widget, context, x, y, selection, targetType,
                        time):
        if targetType == self.TARGET_TYPE_PIXMAP:
            #self.addImage(string.split(selection.data, '\n'), x, y)
            self.addVertice(x,y)

    def makeLayout(self):
        self.lwidth = self.L_WIDTH
        self.lheight = self.HEIGHT
        box = gtk.HBox(False,0)
        box.show()
        box.pack_start(self.menu_box)
        table = gtk.Table(2, 2, False)
        table.set_size_request(self.WIDTH, self.HEIGHT)
        table.show()

        box.pack_start(table, True, True, 0)
        layout = gtk.Layout()
        layout.set_name("graph_area")
        self.layout = layout
        layout.set_size(self.WIDTH, self.HEIGHT)
        layout.connect("size-allocate", self.layout_resize)
        drawing_area = GraphViewDrawingArea(self.graph)
        drawing_area.show()
        layout.add(drawing_area)
        layout.show()
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
        layout.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        layout.connect("button_press_event", self.button_graph_area_press_event)
        layout.connect("drag_data_received", self.receiveCallback)
        layout.drag_dest_set(gtk.DEST_DEFAULT_MOTION |
                                  gtk.DEST_DEFAULT_HIGHLIGHT |
                                  gtk.DEST_DEFAULT_DROP,
                                  self.toCanvas, gtk.gdk.ACTION_COPY)


        return box
        #self.addImage(gtkxpm.gtk_xpm, 0, 0)
        #button = gtk.Button("Text Target")
        #button.show()
        #button.connect("drag_data_received", self.receiveCallback)
        #button.drag_dest_set(gtk.DEST_DEFAULT_MOTION |
        #                     gtk.DEST_DEFAULT_HIGHLIGHT |
        #                     gtk.DEST_DEFAULT_DROP,
        #                     self.toButton, gtk.gdk.ACTION_COPY)
        #box.pack_start(button, False, False, 0)
        #return box
    def button_graph_area_press_event(self, widget, event):
        print "graph area clicked"
        if widget.name != "graph_area":
            return
        if self.menu_box.get_state() == SelectionMode.adding_removing_vertices:
            if event.button == 1:
                #self.addImage(gtkxpm.gtk_xpm, event.x, event.y)
                self.addVertice(event.x, event.y)


        return True

    def button_vertice_press_event(self, widget, event):
        print "clicked"
        if self.menu_box.get_state() == SelectionMode.adding_removing_vertices:
            if event.button == 3:
                self.removeVertice(widget, widget.child.vertice.get_id())
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
