import pandas as pd
import os
import glob

# Step 1: get a list of all csv files in target directory
my_dir = "C:\\Users\\moralesja.group\\Documents\\polea"
filelist = []
filesList = []
os.chdir( my_dir )

# Step 2: Build up list of files:
for files in glob.glob("*.txt"):
    fileName, fileExtension = os.path.splitext(files)
    filelist.append(fileName) #filename without extension
    filesList.append(files) #filename with extension

# Step 3: Build up DataFrame:
df = pd.DataFrame()
for ijk in filelist:
	frame = pd.read_csv(ijk+".txt", sep='	', header=None, names=["Fecha","Hora","Tanque_Temp","Limite","Nivel","GWK_Torre_Temp"])
	df = df.append(frame)
	
print(df.describe().applymap('{:,.2f}'.format))


#df.to_csv("C:\\Users\\moralesja.group\\Documents\\polea\\rawdata.csv")

