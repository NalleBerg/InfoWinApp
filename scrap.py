import wmi

c = wmi.WMI()
my_system = c.Win32_ComputerSystem()[0]

print(f"Manufacturer: {my_system.Manufacturer}") #OK
print(f"Model: {my_system.Model}") # OK
print(f"Number of Logical Processors: {my_system.NumberOfLogicalProcessors}")
print(f"Number of Physical Processors: {my_system.NumberOfProcessors}")
print(f"System Type: {my_system.SystemType}")
print(f"User Name: {my_system.UserName}")
print(f"Domain: {}")
print(f"Workgroup: {my_system.Workgroup}")
print(f"Status: {my_system.Status}")
print(f"SystemFamily: {my_system.SystemFamily}")