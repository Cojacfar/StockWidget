#!/usr/bin/python
from gi.repository import Gtk, Gdk
import ystockquote


class Stocks(Gtk.Window):

    #Creating UI
    UI_INFO = """
    <ui>
        <toolbar name='Toolbar'>
            <toolitem action='Add' />
            <toolitem action='About' />
            <toolitem action='Exit' />
        </toolbar>
    </ui>
    """
    #Using a window subclass and creating GUI upon initialization
    def __init__(self):
        Gtk.Window.__init__(self, title="Stock Market Watcher")
        self.set_border_width(10)

        #Create UI
        uimanager = Gtk.UIManager()
        uimanager.add_ui_from_string(UI_INFO)

        #Create ListStore to hold stock values then display
        self.data = Gtk.ListStore(str, str)
        self.data.append(["Test", "Test2"])
        self.view = Gtk.TreeView(self.data)
        self.text_renderer = Gtk.CellRendererText()
        self.text_renderer.set_property("editable", True)
        self.stock_names = Gtk.TreeViewColumn("Stocks", self.text_renderer, text=0)
        self.stock_prices = Gtk.TreeViewColumn("Price", self.text_renderer, text=0)
        self.view.append_column(self.stock_names)
        self.view.append_column(self.stock_prices)

        pane = Gtk.HPaned()
        self.add(pane) 
        box = Gtk.Box(spacing=0)
        pane.add2(self.view)
        
        pane.add2(box)

        button = Gtk.Button(None,image=Gtk.Image(stock=Gtk.STOCK_ADD))
        button.connect("clicked", self.add_stock)
        
        button2 = Gtk.Button(None, image=Gtk.Image(stock=Gtk.STOCK_ABOUT))
        button2.connect("clicked", self.about_clicked)

        button3 = Gtk.Button(None,image=Gtk.Image(stock=Gtk.STOCK_STOP))
        button3.connect("clicked", lambda w: Gtk.main_quit())
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
                #I have returned a valid stock price, add this
                # new stock to the list widget
                self.data.append([entry, stock_price])




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
