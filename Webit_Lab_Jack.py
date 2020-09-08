import tkinter as tk
from tkinter import ttk, Spinbox,Scrollbar
from labjack import ljm
from matplotlib import pyplot as plt
from matplotlib import style

class Webit_GUI(tk.Frame):

	def __init__(self, master):
		# Initializes the frame
		tk.Frame.__init__(self, master)

		WRITE = ljm.constants.WRITE
		READ = ljm.constants.READ
		FLOAT32 = ljm.constants.FLOAT32
		UINT16 = ljm.constants.UINT16
		UINT32 = ljm.constants.UINT32

		ConnectButton = tk.Button(
			self.master, text = 'Connect', command=self.Connect)
		ConnectButton.grid(row=0, column=0)

		disconnectButton = tk.Button(
			self.master, text = 'Disconnect', command=self.Disconnect)
		disconnectButton.grid(row=0, column=1)
	
		QuitButton = tk.Button(
			master,
			text = 'Quit',
			command=master.quit,
			width=15
		)
		QuitButton.grid(row=6, column=4)


	def Connect(self):
		self.handle = ljm.openS("T7", "ANY", "ANY")  # T7 device, Any connection, Any identifier
		
	def Disconnect(self):
		ljm.close(self.handle)

	def Get_Info(self):
		info = ljm.getHandleInfo(self.handle)
		print("Opened a LabJack with Device type: %i, Connection type: %i,\n"
			"Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
			(info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))


if __name__ == "__main__":
	root = tk.Tk()
	root.title("WEBIT LabJack GUI")
	app = Webit_GUI(root)
	app.mainloop()

#There are two DACs (digital-to-analog converters, also known as analog outputs) on T-series devices. Each DAC can be set to a voltage between about 0 and 5 volts with 10 bits of resolution (T4) or 12 bits of resolution (T7).
#To set DAC output voltage, write to the following registers:
# Expanded Names	Addresses
# DAC0, DAC1	1000, 1002

#The LabJack T7 has 14 built-in analog inputs, readable as AIN0-13:

# Expanded Names	Addresses
# AIN0, AIN1, AIN2, Show All	0, 2, 4, Show All
