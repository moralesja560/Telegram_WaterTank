import datetime
import subprocess
import os
import sys
import time


x = datetime.datetime(2021, 9, 20)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def My_Documents(location):
	import ctypes.wintypes
		#####-----This section discovers My Documents default path --------
		#### loop the "location" variable to find many paths, including AppData and ProgramFiles
	CSIDL_PERSONAL = location       # My Documents
	SHGFP_TYPE_CURRENT = 0   # Get current, not default value
	buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
	ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
	#####-------- please use buf.value to store the data in a variable ------- #####
	#add the text filename at the end of the path
	temp_docs = buf.value
	return temp_docs

mis_docs = My_Documents(5)


def decode(hst_name):
	ruta = str(mis_docs)+ str(r'\\SC_Repo\\DataWT') + "\\" + hst_name
	subprocess.call([resource_path(r"images/HST2TXT.exe"), ruta])
	time.sleep(5)



for  i in range(0,264):
	#HST name structure:
	d1 =x.strftime("%d")
	m1 = x.strftime("%m")
	a1 = x.strftime("%y")
	hst_name = f"18{a1}{m1}{d1}.hst"
	print(hst_name)
	decode(hst_name)
	x = x + datetime.timedelta(days=1)