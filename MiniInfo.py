# Copyleft Nalle Berg 2025
# License GPL V2
AppVersion = '0.8.0'

# Importing modules
import tkinter as tk					 
from tkinter import ttk
from tkinter import ttk, Menu
import psutil
from psutil import disk_partitions
import urllib.request
import socket
import wmi
import platform
import sys
import os
import webbrowser
import locale
import subprocess
from screeninfo import get_monitors
import math
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Disable DPI scaling

global i # I need it to bew global further down to use it in some functions

# Making the app know it's path.
def resource_path(relative_path):
		try:
			base_path = sys._MEIPASS
		except Exception:
			base_path = os.path.abspath(".")

		return os.path.join(base_path, relative_path)

# Language file:
# Norwegian: NO_nb_lang - English: EN_uk_lang
exec(open(resource_path("NO_nb_lang"), encoding="utf-8").read())

def main():
    
    # I use WMI for several things, so I also query in several ways.
    # This one gets used both on the «Network» and the «PC» page
	c = wmi.WMI()    
	my_system = c.Win32_ComputerSystem()[0]
    
    # Local IP & Default Gateway I do the querys here to use to detemine if you are on net and internet
	wmi_obj = wmi.WMI()
	wmi_sql = "select IPAddress,DefaultIPGateway from Win32_NetworkAdapterConfiguration where IPEnabled=TRUE"
	wmi_out = wmi_obj.query( wmi_sql )
	
	# For some diskinfo as bus, type and model used in a for-loop
	wmi_obj_1 = wmi.WMI(namespace='root/Microsoft/Windows/Storage')
 
	# Checking if you are at all on the network.
 	# Expecting you will always have a IPv4 address on your local netwok i ask for it.
	# It is bolean, just to make it easier to query for it later.
	for dev in wmi_out:
		LocalIPv4 = dev.IPAddress[0]
	try:
		LocalIPv4
	except NameError:
		OnNetWork = False
	else:
		OnNetWork = True
  	
	# We also need to know if we're on the internet.
	REMOTE_SERVER = "one.one.one.one"
	def is_connected(hostname):
		try:
    		# See if we can resolve the host name - tells us if there is
    		# A DNS listening
			host = socket.gethostbyname(hostname)
   			# Connect to the host - tells us if the host is actually reachable
			s = socket.create_connection((host, 80), 2)
			s.close()
			return True
		except Exception:
			pass # We ignore errors, only looking for «True»

    # Google to the rescue! It's always there.
	OnInternet = is_connected('www.google.com')
	
    
	# Making the app know it's path.
	# Importing «os» here, since it for some rason had to be within main()
	import os
	
	# Defining the window
	Window = tk.Tk() 
	Window.minsize(1200, 0)
 
	# Adding title
	Window.title("MiniInfo V " + AppVersion)  # Initial titlw
	# with
	# Function to toggle "always on top"
	def toggle_topmost():
		if Window.attributes("-topmost"):
			Window.attributes("-topmost", False)
			Window.title("MiniInfo V " + AppVersion)  # Reset title
			toggle_var.set(0)  # Uncheck the menu item
		else:
			Window.attributes("-topmost", True)
			Window.title("MiniInfo V " + AppVersion +" - " + AlwaysOnTopText)  # Append " - Always on Top"
			toggle_var.set(1)  # Check the menu item

	# Create a menu bar
	menu_bar = Menu(Window)
	Window.config(menu=menu_bar)
 
	 # Create a toggle variable
	toggle_var = tk.IntVar(value=0)
	
    # Add the "Always on Top" toggle option directly to the menu bar
	menu_bar.add_checkbutton(label=AlwaysOnTopText, variable=toggle_var, command=toggle_topmost)


 
 	# For your own icon 
	ICO = tk.PhotoImage(file=(resource_path("info.png"))) 
	Window.iconphoto(True, ICO)

	# Getting the memory information
	mem = psutil.virtual_memory()
	swap = psutil.swap_memory()

	# Getting CPU information
	cpufreq = psutil.cpu_freq()
	CPUProc = platform.processor()

	tabControl = ttk.Notebook(Window)

	tab1 = ttk.Frame(tabControl) 
	tab2 = ttk.Frame(tabControl) 
	tab3 = ttk.Frame(tabControl) 
	tab4 = ttk.Frame(tabControl)
	tab5 = ttk.Frame(tabControl)
	tab6 = ttk.Frame(tabControl)
	tab7 = ttk.Frame(tabControl)
	tab8 = ttk.Frame(tabControl)
	tab9 = ttk.Frame(tabControl)
	

	tabControl.add(tab1, text = Tab1Text) 
	tabControl.add(tab2, text = Tab2Text) 
	tabControl.add(tab3, text = Tab3Text) 
	tabControl.add(tab4, text = Tab4Text)
	tabControl.add(tab5, text = Tab5Text)
	tabControl.add(tab6, text = Tab6Text)
	tabControl.add(tab7, text = Tab7Text)
	tabControl.add(tab8, text = Tab8Text)
	tabControl.add(tab9, text = Tab9Text)
	

	tabControl.pack(expand = False, fill = "both", side="top") 
	

	# Format memory and swap values
			
	mem_total = mem.total / (1024 * 1024 * 1024)
	memsize = f"{mem_total:.2f} GB".replace(',', ' ').replace('.', ',')
	
	mem_used = mem.used / (1024 * 1024 * 1024)
	memused = f"{mem_used:.2f} GB".replace(',', ' ').replace('.', ',')
 
	mem_free = mem.free / (1024 * 1024 * 1024)
	memfree = f"{mem_free:.2f} GB".replace(',', ' ').replace('.', ',')

	swap_total = swap.total / (1024 * 1024 * 1024)
	swaptotal = f"{swap_total:.2f} GB".replace(',', ' ').replace('.', ',')

	swap_used = swap.used / (1024 * 1024 * 1024)
	swapused = f"{swap_used:.2f} GB".replace(',', ' ').replace('.', ',')
    
	swap_free = swap.free / (1024 * 1024 * 1024)
	swapfree = f"{swap_free:.2f} GB".replace(',', ' ').replace('.', ',')


	
	if OnNetWork:
		for dev in wmi_out:
			DefGWv4 = dev.DefaultIPGateway[0] 
			DefGWv6 = dev.DefaultIPGateway[1]
			LocalIPv4 = dev.IPAddress[0]
			LocalIPv6 = dev.IPAddress[1]
  
		# Networkadapter (active) an it's Mac address
		for interface in wmi_obj.Win32_NetworkAdapterConfiguration (IPEnabled=1):
			ActiveNetCard = interface.Description 
			MacAddr = interface.MACAddress


		# Network info, fetching
		# Hostname
		hostname = socket.gethostname()
  
	if OnInternet:
 		# External IP
		external_ip_v4 = urllib.request.urlopen('https://ipv4.ident.me').read().decode('utf8')
		external_ip_v6 = urllib.request.urlopen('https://ipv6.ident.me').read().decode('utf8')
	
	# OS
	# OS name
	for os in wmi_obj.Win32_OperatingSystem():
		OSName = os.caption
  
	OSVersion = platform.version()
	OSMachine = platform.machine()
 
	loc = locale.getlocale() # get current locale
	enc = locale.getencoding() # get encoding

	#####################################################################
	# Displaying ########################################################
	#####################################################################
 
	# Network 
	ttk.Label(tab1, 
		text = NetworkTitleText, foreground="blue", font=("Verdana", 16, "bold")).grid(column = 0, 
									row = 0, 
									padx = 10, 
									pady = 3,
                                    columnspan=2)
	
	ttk.Label(tab1, 
		text = ActiveCardText, anchor="nw", font=("Verdana", 9, "bold")).grid(column = 0, 
									row = 1, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW') 
	# If there is no net
	if not OnNetWork:
		ActiveNetCard = NoActiveCardText 
	ttk.Label(tab1, 
		text = ActiveNetCard+"\n ", anchor="nw", font=("Verdana", 9)).grid(column = 1, 
									row = 1, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW') 
  
	
	ttk.Label(tab1, 
		text = MachineNetNameText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 2, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW') 
	# If no network
	if not OnNetWork:
		hostname = NoActiveCardText 
	
	ttk.Label(tab1, 
		text = hostname+"\n ", anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = 2, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW')
	
	ttk.Label(tab1, 
		text = LocalIPv4Text , anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 3, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW')
	# If no network
	if not OnNetWork:
		LocalIPv4 = NoActiveCardText
  
	ttk.Label(tab1, 
		text = LocalIPv4+"\n ", anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = 3, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW')
	# Local IP address V6
	ttk.Label(tab1, 
		text = LocalIPv6Text , anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 4, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW') 
	# If no network
	if not OnNetWork:
		LocalIPv6 = NoActiveCardText

	ttk.Label(tab1, 
		text = LocalIPv6+"\n ", anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = 4, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW')
	
	ttk.Label(tab1, 
		text = ExtIPv4Text, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 5, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW') 
	# If no Internet
	if not OnInternet:
		external_ip_v4 = NotOnInternetText
  
	ttk.Label(tab1, 
		text = external_ip_v4+"\n ", anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = 5, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW') 
	ttk.Label(tab1, 
		text = ExtIPv6Text, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 6, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW')
	# If no Internet
	if not OnInternet:
		external_ip_v6 = NotOnInternetText
  
	ttk.Label(tab1, 
		text = external_ip_v6+"\n ", anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = 6, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW') 
	ttk.Label(tab1, 
		text = StdGWv4Text, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 7, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW') 
  
	if not OnNetWork:
		DefGWv4 = NoActiveCardText

	ttk.Label(tab1, 
		text =DefGWv4+"\n ", anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = 7, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW') 
	ttk.Label(tab1, 
		text = StdGWv6Text, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 8, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW')  
	if not OnNetWork:
		DefGWv6 = NoActiveCardText
  
	ttk.Label(tab1, 
		text = DefGWv6+"\n ", anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = 8, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW') 
	ttk.Label(tab1, 
		text = MacAddrText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 9, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW')

	if not OnNetWork:
		MacAddr = NoActiveCardText
 
	ttk.Label(tab1, 
		text = MacAddr+"\n ", anchor="nw").grid(column = 1, 
									row = 9, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW') 

	# Getting domain and workgroup
	net_domain = my_system.Domain
	net_workgroup = my_system.Workgroup
 
	ttk.Label(tab1, 
		text = NetDomainText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 10, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW')

	if not OnNetWork:
		net_domain = NoActiveCardText
 
	ttk.Label(tab1, 
		text = net_domain, anchor="nw").grid(column = 1, 
									row = 10, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW') 
	ttk.Label(tab1, 
		text = NetWorkgroupText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 11, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW')

	if not OnNetWork:
		net_domain = NoActiveCardText
 
	ttk.Label(tab1, 
		text = net_workgroup, anchor="nw").grid(column = 1, 
									row = 11, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW') 



###########
# CPU
	ttk.Label(tab2, 
		text = CPUTitleText, foreground="blue", font=("Verdana", 16, "bold")).grid(column = 0, 
									row = 0, 
									padx = 10, 
									pady = 3,
                                    columnspan=2)
 
	ttk.Label(tab2, 
		text = ProcessorText, font=("Verdana", 8, "bold")).grid(column = 0, 
			    					row = 1, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW') 
	ttk.Label(tab2, 
		text = CPUProc, anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = 1, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW',
                                    columnspan=2)
	ttk.Label(tab2, 
		text = PhysicKernelText, font=("Verdana", 8, "bold")).grid(column = 0, 
			    					row = 2, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW')
	ttk.Label(tab2, 
		text = psutil.cpu_count(logical=False), anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = 2, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW')
	ttk.Label(tab2, 
		text = PiecesText, anchor="nw", font=("Verdana", 8)).grid(column = 2, 
									row = 2, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW')
  
	ttk.Label(tab2, 
		text = TotalKernelText, font=("Verdana", 8, "bold")).grid(column = 0, 
			    					row = 3, 
									padx = 10, 
									pady = 1,
                                    sticky='NESW') 
	ttk.Label(tab2, 
		text = psutil.cpu_count(logical=True), anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = 3, 
									padx = 10, 
									pady = 1,
                                    sticky='NESW')
	ttk.Label(tab2, 
		text = PiecesText, anchor="nw", font=("Verdana", 8)).grid(column = 2, 
									row = 3, 
									padx = 10, 
									pady = 1,
                                    sticky='NESW')
  
	ttk.Label(tab2, 
		text = MaxCPUFreqText, font=("Verdana", 8, "bold")).grid(column = 0, 
			    					row = 4, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW') 
	ttk.Label(tab2, 
		text = f"{cpufreq.max:.2f}", anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = 4, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW')
	ttk.Label(tab2, 
		text = MhzText, anchor="nw", font=("Verdana", 8)).grid(column = 2, 
									row = 4, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW') 
  
  
	ttk.Label(tab2, 
		text = CurCPUFreqText, font=("Verdana", 8, "bold")).grid(column = 0, 
			    					row = 5, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW')

	ttk.Label(tab2, 
		text = MhzText, anchor="nw", font=("Verdana", 8)).grid(column = 2, 
									row = 5, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW')
  
	ttk.Label(tab2, 
		text = CurCPUUsageText, font=("Verdana", 8, "bold")).grid(column = 0, 
			    					row = 6, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW')
	
	ttk.Label(tab2,
		text = "%", anchor="nw", font=("Verdana", 8)).grid(column = 2, 
									row = 6, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW')

	def update_cpu_info(tab2):
		def update():
			# Fetch current CPU frequency
			cpufreq = psutil.cpu_freq()
			current_freq = cpufreq.current

			# Fetch current CPU usage
			cpu_usage = psutil.cpu_percent(interval=0.1)

			# Update CPU Frequency
			cpu_freq_label.config(text=f"{current_freq:.2f}")

			# Update CPU Usage
			cpu_usage_label.config(text=f"{cpu_usage}")

			# Schedule the next update
			Window.after(1000, update)  # Update every 1 second (1000 milliseconds)

		# Create labels for CPU frequency and usage if they don't exist
		global cpu_freq_label, cpu_usage_label
		cpu_freq_label = ttk.Label(tab2, text="", anchor="nw", font=("Verdana", 8))
		cpu_freq_label.grid(column=1, row=5, padx=10, pady=3, sticky='NESW')

		cpu_usage_label = ttk.Label(tab2, text="", anchor="nw", font=("Verdana", 8))
		cpu_usage_label.grid(column=1, row=6, padx=10, pady=3, sticky='NESW')

		# Start the update loop
		update()	
 
	# Call this function after setting up the CPU tab (tab2)
	update_cpu_info(tab2)
  
 
 # Memory
	ttk.Label(tab3, text = MemoryTitleText, foreground="blue", font=("Verdana", 16, "bold")).grid(column = 0, 
							       row = 0, 
							       padx = 10, 
							       pady = 1,
                                   columnspan=2) 
 
	ttk.Label(tab3, text = TotalMemoryText, font=("Verdana", 8, "bold")).grid(column = 0, 
							       row = 1, 
							       padx = 10, 
							       pady = 1,
                                   sticky='NESW') 
 
	ttk.Label(tab3, text = memsize, anchor="nw", font=("Verdana", 8)).grid(column = 1, 
							       row = 1, 
							       padx = 10, 
							       pady = 1, 
                                   sticky='NESW')

	ttk.Label(tab3, text = UsedMemoryText, font=("Verdana", 8, "bold")).grid(column = 0, 
							       row = 2, 
							       padx = 10, 
							       pady = 1,
                                   sticky='NESW')
 
	ttk.Label(tab3, text = memused, anchor="nw", font=("Verdana", 8)).grid(column = 1, 
							       row = 2, 
							       padx = 10, 
							       pady = 1, 
                                   sticky='NESW')
 
	ttk.Label(tab3, text = FreeMemoryText, font=("Verdana", 8, "bold")).grid(column = 0, 
							       row = 3, 
							       padx = 10, 
							       pady = 1,
                                   sticky='NESW')
 
	ttk.Label(tab3, text = memfree, anchor="nw", font=("Verdana", 8)).grid(column = 1, 
							       row = 3, 
							       padx = 10, 
							       pady = 1, 
                                   sticky='NESW')

	ttk.Label(tab3, text = "", font=("Verdana", 8)).grid(column = 0, 
							       row = 4, 
							       padx = 10, 
							       pady = 1,
                                   sticky='NESW')

	ttk.Label(tab3, text = "", font=("Verdana", 8), anchor="nw").grid(column = 1, 
							       row = 5, 
							       padx = 10, 
							       pady = 1, 
                                   sticky='NESW')

	ttk.Label(tab3, text = SwapTitle, foreground="blue", font=("Verdana", 16, "bold")).grid(column = 0, 
							       row = 5, 
							       padx = 10, 
							       pady = 1,
                                   columnspan=2)

	ttk.Label(tab3, text = TotalSwapText, font=("Verdana", 8, "bold")).grid(column = 0, 
							       row = 6, 
							       padx = 10, 
							       pady = 1,
                                   sticky='NESW')
 
 
	ttk.Label(tab3, text = UsedSwapText, font=("Verdana", 8, "bold")).grid(column = 0, 
							       row = 7, 
							       padx = 10, 
							       pady = 1,
                                   sticky='NESW') # Used swap
 
 
	ttk.Label(tab3, text = FreeSwapText, font=("Verdana", 8, "bold")).grid(column = 0, 
							       row = 8, 
							       padx = 10, 
							       pady = 1,
                                   sticky='NESW') 
 
	
	ttk.Label(tab3, text = "").grid(column = 0, 
							       row = 9, 
							       padx = 10, 
							       pady = 1,
                                   sticky='NESW')

	ttk.Label(tab3, text = "").grid(column = 1, 
							       row = 9, 
							       padx = 10, 
							       pady = 1, 
                                   sticky='NESW')
	# After looking up the values we now make them update themselves every second
	def update_memory_info(tab3):
		def update():
			# Fetch current memory information
			mem = psutil.virtual_memory()
			swap = psutil.swap_memory()

			# Format memory and swap values
			
			mem_total = mem.total / (1024 * 1024 * 1024)
			memsize = f"{mem_total:.2f} GB".replace(',', ' ').replace('.', ',')

			mem_used = mem.used / (1024 * 1024 * 1024)
			memused = f"{mem_used:.2f} GB".replace(',', ' ').replace('.', ',')
			
			mem_free = mem.free / (1024 * 1024 * 1024)
			memfree = f"{mem_free:.2f} GB".replace(',', ' ').replace('.', ',')
	
			swap_total = swap.total / (1024 * 1024 * 1024)
			swaptotal = f"{swap_total:.2f} GB".replace(',', ' ').replace('.', ',')

			swap_used = swap.used / (1024 * 1024 * 1024)
			swapused = f"{swap_used:.2f} GB".replace(',', ' ').replace('.', ',')
			
			swap_free = swap.free / (1024 * 1024 * 1024)
			swapfree = f"{swap_free:.2f} GB".replace(',', ' ').replace('.', ',')

			# Update memory labels
			total_memory_label.config(text=memsize)
			used_memory_label.config(text=memused)
			free_memory_label.config(text=memfree)

			# Update swap labels
			total_swap_label.config(text=swaptotal)
			used_swap_label.config(text=swapused)
			free_swap_label.config(text=swapfree)

			# Schedule the next update
			Window.after(1000, update)  # Update every 1 second (1000 milliseconds)

		# Create labels for memory and swap information if they don't exist
		global total_memory_label, used_memory_label, free_memory_label
		global total_swap_label, used_swap_label, free_swap_label

		total_memory_label = ttk.Label(tab3, text="", anchor="nw", font=("Verdana", 8))
		total_memory_label.grid(column=1, row=1, padx=10, pady=1, sticky='NESW')

		used_memory_label = ttk.Label(tab3, text="", anchor="nw", font=("Verdana", 8))
		used_memory_label.grid(column=1, row=2, padx=10, pady=1, sticky='NESW')

		free_memory_label = ttk.Label(tab3, text="", anchor="nw", font=("Verdana", 8))
		free_memory_label.grid(column=1, row=3, padx=10, pady=1, sticky='NESW')

		total_swap_label = ttk.Label(tab3, text="", anchor="nw", font=("Verdana", 8))
		total_swap_label.grid(column=1, row=6, padx=10, pady=1, sticky='NESW')

		used_swap_label = ttk.Label(tab3, text="", anchor="nw", font=("Verdana", 8))
		used_swap_label.grid(column=1, row=7, padx=10, pady=1, sticky='NESW')

		free_swap_label = ttk.Label(tab3, text="", anchor="nw", font=("Verdana", 8))
		free_swap_label.grid(column=1, row=8, padx=10, pady=1, sticky='NESW')

    	# Start the update loop
		update()
    
    # Call the function
	update_memory_info(tab3)

  
 ########################
# Disk
	ttk.Label(tab4, 
    	text=DiskTitleText, foreground="blue", font=("Verdana", 16, "bold")).grid(column=0, 
                                row=0, 
                                padx=10, 
                                pady=3,
                                columnspan=5) 

	ttk.Label(tab4, 
    	text=DiskText, font=("Verdana", 8, "bold")).grid(column=0, 
                                row=1, 
                                padx=10, 
                                pady=3) 

	ttk.Label(tab4, 
    	text=DiskFStypeText, font=("Verdana", 8, "bold")).grid(column=1, 
                                row=1, 
                                padx=10, 
                                pady=3) 

	ttk.Label(tab4, 
    	text=TotalDiskSpaceText, font=("Verdana", 8, "bold")).grid(column=2, 
                                row=1, 
                                padx=10, 
                                pady=3) 

	ttk.Label(tab4, 
	    text=UsedDiskSpaceText, font=("Verdana", 8, "bold")).grid(column=3, 
                                row=1, 
                                padx=10, 
                                pady=3) 

	ttk.Label(tab4, 
    	text=FreeDiskSpaceText, font=("Verdana", 8, "bold")).grid(column=4, 
                                row=1, 
                                padx=10, 
                                pady=3, 
                                sticky='NESW') 

	ttk.Label(tab4, 
    	text=FreeDiskSpacePercentText, font=("Verdana", 8, "bold")).grid(column=5, 
                                row=1, 
                                padx=10, 
                                pady=3)

	# Dictionary to store disk labels for dynamic updates
	disk_labels = {}

	# Function to update disk information
	def update_disk_info(tab4):
		def update():
			# Fetch disk partitions
			partitions = disk_partitions()

        	# Update disk information for each partition
			for i, disk in enumerate(partitions):				
				disk_letter = disk.device.replace("\\", "/")
				clean_disk_letter = disk.device.replace("\\", "").replace(":", "")
            
				# Get disk usage
				hdd = psutil.disk_usage(disk_letter)
            
				# Format disk usage values
				hdd_total = hdd.total / (1024 * 1024 * 1024)
				hdd_used = hdd.used / (1024 * 1024 * 1024)
				hdd_free = hdd.free / (1024 * 1024 * 1024)
				hdd_percent = 100 - hdd.percent
            
				# Update labels for this disk
				if clean_disk_letter not in disk_labels:
					# Create labels for this disk if they don't exist
					disk_labels[clean_disk_letter] = {
						"total": ttk.Label(tab4, text="", anchor="ne", font=("Verdana", 8)),
                    	"used": ttk.Label(tab4, text="", anchor="ne", font=("Verdana", 8)),
                    	"free": ttk.Label(tab4, text="", anchor="ne", font=("Verdana", 8)),
                    	"percent": ttk.Label(tab4, text="", anchor="ne", font=("Verdana", 8))
                	}
                
					# Place labels in the grid
					disk_labels[clean_disk_letter]["total"].grid(column=2, row=i+2, padx=10, pady=3, sticky='NESW')
					disk_labels[clean_disk_letter]["used"].grid(column=3, row=i+2, padx=10, pady=3, sticky='NESW')
					disk_labels[clean_disk_letter]["free"].grid(column=4, row=i+2, padx=10, pady=3, sticky='NESW')
					disk_labels[clean_disk_letter]["percent"].grid(column=5, row=i+2, padx=10, pady=3, sticky='NESW')
            
				# Update label text
				disk_labels[clean_disk_letter]["total"].config(text=f"{hdd_total:.2f} GB".replace('.', ','))
				disk_labels[clean_disk_letter]["used"].config(text=f"{hdd_used:.2f} GB".replace('.', ','))
				disk_labels[clean_disk_letter]["free"].config(text=f"{hdd_free:.2f} GB".replace('.', ','))
				disk_labels[clean_disk_letter]["percent"].config(text=f"{hdd_percent:.2f} %".replace('.', ','))
        
			# Schedule the next update
			Window.after(1000, update)  # Update every 1 second (1000 milliseconds)
    
		# Start the update loop
		update()

	# Call the function to start updating disk information
	update_disk_info(tab4)

	# The first counter «i» goes through dhe disks and give a number for the row
	for i, disk in enumerate(disk_partitions()):
    	# Fetching the info here and not at the top because I need it to be inside
    	# a for-loop.
		str = disk.device
		DiskLetter = (str).replace("\\", "/")
		CleanDiskLetter = (str).replace("\\", "").replace(":", "")
    	# For each drive, we have to make the human readable values.
    	# Since this app is Norwegian, I change the decimal devider to comma.
		hdd = psutil.disk_usage(DiskLetter)
		
  		# Formatting the values for the disk(s)
		hdd_total = hdd.total / (1024 * 1024 * 1024)
		HddTotal = f"{hdd_total:.2f} GB".replace(',', ' ').replace('.', ',')
		
		hdd_free = hdd.free / (1024 * 1024 * 1024)
		HddFree = f"{hdd_free:.2f} GB".replace(',', ' ').replace('.', ',')
		
		hdd_used = hdd.used / (1024 * 1024 * 1024)
		HddUsed = f"{hdd_used:.2f} GB".replace(',', ' ').replace('.', ',')
  
		
		hdd_percent = hdd.percent
		HddPercent = f"{100-hdd_percent:.2f} %".replace(',', ' ').replace('.', ',')

		#checking the file system type
		FsType = disk.fstype
		
		ttk.Label(tab4, 
				text = CleanDiskLetter + ":").grid(column = 0, 
									row = i+2, 
									padx = 10, 
									pady = 3,
         							sticky='NESW') 
		ttk.Label(tab4, 
				text = FsType).grid(column = 1, 
									row = i+2, 
									padx = 10, 
									pady = 3,
         							sticky='NESW') 

		ttk.Label(tab4, 
				text = HddTotal, anchor="ne").grid(column = 2, 
									row = i+2, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW') 
		ttk.Label(tab4, 
				text = HddUsed, anchor="ne").grid(column = 3, 
									row = i+2, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW') 
		ttk.Label(tab4, 
				text = HddFree, anchor="ne").grid(column = 4, 
									row = i+2, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW') 
		ttk.Label(tab4, 
				text = HddPercent, anchor="ne").grid(column = 5, 
									row = i+2, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')
		
	
	wmi_obj_1 = wmi.WMI(namespace='root/Microsoft/Windows/Storage')
	# As «i» was used «j» is the offset from «i» to give some space for next listing
	j = i+3
	# And after «j», comes «k» that is used to place the health status of the disks
	# below the dqata about the disk
	k = j+1
	# Description line after one empty line
	ttk.Label(tab4, 
				text = "", anchor="nw").grid(column = 0, 
									row = i+4, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW', 
                					columnspan = 6)
	ttk.Label(tab4, 
				text = DiskIDText, font=("Verdana", 8, "bold")).grid(column = 0, 
									row = i+5, 
									padx = 10, 
									pady = 3)
	ttk.Label(tab4, 
				text = DiskModelText, font=("Verdana", 8, "bold"), anchor="nw").grid(column = 1, 
									row = i+5, 
									padx = 10, 
									pady = 3, 
         							columnspan = 2) 
	ttk.Label(tab4, 
				text = DiskBusTypeText, font=("Verdana", 8, "bold"), anchor="nw").grid(column = 3, 
									row = i+5, 
									padx = 10, 
									pady = 3) 
	ttk.Label(tab4, 
				text = MediaTypeText, font=("Verdana", 8, "bold"), anchor="nw").grid(column = 4, 
									row = i+5, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')
	ttk.Label(tab4, 
				text = FirmwareVersionText, font=("Verdana", 8, "bold"), anchor="nw").grid(column = 5, 
									row = i+5, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW') 
    
	for d in wmi_obj_1.MSFT_PhysicalDisk():
		MediaTypeName = [UnspecifiedText, "", "", HDDText, SSDText, SCMText]
		BusTypeName =[UnknownBusTypeText, SCSIText, ATAPText, ATAText, IEEE1394Text, SSAText, FibreChannelText, USBText, RAIDText, iSCSIText, SASText, SATAText, SDText, MMCText, MAXText, FileSupportedViritualText, StorageSpacesText, NVMEText, SCMText, UFSText, MSReservedText] 
		HealthStatusMeaning = [HealtStatusOKText, HealthStausWarningText, HealthStatusUnhealtyText, "", "", HealthStausUnknownText] 
		j = j + 1
		ttk.Label(tab4, 
				text = DiskIDText + d.DeviceID , anchor="nw", font=("Verdana", 8)).grid(column = 0, 
									row = i+j+2, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')
		ttk.Label(tab4, 
				text = d.Model, font=("Verdana", 8), anchor="nw").grid(column = 1, 
									row = i+j+2, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW', columnspan = 2)
		ttk.Label(tab4, 
				text = BusTypeName[d.BusType], font=("Verdana", 8), anchor="nw").grid(column = 3, 
									row = i+j+2, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')
		ttk.Label(tab4, 
				text = MediaTypeName[d.MediaType], font=("Verdana", 8), anchor="nw").grid(column = 4, 
									row = i+j+2, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW') 
		ttk.Label(tab4, 
				text = d.FirmwareVersion, anchor="nw", font=("Verdana", 8)).grid(column = 5, 
									row = i+j+2, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')
		ttk.Label(tab4, 
				text = DiskDeviceHelathStaus1Text + d.DeviceID + DiskDeviceHelathStaus2Text, font=("Verdana", 8, "bold"), anchor="nw").grid(column = 0, 
									row = i+j+k, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW', columnspan = 2)
		ttk.Label(tab4, 
				text = HealthStatusMeaning[d.HealthStatus], anchor="nw", font=("Verdana", 8)).grid(column = 2, 
									row = i+j+k, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW',
                					columnspan=3)
  
	# Operating system
	ttk.Label(tab5, 
			text = OperatingSystemTitleText, foreground="blue", font=("Verdana", 16, "bold")).grid(column = 0, 
									row = 0, 
									padx = 10, 
									pady = 3,
                					columnspan=2) 
	ttk.Label(tab5, 
			text = OperatingSystemText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 1, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW') 
	ttk.Label(tab5, 
			text = OSName, anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = 1, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW') 
	ttk.Label(tab5, 
			text = OSVersionText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 2, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW')
	ttk.Label(tab5, 
			text = OSVersion, anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = 2, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW') 
	ttk.Label(tab5, 
			text = ForMachineTypeText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 3, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW') # For machine type
	ttk.Label(tab5, 
			text = OSMachine, anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = 3, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')
	ttk.Label(tab5, 
			text = OSLanguageText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 4, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW') # For machine type
	ttk.Label(tab5, 
			text = loc[0], anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = 4, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')  
	ttk.Label(tab5, 
			text = OSCodePageText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 5, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW') # For machine type
	ttk.Label(tab5, 
			text = enc, anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = 5, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW') 
   
    ###############
    # Graphics page
    
    # Run a PowerShell command and capture the output
	command = '''
				powershell -WindowStyle Hidden -Command "Get-CimInstance Win32_VideoController | 
				Select-Object Name, AdapterRAM, VideoModeDescription, CurrentNumberOfColors, PNPDeviceID, CurrentBitsPerPixel | 
				ConvertTo-Csv -NoTypeInformation"
				'''
	# Importing modules that's needed
	import csv
	from io import StringIO

	# Using popen her as it was needed to supress console popping up for a second
	# when starting the compiled program, that was compiled with pyinstaller.
	process = subprocess.Popen(['powershell', '-WindowStyle', 'Hidden', '-Command', command], 
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                             creationflags=subprocess.CREATE_NO_WINDOW)
	output, error = process.communicate()

	# Decode the output
	output = output.decode('utf-8')

	# Now use the decoded string with StringIO
	reader = csv.reader(StringIO(output))

    # Parse the CSV data get the corrct module for it.
	from io import StringIO

    # Use csv.reader to parse the CSV data
	reader = csv.reader(StringIO(output))
	next(reader)  # Skip the header row

    # Loop through each video card
	counter = 0
	morecards = 0
	for row in reader:
		if len(row) == 6:  # Ensure we have all 6 columns
			name = row[0]
			adapter_ram = int(row[1]) if row[1] else 0 # Showing zero if empty
			video_mode = row[2]
			current_colors = int(row[3]) if row[3] else 0 # Showing zero if empty
			pnp_device_id = row[4]
			bits_per_pixel = int(row[5]) if row[5] else 0 # Showing zero if empty

            # Convert RAM to GB and format numbers to fit Norwegian number formatting.
			ram_gb = adapter_ram / (1024 ** 3)  # Convert bytes to GB
			formatted_ram_gb = f"{ram_gb:,.2f}".replace(",", " ").replace(".", ",")
			formatted_colors = f"{current_colors:,}".replace(",", " ") # There will be no decimals here
			
			# Displaying what we've found
			ttk.Label(tab6, 
				text = GraphicCardNumberText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = counter + morecards, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW') 
			ttk.Label(tab6, 
				text = counter + 1, anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = counter + morecards, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')
			ttk.Label(tab6, 
				text = GraphicCardNameText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = counter + morecards + 1, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW') 
			ttk.Label(tab6, 
				text = name, anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = counter + morecards + 1, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')
			ttk.Label(tab6, 
				text = GraphicCardRAMText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = counter + morecards + 2, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW') 
			ttk.Label(tab6, 
				text = f"{formatted_ram_gb} GB", anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = counter + morecards + 2, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')
			ttk.Label(tab6, 
				text = GraphicCardVideoModeText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = counter + morecards + 3, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW') 
			ttk.Label(tab6, 
				text = GraphicCardVideoModeText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = counter + morecards + 3, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW')
			
			# If the card has no video modes the line will stay empty
			# In some mechines (like mine), There is a grphics card and a GPU
			# Then the graphics card will handle the video mode.
			if video_mode == "":
				video_mode = NoneText
    
			ttk.Label(tab6, 
				text = video_mode, anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = counter + morecards + 3, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')
			ttk.Label(tab6, 
				text = GraphicCardColorsText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = counter + morecards + 4, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW') 
			ttk.Label(tab6, 
				text = formatted_colors, anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = counter + morecards + 4, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')
			ttk.Label(tab6, 
				text = GraphicCardPNPDeviceIDText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = counter + morecards + 5, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW') 
			ttk.Label(tab6, 
				text = pnp_device_id, anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = counter + morecards + 5, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')
			ttk.Label(tab6, 
				text = GraphicCardBitsPerPixelText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = counter + morecards + 6, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW') 
			ttk.Label(tab6, 
				text = bits_per_pixel, anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = counter + morecards + 6, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')
			
			# Separator line
			ttk.Label(tab6, 
				text = " ", anchor="center", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = counter + morecards + 7, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW', columnspan=2) 
			# Counters for placement of the grid
			counter = counter + 1
			morecards = counter + 7

#################
# Screen

    # Set a tolerance for finding the closest ratio for the screen ratio
	ratio_tolerance = 0.01

	# Get the list of monitors
	monitors = get_monitors()

	# Iterate through each monitor and print its details
	for m in monitors:
		# Access individual values using the dictionary keys
		s_x = m.x
		s_y = m.y
		s_width = float(m.width)
		s_height = float(m.height)
		s_name = m.name
		s_primary = m.is_primary
		s_width_mm = m.width_mm
		s_height_mm = m.height_mm
		
		# Starting to get aspect ratio
		aspect_ratio = s_width / s_height
     # Find the closest whole number ratio
	best_width_ratio = 0
	best_height_ratio = 0
	best_difference = float('inf')

	def gcd(a, b):
		"""Calculates the greatest common divisor (GCD) of two numbers."""
		while b:
			a, b = b, a % b
		return a

    # Find the closest whole number ratio
	best_width_ratio = 0
	best_height_ratio = 0
	best_difference = float('inf')

    # Start with a smaller range
	max_ratio = 10

	found_ratio = False
	while not found_ratio:
		for width_ratio in range(1, max_ratio + 1):
			for height_ratio in range(1, max_ratio + 1):
				test_ratio = width_ratio / height_ratio
				difference = abs(aspect_ratio - test_ratio)

                # Check if the difference is within the tolerance
				if difference < best_difference and difference <= ratio_tolerance:
					best_width_ratio = width_ratio
					best_height_ratio = height_ratio
					best_difference = difference
					found_ratio = True
                    # Break out of all loops
					break 

        # If no ratio is found, increase the range
		if not found_ratio:
			max_ratio += 5

    # Handle the case where no ratio is found
	if best_width_ratio == 0 and best_height_ratio == 0:
		print(f"Unable to find a suitable aspect ratio for the monitor.")
	else:
        # Find the GCD to simplify the ratio
		common_divisor = gcd(best_width_ratio, best_height_ratio)
		simplified_width_ratio = best_width_ratio // common_divisor
		simplified_height_ratio = best_height_ratio // common_divisor


	ttk.Label(tab7, 
        	text = ScreenTitleText, foreground="blue", font=("Verdana", 16, "bold")).grid(column = 0, 
									row = 0, 
									padx = 10, 
									pady = 3,	
         						#	sticky='NESW',
                					columnspan=2)	

	# Setting counters
	s_counter = 0
	S_morescreens  = 6
	for m in monitors:
		ttk.Label(tab7, 
				text = ScreenNameText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = s_counter + S_morescreens + 1, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW') 
		ttk.Label(tab7, 
				text = s_name, anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = s_counter + S_morescreens + 1, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW', 
                					columnspan=2)
    
		ttk.Label(tab7, 
				text = ScreenResText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = s_counter + S_morescreens + 2, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW') 
		ttk.Label(tab7, 
				text = f"{s_width:,.0f} x {s_height:,.0f}", anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = s_counter + S_morescreens + 2, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')  
		ttk.Label(tab7, 
				text = PxText, anchor="nw", font=("Verdana", 8)).grid(column = 2, 
									row = s_counter + S_morescreens + 2, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')
		ttk.Label(tab7, 
				text = ScreenSizeText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = s_counter + S_morescreens + 3, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW') 
		ttk.Label(tab7, 
				text = f"{s_width_mm} x {s_height_mm}", anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = s_counter + S_morescreens + 3, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')   
		ttk.Label(tab7, 
				text = MmText, anchor="nw", font=("Verdana", 8)).grid(column = 2, 
									row = s_counter + S_morescreens + 3, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')   
    
		ttk.Label(tab7, 
				text = ScreenRatioText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = s_counter + S_morescreens + 4, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW') 
		ttk.Label(tab7, 
				text = f"{simplified_width_ratio}:{simplified_height_ratio}", anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = s_counter + S_morescreens + 4, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW', 
                					columnspan=2) 
    
		
		if s_primary:
			s_primary = YesText
		else:
			s_primary = NoText
  
		ttk.Label(tab7, 
				text = ScreenPrimaryText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = s_counter + S_morescreens + 5, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW') 
		ttk.Label(tab7, 
				text = s_primary, anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = s_counter + S_morescreens + 5, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW',
                					columnspan=2) 
    
    
    
		# Increasing the counters
		s_counter = s_counter + 1
		S_morescreens = s_counter + 6
  
#############
# About the PC

	
	# Putting the info into variables
	pc_manufacturer = my_system.Manufacturer
	pc_model = my_system. Model
	pc_name = my_system.Name
	pc_system_type = my_system.SystemType
	pc_sys_family = my_system.SystemFamily
	pc_processors = my_system.NumberOfProcessors
	pc_log_processors = my_system.NumberOfLogicalProcessors
	pc_cur_user = my_system.UserName
	
	
	ttk.Label(tab8, 
        	text = PCTitleText, foreground="blue", font=("Verdana", 16, "bold")).grid(column = 0, 
									row = 0, 
									padx = 10, 
									pady = 3,	
         						#	sticky='NESW',
                					columnspan=2)	
 
	ttk.Label(tab8, 
			text = PCManufacturerText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 1, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW') # For machine type
	ttk.Label(tab8, 
			text = pc_manufacturer, anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = 1, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW') 

	ttk.Label(tab8, 
			text = PCModelText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 2, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW') # For machine type
	ttk.Label(tab8, 
			text = pc_model, anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = 2, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW') 
	ttk.Label(tab8, 
			text = PCNameText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 3, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW') # For machine type
	ttk.Label(tab8, 
			text = pc_name, anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = 3, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW') 
	ttk.Label(tab8, 
			text = PCSysTypeText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 4, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW') # For machine type
	ttk.Label(tab8, 
			text = pc_system_type, anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = 4, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')
	ttk.Label(tab8, 
			text = PCSysFamilyText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 5, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW') # For machine type
	ttk.Label(tab8, 
			text = pc_sys_family, anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = 5, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')
	ttk.Label(tab8, 
			text = PCSysNumProcText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 6, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW') # For machine type
	ttk.Label(tab8, 
			text = pc_processors, anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = 6, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')
   
	tk.Label(tab8, 
			text = PCSysNumLogProcText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 7, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW') # For machine type
	ttk.Label(tab8, 
			text = pc_log_processors, anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = 7, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')

	tk.Label(tab8, 
			text = PCCurUserText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 8, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW') # For machine type
	ttk.Label(tab8, 
			text = pc_cur_user, anchor="nw", font=("Verdana", 8)).grid(column = 1, 
									row = 8, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')




  
#############
# About 
	ttk.Label(tab9, 
		text ="MiniInfo\n", foreground="blue", font=("Verdana", 16, "bold")).grid(column = 0, 
									row = 0, 
									padx = 10, 
									pady = 3,	
         						#	sticky='NESW',
                					columnspan=2)
	ttk.Label(tab9, 
		text = CopyleftText, font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 1, 
									padx = 10, 
									pady = 3,	
         							#sticky='NESW',
                					columnspan=2) 
	ttk.Label(tab9, 
		text = LicenseText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 2, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')
	ttk.Label(tab9, 
		text = LicenseTypeText, anchor="nw").grid(column = 1, 
									row = 2, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW') 
	ttk.Label(tab9, 
		text = VersionText, anchor="nw", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 3, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW') 
	
	def open_url(event):
		webbrowser.open("https://prog.nalle.no")

	
	StaticLabel = ttk.Label(tab9, text = SourceCodeText, font=("Verdana", 8))
	StaticLabel.grid(column = 0, 
									row = 4, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')

	URLLabel = ttk.Label(tab9, text="https://prog.nalle.no", font=("Verdana", 8), foreground="Blue", cursor="Hand2")
	URLLabel.grid(column=1, row=4, padx=10, pady=3, sticky='NESW', columnspan=2)
	URLLabel.bind("<Button-1>", open_url)

	ttk.Label(tab9, 
		text = AppVersion, font=("Verdana", 8), anchor="nw").grid(column = 1, 
									row = 3, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW') 

	Window.mainloop() 

if __name__ == "__main__":
    main()
