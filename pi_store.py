
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')
from gi.repository import Gtk, WebKit, GObject
import requests

class Store(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="Pi Store")
		self.set_border_width(10)

		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		self.add(vbox)
		
		#Web view
		self.webview = WebKit.WebView()
		self.webview.show()
		self.webview.open("http://localhost:8000")
		vbox.pack_start(self.webview, True, True, 0)
		#~ self.webview.open("https://piStore.pythonanywhere.com")# Production
		self.webview.connect('download-requested', self.download_requested)
		self.webview.connect('mime-type-policy-decision-requested', self.policy_decision_requested)
		
		#Progress bar
		self.progressbar = Gtk.ProgressBar()
		vbox.pack_start(self.progressbar, True, True, 0)
		
		self.timeout_id = GObject.timeout_add(50, self.on_timeout, None)
		self.activity_mode = False
		
		self.progressbar.set_text("Installing...")
		self.progressbar.set_show_text(self.activity_mode)
		self.progressbar.set_pulse_step(0.03)
		
		
	def policy_decision_requested(self, view, frame, request, mimetype, policy_decision):
		if mimetype != 'text/html':
				policy_decision.download()
				return True
		
	def download_requested(self, view, download):
		self.activity_mode = True
		name = download.get_suggested_filename()
		path = "/home/linus/Downloads/"
		r = requests.get(download.get_uri())
		with open(path+name,'wb') as f:
			f.write(r.content)
		return False
		
	def on_timeout(self, user_data):
		if self.activity_mode:
			self.progressbar.pulse()

		return True

win = Store()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
