# Copyleft Nalle Berg 2025
# License GPL V2
AppVersion = '0.5.0'

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
exec(open(resource_path("EN_uk_lang"), encoding="utf-8").read())

def main():
    
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
	ICO = tk.PhotoImage(file=(resource_path("NSB-2021.PNG"))) 
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
	

	tabControl.add(tab1, text = Tab1Text) 
	tabControl.add(tab2, text = Tab2Text) 
	tabControl.add(tab3, text = Tab3Text) 
	tabControl.add(tab4, text = Tab4Text)
	tabControl.add(tab5, text = Tab5Text)
	tabControl.add(tab6, text = Tab6Text)
	

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
		text = ActiveCardText, anchor="w", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 1, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW') 
	# If there is no net
	if not OnNetWork:
		ActiveNetCard = NoActiveCardText 
	ttk.Label(tab1, 
		text = ActiveNetCard+"\n ", anchor="w").grid(column = 1, 
									row = 1, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW') 
  
	
	ttk.Label(tab1, 
		text = MachineNetNameText, anchor="w", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 2, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW') 
	# If no network
	if not OnNetWork:
		hostname = NoActiveCardText 
	
	ttk.Label(tab1, 
		text = hostname+"\n ", anchor="w", font=("Verdana", 8)).grid(column = 1, 
									row = 2, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW')
	
	ttk.Label(tab1, 
		text = LocalIPv4Text , anchor="w", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 3, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW')
	# If no network
	if not OnNetWork:
		LocalIPv4 = NoActiveCardText
  
	ttk.Label(tab1, 
		text = LocalIPv4+"\n ", anchor="w", font=("Verdana", 8)).grid(column = 1, 
									row = 3, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW')
	# Local IP address V6
	ttk.Label(tab1, 
		text = LocalIPv6Text , anchor="w", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 4, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW') 
	# If no network
	if not OnNetWork:
		LocalIPv6 = NoActiveCardText

	ttk.Label(tab1, 
		text = LocalIPv6+"\n ", anchor="w", font=("Verdana", 8)).grid(column = 1, 
									row = 4, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW')
	
	ttk.Label(tab1, 
		text = ExtIPv4Text, anchor="w", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 5, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW') 
	# If no Internet
	if not OnInternet:
		external_ip_v4 = NotOnInternetText
  
	ttk.Label(tab1, 
		text = external_ip_v4+"\n ", anchor="w", font=("Verdana", 8)).grid(column = 1, 
									row = 5, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW') 
	ttk.Label(tab1, 
		text = ExtIPv6Text, anchor="w", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 6, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW')
	# If no Internet
	if not OnInternet:
		external_ip_v6 = NotOnInternetText
  
	ttk.Label(tab1, 
		text = external_ip_v6+"\n ", anchor="w", font=("Verdana", 8)).grid(column = 1, 
									row = 6, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW') 
	ttk.Label(tab1, 
		text = StdGWv4Text, anchor="w", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 7, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW') 
  
	if not OnNetWork:
		DefGWv4 = NoActiveCardText

	ttk.Label(tab1, 
		text =DefGWv4+"\n ", anchor="w", font=("Verdana", 8)).grid(column = 1, 
									row = 7, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW') 
	ttk.Label(tab1, 
		text = StdGWv6Text, anchor="w", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 8, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW')  
	if not OnNetWork:
		DefGWv6 = NoActiveCardText
  
	ttk.Label(tab1, 
		text = DefGWv6+"\n ", anchor="w", font=("Verdana", 8)).grid(column = 1, 
									row = 8, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW') 
	ttk.Label(tab1, 
		text = MacAddrText, anchor="w", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 9, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW')

	if not OnNetWork:
		MacAddr = NoActiveCardText
 
	ttk.Label(tab1, 
		text = MacAddr+"\n ", anchor="w").grid(column = 1, 
									row = 9, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW') 




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
		text = CPUProc, anchor="w", font=("Verdana", 8)).grid(column = 1, 
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
		text = psutil.cpu_count(logical=False), anchor="w", font=("Verdana", 8)).grid(column = 1, 
									row = 2, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW')
	ttk.Label(tab2, 
		text = PiecesText, anchor="w", font=("Verdana", 8)).grid(column = 2, 
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
		text = psutil.cpu_count(logical=True), anchor="w", font=("Verdana", 8)).grid(column = 1, 
									row = 3, 
									padx = 10, 
									pady = 1,
                                    sticky='NESW')
	ttk.Label(tab2, 
		text = PiecesText, anchor="w", font=("Verdana", 8)).grid(column = 2, 
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
		text = f"{cpufreq.max:.2f}", anchor="w", font=("Verdana", 8)).grid(column = 1, 
									row = 4, 
									padx = 10, 
									pady = 3,
                                    sticky='NESW')
	ttk.Label(tab2, 
		text = MhzText, anchor="w", font=("Verdana", 8)).grid(column = 2, 
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
		text = MhzText, anchor="w", font=("Verdana", 8)).grid(column = 2, 
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
		text = "%", anchor="w", font=("Verdana", 8)).grid(column = 2, 
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
			cpu_usage_label.config(text=f"{cpu_usage} %")

			# Schedule the next update
			Window.after(1000, update)  # Update every 1 second (1000 milliseconds)

		# Create labels for CPU frequency and usage if they don't exist
		global cpu_freq_label, cpu_usage_label
		cpu_freq_label = ttk.Label(tab2, text="", anchor="w", font=("Verdana", 8))
		cpu_freq_label.grid(column=1, row=5, padx=10, pady=3, sticky='NESW')

		cpu_usage_label = ttk.Label(tab2, text="", anchor="w", font=("Verdana", 8))
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
 
	ttk.Label(tab3, text = memsize, anchor="w", font=("Verdana", 8)).grid(column = 1, 
							       row = 1, 
							       padx = 10, 
							       pady = 1, 
                                   sticky='NESW')

	ttk.Label(tab3, text = UsedMemoryText, font=("Verdana", 8, "bold")).grid(column = 0, 
							       row = 2, 
							       padx = 10, 
							       pady = 1,
                                   sticky='NESW')
 
	ttk.Label(tab3, text = memused, anchor="w", font=("Verdana", 8)).grid(column = 1, 
							       row = 2, 
							       padx = 10, 
							       pady = 1, 
                                   sticky='NESW')
 
	ttk.Label(tab3, text = FreeMemoryText, font=("Verdana", 8, "bold")).grid(column = 0, 
							       row = 3, 
							       padx = 10, 
							       pady = 1,
                                   sticky='NESW')
 
	ttk.Label(tab3, text = memfree, anchor="w", font=("Verdana", 8)).grid(column = 1, 
							       row = 3, 
							       padx = 10, 
							       pady = 1, 
                                   sticky='NESW')

	ttk.Label(tab3, text = "", font=("Verdana", 8)).grid(column = 0, 
							       row = 4, 
							       padx = 10, 
							       pady = 1,
                                   sticky='NESW')

	ttk.Label(tab3, text = "", font=("Verdana", 8), anchor="w").grid(column = 1, 
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

		total_memory_label = ttk.Label(tab3, text="", anchor="w", font=("Verdana", 8))
		total_memory_label.grid(column=1, row=1, padx=10, pady=1, sticky='NESW')

		used_memory_label = ttk.Label(tab3, text="", anchor="w", font=("Verdana", 8))
		used_memory_label.grid(column=1, row=2, padx=10, pady=1, sticky='NESW')

		free_memory_label = ttk.Label(tab3, text="", anchor="w", font=("Verdana", 8))
		free_memory_label.grid(column=1, row=3, padx=10, pady=1, sticky='NESW')

		total_swap_label = ttk.Label(tab3, text="", anchor="w", font=("Verdana", 8))
		total_swap_label.grid(column=1, row=6, padx=10, pady=1, sticky='NESW')

		used_swap_label = ttk.Label(tab3, text="", anchor="w", font=("Verdana", 8))
		used_swap_label.grid(column=1, row=7, padx=10, pady=1, sticky='NESW')

		free_swap_label = ttk.Label(tab3, text="", anchor="w", font=("Verdana", 8))
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
						"total": ttk.Label(tab4, text="", anchor="e", font=("Verdana", 8)),
                    	"used": ttk.Label(tab4, text="", anchor="e", font=("Verdana", 8)),
                    	"free": ttk.Label(tab4, text="", anchor="e", font=("Verdana", 8)),
                    	"percent": ttk.Label(tab4, text="", anchor="e", font=("Verdana", 8))
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
				text = HddTotal, anchor="e").grid(column = 2, 
									row = i+2, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW') 
		ttk.Label(tab4, 
				text = HddUsed, anchor="e").grid(column = 3, 
									row = i+2, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW') 
		ttk.Label(tab4, 
				text = HddFree, anchor="e").grid(column = 4, 
									row = i+2, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW') 
		ttk.Label(tab4, 
				text = HddPercent, anchor="e").grid(column = 5, 
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
				text = "", anchor="w").grid(column = 0, 
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
				text = DiskModelText, font=("Verdana", 8, "bold"), anchor="w").grid(column = 1, 
									row = i+5, 
									padx = 10, 
									pady = 3, 
         							columnspan = 2) 
	ttk.Label(tab4, 
				text = DiskBusTypeText, font=("Verdana", 8, "bold"), anchor="w").grid(column = 3, 
									row = i+5, 
									padx = 10, 
									pady = 3) 
	ttk.Label(tab4, 
				text = MediaTypeText, font=("Verdana", 8, "bold"), anchor="w").grid(column = 4, 
									row = i+5, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')
	ttk.Label(tab4, 
				text = FirmwareVersionText, font=("Verdana", 8, "bold"), anchor="w").grid(column = 5, 
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
				text = DiskIDText + d.DeviceID , anchor="w", font=("Verdana", 8)).grid(column = 0, 
									row = i+j+2, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')
		ttk.Label(tab4, 
				text = d.Model, font=("Verdana", 8), anchor="w").grid(column = 1, 
									row = i+j+2, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW', columnspan = 2)
		ttk.Label(tab4, 
				text = BusTypeName[d.BusType], font=("Verdana", 8), anchor="w").grid(column = 3, 
									row = i+j+2, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')
		ttk.Label(tab4, 
				text = MediaTypeName[d.MediaType], font=("Verdana", 8), anchor="w").grid(column = 4, 
									row = i+j+2, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW') 
		ttk.Label(tab4, 
				text = d.FirmwareVersion, anchor="w", font=("Verdana", 8)).grid(column = 5, 
									row = i+j+2, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')
		ttk.Label(tab4, 
				text = DiskDeviceHelathStaus1Text + d.DeviceID + DiskDeviceHelathStaus2Text, font=("Verdana", 8, "bold"), anchor="w").grid(column = 0, 
									row = i+j+k, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW', columnspan = 2)
		ttk.Label(tab4, 
				text = HealthStatusMeaning[d.HealthStatus], anchor="w", font=("Verdana", 8)).grid(column = 2, 
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
			text = OperatingSystemText, anchor="w", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 1, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW') 
	ttk.Label(tab5, 
			text = OSName, anchor="w", font=("Verdana", 8)).grid(column = 1, 
									row = 1, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW') 
	ttk.Label(tab5, 
			text = OSVersionText, anchor="w", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 2, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW')
	ttk.Label(tab5, 
			text = OSVersion, anchor="w", font=("Verdana", 8)).grid(column = 1, 
									row = 2, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW') 
	ttk.Label(tab5, 
			text = ForMachineTypeText, anchor="w", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 3, 
									padx = 10, 	
									pady = 3,	
         							sticky='NESW') # For machine type
	ttk.Label(tab5, 
			text = OSMachine, anchor="w", font=("Verdana", 8)).grid(column = 1, 
									row = 3, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')
	ttk.Label(tab5, 
			text = OSLanguageText, anchor="w", font=("Verdana", 8, "bold")).grid(column = 0, 
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
			text = OSCodePageText, anchor="w", font=("Verdana", 8, "bold")).grid(column = 0, 
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
   


	# About 
	ttk.Label(tab6, 
		text ="MiniInfo\n", foreground="blue", font=("Verdana", 16, "bold")).grid(column = 0, 
									row = 0, 
									padx = 10, 
									pady = 3,	
         						#	sticky='NESW',
                					columnspan=2)
	ttk.Label(tab6, 
		text = CopyleftText, font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 1, 
									padx = 10, 
									pady = 3,	
         							#sticky='NESW',
                					columnspan=2) 
	ttk.Label(tab6, 
		text = LicenseText, anchor="w", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 2, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')
	ttk.Label(tab6, 
		text = LicenseTypeText, anchor="w").grid(column = 1, 
									row = 2, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW') 
	ttk.Label(tab6, 
		text = VersionText, anchor="w", font=("Verdana", 8, "bold")).grid(column = 0, 
									row = 3, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW') 
	
	def open_url(event):
		webbrowser.open("https://prog.nalle.no")

	
	StaticLabel = ttk.Label(tab6, text = SourceCodeText)
	StaticLabel.grid(column = 0, 
									row = 4, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW')

	URLLabel = ttk.Label(tab6, text="https://prog.nalle.no", foreground="Blue", cursor="Hand2")
	URLLabel.grid(column=1, row=4, padx=10, pady=3, sticky='NESW', columnspan=2)
	URLLabel.bind("<Button-1>", open_url)

	ttk.Label(tab6, 
		text = AppVersion, anchor="w").grid(column = 1, 
									row = 3, 
									padx = 10, 
									pady = 3,	
         							sticky='NESW') 

	Window.mainloop() 

if __name__ == "__main__":
    main()
