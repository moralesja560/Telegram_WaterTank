import pandas as pd
import sys
import os

#en este modelo de análisis falta algo que hacer con el slope
#cuando el nivel está en n (ej. 100cm) ¿Que probabilidad hay de que suba o baje? 
	#Ej. En todas las veces que ha estado la cisterna en 100, 55% de las veces se va hacia abajo.




slope = {"FechaHora":[],"Slope":[]}

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

rawData = pd.read_csv (resource_path(r"images/data_WT.csv"),header=0)

#Step1Data filters out every other minute except o-clock and half hours
Step1Data= rawData.loc[(rawData['Minute'].eq('ok'))]
Step1Data.to_csv(resource_path(r"images/filtered_data.csv"), encoding='utf-8')


#################------------------------------Level Probability--------------------#
Step1_lastLevel = 10000
Step1_UpLevel = 0
Step1_DownLevel = 0
for index,row in Step1Data.iterrows():
	if row['Nivel OK'] == 100 and Step1_lastLevel == 10000:
		Step1_lastLevel = 100
		continue
	if Step1_lastLevel == 100:
		if row['Nivel OK'] > Step1_lastLevel:
			Step1_UpLevel +=1
		elif row['Nivel OK'] < Step1_lastLevel:
			Step1_DownLevel +=1
		Step1_lastLevel = 10000

print(f"Cuando la cisterna toca 100cm, hay una posibilidad del {Step1_UpLevel/(Step1_DownLevel+Step1_UpLevel):.2%} de subir y {Step1_DownLevel/(Step1_DownLevel+Step1_UpLevel):.2%} de que baje")






lastLevel = 0
newLevel = 0


for index, row in Step1Data.iterrows():
	#if lastLevel = 0 then assign the initial value
	if lastLevel == 0:
		lastLevel = row['Nivel OK']
		continue
	#let's say that the last level was 100 and now it's 98. That's a -2
	#store the new level
	newLevel = row['Nivel OK']
	#calculate the level difference between last row and actual row
	WT_delta = (newLevel-lastLevel)
	#for reference, also store exact date/time info
	newLevelDate = row['Fecha Hora']
	#append to dictionary only if they're valid values
	if WT_delta >=-9 and WT_delta <=10:
		slope["FechaHora"].append(newLevelDate)
		slope["Slope"].append(WT_delta)
		#shift the newlevel var to serve as the lastlevel for the next row.
		lastLevel = newLevel

#create a dataframe to find simple statistics
Step2_Data = pd.DataFrame(slope)

#print(Step2_Data)
Step2_Data.to_csv(resource_path(r"images/processed_data.csv"), encoding='utf-8')

# categories:
#+ after +
plusaplus = 0
#+ after -
plusaneg = 0
#+ after 0
plusazero = 0
#- after +
negaplus = 0
#- after -
neganeg = 0
#- after 0
negazero = 0
#0 after +
zeroaplus = 0
#0 after -
zeroaneg=0
#0 after 0
zeroazero = 0

old_slope_data = 10000

for index, row in Step2_Data.iterrows():
	slope_data = row['Slope']
	if old_slope_data == 10000:
		old_slope_data = slope_data
		continue

	#if old_data is positive, select 
	if old_slope_data > 0:
		#if new data is positive add 1 to pertinent var
		if slope_data >0:
			plusaplus +=1
		elif slope_data <0:
			negaplus +=1
		elif slope_data == 0:
			zeroaplus +=1
	if old_slope_data < 0:
		#if new data is positive add 1 to pertinent var
		if slope_data >0:
			plusaneg +=1
		elif slope_data <0:
			neganeg +=1
		elif slope_data == 0:
			zeroaneg +=1
	if old_slope_data == 0:
		#if new data is positive add 1 to pertinent var
		if slope_data >0:
			plusazero +=1
		elif slope_data <0:
			negazero +=1
		elif slope_data == 0:
			zeroazero +=1
	old_slope_data = slope_data

print(f"El total de la información es de: {len(Step2_Data['Slope'])}. \nHay una probabilidad del {plusaplus/len(Step2_Data['Slope']):.2%} que un número positivo, siga a uno positivo")
print(f"Hay una probabilidad del {negaplus/len(Step2_Data['Slope']):.2%} que un número negativo, siga a uno positivo")
print(f"Hay una probabilidad del {zeroaplus/len(Step2_Data['Slope']):.2%} que un zero, siga a uno positivo")
print(f"Hay una probabilidad del {plusaneg/len(Step2_Data['Slope']):.2%} que un número positivo siga a uno negativo")
print(f"Hay una probabilidad del {neganeg/len(Step2_Data['Slope']):.2%} que un número negativo, siga a uno negativo")
print(f"Hay una probabilidad del {zeroaneg/len(Step2_Data['Slope']):.2%} que un zero, siga a uno negativo")
print(f"Hay una probabilidad del {plusazero/len(Step2_Data['Slope']):.2%} que un número positivo siga a zero")
print(f"Hay una probabilidad del {negazero/len(Step2_Data['Slope']):.2%} que un número negativo, siga a un cero")
print(f"Hay una probabilidad del {zeroazero/len(Step2_Data['Slope']):.2%} que un zero, siga a un zero")
print(plusaplus, negaplus, zeroaplus, plusaneg, neganeg, zeroaneg, plusazero, negazero, zeroazero)




