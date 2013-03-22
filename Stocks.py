#!/usr/bin/python
from gi.repository import Gtk
import ystockquote


class Stocks(Gtk.Window):

    #Using a window subclass to create GUI upon start
    self.num_of_stock = 1
    stock_list = { }

    def __init__(self):
        Gtk.Window.__init__(self, title="Stock Market Watcher")
        self.set_border_width(10)

        pane = Gtk.HPaned()
        self.add(pane)
        self.grid = Gtk.Grid()
        pane.add2(self.grid)
        box = Gtk.Box(spacing=0)
        self.grid.attach(box,2,0,1,1)

        button = Gtk.Button(None,image=Gtk.Image(stock=Gtk.STOCK_ADD))
        button.connect("clicked", self.add_stock)
        
        button2 = Gtk.Button(None, image=Gtk.Image(stock=Gtk.STOCK_ABOUT))
        button2.connect("clicked", self.about_clicked)

        button3 = Gtk.Button(None,image=Gtk.Image(stock=Gtk.STOCK_STOP))
        button3.connect("clicked", lambda w: Gtk.main_quit())
        #Attach to Grid in top right corner
        #grid.attach(button3,4,0,1,1)
        #grid.attach_next_to(button2, button3, Gtk.PositionType.LEFT,1,1)
        #grid.attach_next_to(button,button2,Gtk.PositionType.LEFT,1,1)
        box.pack_end(button,False,False,0)
        box.pack_end(button2,False,False,0)
        box.pack_end(button3,False,False,0)

        button4 = Gtk.Button("Quit More!")
        button4.connect("clicked", lambda w: Gtk.main_quit())
        pane.add1(button4)

    #Begin Handling Connections

    def add_stock(self, widget): 
        entry = self.get_text("Enter your stock symbol below", "Stock")

        if entry != None:
            stock_price = ystockquote.get_price(entry)
            if stock_price == 0:
                alert = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                          Gtk.ButtonsType.OK, "Invalid Stock")
                alert.format_secondary_text("Yahoo had no information on the \
                                            stock you entered. This could be\
                                            due to an incorrect symbol or Yahoo\
                                            simply not having the stock")
                alert.run()
                alert.destroy()
            else:
                #I have returned a valid stock price, create
                # a list of stock values on the screen.
                # Add new stock to the dictionary containing
                # all of the stocks to be displayed
                stock_list[entry] = stock_price
                self.stock = Gtk.Label(entry)
                self.grid.attach(self.stock, 1, num_of_stock, 1, 1)


        print "Stock Added!"

    def about_clicked(self, widget):
        print "This program is designed by Cody Farmer"

    def get_text(parent, message, default=''):
        """
        Display a dialog with a text entry.
        Returns the text, or None if canceled.
        """
        d = Gtk.MessageDialog(parent,
                              Gtk.DialogFlags.MODAL |
                              Gtk.DialogFlags.DESTROY_WITH_PARENT,
                              Gtk.MessageType.QUESTION,
                              Gtk.ButtonsType.OK_CANCEL,
                              message)
        entry = Gtk.Entry()
        entry.set_text(default)
        entry.show()
        d.vbox.pack_end(entry,False,False,0)
        entry.connect('activate', lambda _: d.response(Gtk.ResponseType.OK))
        d.set_default_response(Gtk.ResponseType.OK)
        
        r = d.run()
        text = entry.get_text().decode('utf8')
        d.destroy()
        if r == Gtk.ResponseType.OK:
            return text
        else:
            return None

win = Stocks()
win.set_default_size(400,300)
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
