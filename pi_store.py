import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')
from gi.repository import Gtk, WebKit

def openWeb(url):
	""" Delete the image and load webview. """
	webview = WebKit.WebView()
	webHolder.add(webview)
	webview.show()
	webview.open(url)

def onDeleteWindow(self, *args):
    Gtk.main_quit(*args)        
    
def on_infobarClose_clicked(self):
	barinfo.hide()

builder = Gtk.Builder()
builder.add_from_file("store.glade")
sigs = {
    "on_infobarClose_clicked":on_infobarClose_clicked,
    "on_infoBarKill_clicked":onDeleteWindow,
    
}
builder.connect_signals(sigs)
barinfo = builder.get_object("infobar1")
webHolder = builder.get_object("box1")
window = builder.get_object("main")
#~ openWeb("https://piStore.pythonanywhere.com")# Production
openWeb("http://localhost:8000")
window.show_all()
Gtk.main()
