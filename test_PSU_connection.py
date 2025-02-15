# import pyvisa

# # rm = pyvisa.ResourceManager('@py')
# # psu = rm.open_resource('/dev/usbtmc0')  # Explicitly use PyVISA-py



import pyvisa

rm = pyvisa.ResourceManager()
print(rm.list_resources())


# import pyvisa
# rm = pyvisa.ResourceManager()
# psu = rm.open_resource('/dev/usbtmc0')
# print(psu.query('*IDN?'))