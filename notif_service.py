#this code will supervise the water tank level and will send warnings through Telegram
#developed by Ing. Jorge Morales, MBA.
#Control and Automation Engineering Department

from asyncio.proactor_events import _ProactorBaseWritePipeTransport
from math import trunc
import os
import sys
import subprocess
import time
import os
from dotenv import load_dotenv
import sys
import time
from urllib.parse import quote
from urllib.request import Request, urlopen
import json
from datetime import date
#get the info

load_dotenv()
JorgeMorales = os.getenv('JorgeMorales')
Grupo_WT = os.getenv('JorgeMorales')
AngelI = os.getenv('AngelI')
token_bot = os.getenv('api_token')


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

#---------------------Telegram messaging services---------------------------------------#

def send_message(user_id, text,token):
	global json_respuesta
	url = f"https://api.telegram.org/{token}/sendMessage?chat_id={user_id}&text={text}"
	#resp = requests.get(url)
	#hacemos la petición
	try:
		respuesta  = urlopen(Request(url))
	except Exception as e:
		print(f"Ha ocurrido un error al enviar el mensaje: {e}")
	else:
		#recibimos la información
		cuerpo_respuesta = respuesta.read()
		# Procesamos la respuesta json
		json_respuesta = json.loads(cuerpo_respuesta.decode("utf-8"))
		print("mensaje enviado exitosamente")

#---------------------Telegram messaging services---------------------------------------#






################## end of the auxiliary functions
#steps
	#convert from HST to TXT
	#recover the file using the filepath
	#

mis_docs = My_Documents(5)
last_line = ""
past_WT = 0
control_number = 0
delta_WT = 0

def retrieveWT():
	today = date.today()
	
	#get the file
	#the name of the file
	d1 = today.strftime("%d")
	m1 = today.strftime("%m")
	a1 = today.strftime("%y")
	hst_name = f"18{a1}{m1}{d1}.hst"
	txt_name = f"18{a1}{m1}{d1}.txt"
	ruta = str(mis_docs)+ str(r'\\InduSoft Web Studio v7.1 Projects\SCADA_MubeaCSMx\Hst') + "\\" + hst_name
	subprocess.call([resource_path(r"images/HST2TXT.exe"), ruta])
	time.sleep(5)
	ruta2 = str(mis_docs)+ str(r'\\InduSoft Web Studio v7.1 Projects\SCADA_MubeaCSMx\Hst')+ "\\" + txt_name
	file_exists = os.path.exists(ruta2)

	if file_exists:
		#if the file exists, then open and read it.
		with open(ruta2, 'rb') as f:
			try:  # catch OSError in case of a one line file 
				f.seek(-2, os.SEEK_END)
				while f.read(1) != b'\n':
					f.seek(-2, os.SEEK_CUR)
			except OSError:
				f.seek(0)
			raw_data = f.readline().decode()
			process1 = raw_data.replace("\t"," ")
			process2 = process1.replace("\r\n","")
			process3 = process2.replace(".000","")
			fecha = process3[0:10]
			hora = process3[11:16]
			nivel = int(process3[-3:])
			print(f"Nivel de agua en {nivel} cm. Ultima actualización: {fecha} a las {hora}")
			return fecha,hora,nivel
	else:
		print(f"no se encontró el archivo {txt_name}")
		last_line = None
		return last_line


def low_level_warning(level):
	send_message(Grupo_WT,quote(f"Advertencia de nivel bajo de cisterna: Nivel en {level}"),token_bot)
	return
def regular_updates(fecha,hora,nivel):
	send_message(Grupo_WT,quote(f"Nivel de agua en {nivel} cm. Ultima actualización: {fecha} a las {hora}"),token_bot)
	return

def delta_warning(delta_WT,past_level,actual_level):
	min_left = actual_level/((past_level-actual_level)/20)
	print(f"Nivel de cisterna en {actual_level}. Ha caido {delta_WT} cm en 20 minutos, se estiman { round(min_left/60,1)} hrs restantes hasta vacío")
	send_message(Grupo_WT,quote(f"Nivel de cisterna en {actual_level}. Ha caido {delta_WT} cm en 20 minutos, se estiman { round(min_left/60,1)} hrs restantes hasta vacío"),token_bot)
	return

while True:
	control_number += 1
	print(control_number)
	#recover the last number:
	actual_WT = retrieveWT()
	if actual_WT == None:
		sys.exit()
	
	#If first run, fill the past_WT var with the actual value, this will serve to find the level slope
	if past_WT == 0:
		past_WT = actual_WT[2]
	else:
		delta_WT =  actual_WT[2] - past_WT
	#here is the part where we compare values to exercise critical actions
	if actual_WT[2] < 100 or delta_WT <=-4:
		#call critical function
		delta_warning(delta_WT,past_WT,actual_WT[2])
		past_WT = actual_WT[2]
		#when a low level warning is issued, wait 20 minutes before sending another warning message
		time.sleep(1)
		continue
	#Regular updates every 3 hours.
	if(control_number % 9 == 0):
		regular_updates(actual_WT[0],actual_WT[1],actual_WT[2])
		past_WT = actual_WT[2]
		time.sleep(1)
		continue
	time.sleep(1)