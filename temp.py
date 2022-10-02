import pandas as pd
import os,sys
import glob
import subprocess

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Step 1: get a list of all csv files in target directory
my_dir = "C:\\Users\\moralesja.group\\Documents\\polea"
filelist = []
filesList = []
os.chdir( my_dir )

# Step 2: Build up list of files:
for files in glob.glob("*.hst"):
    fileName, fileExtension = os.path.splitext(files)
    filelist.append(fileName) #filename without extension
    filesList.append(files) #filename with extension

# Step 2.5 Transform them into txt

#for ijk in filelist:
	#subprocess.call([resource_path(r"images/HST2TXT.exe"), ijk+".hst"])

my_dir = "C:\\Users\\moralesja.group\\Documents\\polea"
filelist = []
filesList = []
os.chdir( my_dir )


# Step 3: Build up list of files:
for files2 in glob.glob("*.txt"):
    fileName2, fileExtension2 = os.path.splitext(files2)
    filelist.append(fileName2) #filename without extension
    filesList.append(files2) #filename with extension

# Step 4: Build up DataFrame:
df = pd.DataFrame()
for ijk in filelist:
	frame = pd.read_csv(ijk+".txt", sep='	', header=None, names=["Fecha","Hora","Tanque_Temp","Limite","Nivel","GWK_Torre_Temp"])
	df = df.append(frame)
	
print(df.describe().applymap('{:,.2f}'.format))


df.to_csv("C:\\Users\\moralesja.group\\Documents\\polea\\rawdata2.csv")

