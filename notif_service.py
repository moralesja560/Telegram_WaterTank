#this code will supervise the water tank level and will send warnings through Telegram
#developed by Ing. Jorge Morales, MBA.
#Control and Automation Engineering Department

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
control_number = 1

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
	send_message(Grupo_WT,quote(f"Notificación de nivel crítico de cisterna: Nivel en {level}"),token_bot)
	return


while True:
	control_number += 1
	print(control_number)
	#recover the last number:
	actual_WT = retrieveWT()
	if actual_WT == None:
		sys.exit()

	#Ya tenemos el nivel de cisterna, se calculan las tendencias.
	if past_WT == 0:
		past_WT = actual_WT[2]
		time.sleep(300)
		continue
	#here is the part where we compare values to exercise critical actions
	#dependiendo del nivel y de las tendencias se hacen las notificaciones pertinentes.
	if actual_WT[2] < 100:
		#call critical function
		low_level_warning(actual_WT[2])
		past_WT = actual_WT[2]
		time.sleep(300)
		continue
	#get WT updates every 
	if(control_number % 6 == 0):
		delta_WT =  actual_WT[2] - past_WT
		if delta_WT <= -2:
			min_left = actual_WT[2]/((past_WT-actual_WT[2])/10)
			print(f"Nivel de cisterna en {actual_WT[2]}. Ha caido {delta_WT} cm en 10 minutos, se estiman { round(min_left/60,1)} hrs restantes hasta vacío")
			send_message(Grupo_WT,quote(f"Nivel de cisterna en {actual_WT[2]}. Ha caido {delta_WT} cm en 10 minutos, se estiman { round(min_left/60,1)} hrs restantes hasta vacío"),token_bot)
		else:
			send_message(Grupo_WT,quote(f"Nivel de cisterna: {actual_WT[2]}. Hay {delta_WT} cm de diferencia vs ultima actualización. Updated: {actual_WT[0]} - {actual_WT[1]} "),token_bot)
		#send_message(Grupo_WT,quote(f"Información actualizada por ultima vez en: {actual_WT[0]} a las {actual_WT[1]}"),token_bot)
	
	past_WT = actual_WT[2]

	time.sleep(300)