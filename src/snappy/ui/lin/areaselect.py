#!/usr/bin/env python
# Copyright (C) 2009 Donald S. F. Harvey
#
# This file is part of Snappy.
#
# Snappy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Snappy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Snappy.  If not, see <http://www.gnu.org/licenses/>.

# TODO: FINISH REFACTORING!
# THIS CODE IS TERRIBLE!

import gobject
import pango
import pygtk
import pangocairo
pygtk.require('2.0')
import gtk
from gtk import gdk
import cairo
from datetime import datetime

if gtk.pygtk_version < (2,10,0):
	print "PyGtk 2.10.0 or later required"
	raise SystemExit

class SelectArea(gtk.Window):
	'''
	The SelectArea window provides area selection to Snappy.
	'''
	def get_selection(self, point):
		if not point:
			return (self.rectselection.x, self.rect_selection.y, self.rect_selection.width, self.rect_selection.height)
		elif point == 'x':
			return self.rect_selection.x
		elif point == 'y':
			return self.rect_selection.y
		elif point == 'width':
			return self.rect_selection.width
		elif point == 'height':
			return self.rect_selection.height

	def keypress(self, widget, event):
		if event.keyval == 65307:
			# escape key pressed. Destroy the window
			self.window.destroy()
			gtk.main_quit()
			self.escaped == True

	def clicked(self, widget, event):
		self.mousedownlocation = (event.x_root, event.y_root)
		print self.mousedownlocation

	def mousemove(self, widget, event):
		self.mouselocation = (event.x_root, event.y_root)
		if self.mouselocation [0] > self.mousedownlocation[0]:
			width = self.mouselocation[0] - self.mousedownlocation[0]
			x = self.mousedownlocation[0]
		else:
			width = self.mousedownlocation[0] - self.mouselocation[0]
			x = self.mouselocation[0]

		if self.mouselocation[1] > self.mousedownlocation[1]:
			height = self.mouselocation[1] - self.mousedownlocation[1]
			y = self.mousedownlocation[1]
		else:
			height = self.mousedownlocation[1] - self.mouselocation[1]
			y = self.mouselocation[1]
		x = int(x)
		y = int(y)
		width = int(width)
		height = int(height)
		(winwidth, winheight) = widget.get_size()
		self.rect_selection = gtk.gdk.Rectangle(x, y, width, height)
		self.window.queue_draw()

	def released(self, widget, event):
		self.mouseuplocation = (event.x_root, event.y_root)
		print self.mouseuplocation
		if self.mouseuplocation [0] > self.mousedownlocation[0]:
			width = self.mouseuplocation[0] - self.mousedownlocation[0]
			x = self.mousedownlocation[0]
		else:
			width = self.mousedownlocation[0] - self.mouseuplocation[0]
			x = self.mouseuplocation[0]

		if self.mouseuplocation[1] > self.mousedownlocation[1]:
			height = self.mouseuplocation[1] - self.mousedownlocation[1]
			y = self.mousedownlocation[1]
		else:
			height = self.mousedownlocation[1] - self.mouseuplocation[1]
			y = self.mouseuplocation[1]
		x = int(x)
		y = int(y)
		width = int(width)
		height = int(height)
		(winwidth, winheight) = widget.get_size()
		self.rect_selection = gtk.gdk.Rectangle(x, y, width, height)
		self.window.queue_draw()
		self.window.destroy()
		gtk.main_quit()


	def expose(self, widget, event):
		'''Main drawing function.'''
		(width, height) = widget.get_size()

		# Get a cairo context
		cr = widget.window.cairo_create()

		# Make the window transparent
		if self.supports_alpha == True:
			cr.set_source_rgba(0.0, 0.0, 0.0, 0)
		else:
			cr.set_source_rgb(1.0, 1.0, 1.0)
		cr.set_operator(cairo.OPERATOR_SOURCE)
		cr.paint()


		# Draw the overlay at 75% opacity
		cr.set_source_rgba(0, 0, 0, 0.75)
		cr.rectangle(0, 0, float(width), float(height))
		#cr.mask(pat)
		cr.fill()
		cr.stroke()

		# Draw the selection box
		cr.set_source_rgba(1, 1, 1, 0)
		cr.set_line_width(2)
		cr.rectangle(float(self.rect_selection.x), float(self.rect_selection.y), float(self.rect_selection.width), float(self.rect_selection.height))

		cr.fill()
		dashes = [ 1.0, 2.0 ]
		cr.set_source_rgba(1, 0.9, 0, 1)
		cr.set_line_width(2)
		cr.move_to(float(self.rect_selection.x - 1), float(self.rect_selection.y - 1))
		cr.line_to(float(self.rect_selection.x + self.rect_selection.width + 1), float(self.rect_selection.y - 1))
		cr.line_to(float(self.rect_selection.x + self.rect_selection.width + 1), float(self.rect_selection.y + self.rect_selection.height + 1))
		cr.line_to(float(self.rect_selection.x - 1), float(self.rect_selection.y + self.rect_selection.height + 1))
		cr.close_path()
		cr.stroke()

		if self.rect_selection.width > 0 and self.rect_selection.height > 0:
			pg = pangocairo.CairoContext(cr)
			pgl = pg.create_layout()
			(pglw, pglh) = pgl.get_pixel_size()
			pgfont = pango.FontDescription("sans bold 14")
			pgfont.set_family("MgOpen Moderna")
			pgl.set_text(str(self.rect_selection.width) + 'px x ' + str(self.rect_selection.height) + 'px')
			pgl.set_font_description(pgfont)
			print 'Width, height = ' + str(pglw + self.rect_selection.width) + ', ' + str(pglh + self.rect_selection.height)
			if self.rect_selection.width + pglw > width:
				print 'Greater than self.window width'
				pglx = float(width - pglw)
				print pglx
			else:
				pglx = float(self.rect_selection.x)
			if self.rect_selection.height + pglh > height:
				print 'Greater than self.window height'
				pgly = float(height - pglh)
			else:
				pgly = float(self.rect_selection.y)
			cr.move_to(pglx, pgly)
			pg.show_layout(pgl)

		pm = gtk.gdk.Pixmap(None, width, height, 1)
		pmcr = pm.cairo_create()
		pmcr.rectangle(0, 0, float(width), float(height))
		pmcr.fill()
		pmcr.stroke()

		self.input_shape_combine_mask(pm, 0, 0)

		return False

	def destroy(self, widget, data=None):
		gtk.main_quit()
		return 'failed!'

	def screen_changed(self, widget=None, old_screen=None):
		screen = self.get_screen()
		colormap = screen.get_rgba_colormap()
		if colormap == None:
			print 'Your screen does not support alpha channels!'
			colormap = screen.get_rgb_colormap()
			self.supports_alpha = False
		else:
			print 'Your screen supports alpha channels!'
			self.supports_alpha = True

		widget.set_colormap(colormap)

		return True

	def realize(self, widget):
		cursor = gtk.gdk.Cursor(gtk.gdk.CROSSHAIR)
		widget.window.set_cursor(cursor)

	def __init__(self):
		escaped = False
		rect_selection = gtk.gdk.Rectangle(0, 0, 0, 0)
		gtk.Window.__init__(self)
		self.set_property("skip-taskbar-hint", True)

		self.connect('delete-event', gtk.main_quit)

		self.set_app_paintable(True)
		self.set_double_buffered(False)

		self.connect('expose-event', self.expose)
		self.fullscreen()
		self.set_decorated(False)
		self.add_events(gdk.BUTTON_PRESS_MASK)
		self.add_events(gdk.BUTTON_RELEASE_MASK)
		self.add_events(gdk.BUTTON1_MOTION_MASK)
		self.add_events(gdk.KEY_RELEASE_MASK)
		self.screen_changed()
		self.connect('button-press-event', self.clicked)
		self.connect('button-release-event', self.released)
		self.connect_object('button-release-event', self.destroy, self.window)
		self.connect('motion-notify-event', self.mousemove)
		self.connect('realize', self.realize)
		self.connect('key_release_event', self.keypress)
		self.show_all()
		pass

	def main(self):
		gtk.main()
		return True
if __name__ == '__main__':
	screenshot = SelectArea()
	screenshot.main()
