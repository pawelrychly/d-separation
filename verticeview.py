__author__ = 'pawel rychly'

import pygtk
pygtk.require('2.0')
import gtk
import string, time
import math
from graph import *

class VerticeEventBox(gtk.EventBox):

    def __init__(self, vertice):
        super(VerticeEventBox, self).__init__()
        vertice_view = VerticeView(vertice)
        #self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(65000, 65000, 65000))
        vertice_view.show()
        self.set_size_request(25,25)
        self.add(vertice_view)

class VerticeView(gtk.DrawingArea):

    def __init__(self, vertice):
        super(VerticeView, self).__init__()
        self.vertice = vertice
        #self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(255, 255, 255))
        self.connect("expose-event", self.expose)

    def expose(self, widget, event):
        position = self.vertice.get_position()
        cr = widget.window.cairo_create()

        cr.set_line_width(4)
        #cr.set_source_rgb(0.7, 0.2, 0.0)
        if self.vertice.get_selection_state() == StateOfVerticeSelection.selected:
            cr.set_source_rgb(0.9, 0.3, 0.3)
        else:
            cr.set_source_rgb(0.7, 0.7, 0.7)

        w = self.allocation.width
        h = self.allocation.height

        cr.translate(w/2, h/2)
        cr.arc(0, 0, 10, 0, 2*math.pi)
        cr.stroke_preserve()

        #cr.set_source_rgb(0.3, 0.4, 0.6)
        if self.vertice.get_selected_set_state() == StateOfSetSelection.selectedx:
            cr.set_source_rgb(0.9, 0.9, 0.3)
        elif self.vertice.get_selected_set_state() == StateOfSetSelection.selectedy:
            cr.set_source_rgb(0.7, 0.7, 1)
        elif self.vertice.get_selected_set_state() == StateOfSetSelection.selectedz:
            cr.set_source_rgb(0.3, 0.9, 0.3)
        else:
            cr.set_source_rgb(1.0, 1.0, 1.0)

        cr.fill()
        cr.stroke_preserve()
        #cr.set_source_rgb(0.7, 0.2, 0.0)
        cr.set_source_rgb(0.0, 0.0, 0.0)
        cr.translate(-w/6, h/7)
        cr.show_text(str(self.vertice.get_id()))



        #self._draw_circle(cr, position)
        #cr.set_source_rgb(0.7, 0.2, 0.0)
        #cr.save()
        #cr.translate(position["x"], position["y"])
        #self._draw_direction_arrow(cr)
        #cr.arc(0, 0, 5, 0, 2 * math.pi)
        #cr.stroke_preserve()
        #cr.set_source_rgb(0.3, 0.4, 0.6)
        #cr.fill()
        #cr.restore()
        #self._draw_filter(cr)