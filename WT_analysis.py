from functools import total_ordering
import pandas as pd
import sys
import os

#en este modelo de análisis falta algo que hacer con el slope
#cuando el nivel está en n (ej. 100cm) ¿Que probabilidad hay de que suba o baje? 
	#Ej. En todas las veces que ha estado la cisterna en 100, 55% de las veces se va hacia abajo.




slope = {"FechaHora":[],"Slope":[]}
WT_trending = {"Nivel":[],"UpLevel":[],"DownLevel":[],"ZeroLevel":[]}

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
Step1_ZeroLevel = 0




for i in range(1,210):
	for index,row in Step1Data.iterrows():
		#this for-loop looks for the level and then decides
		if row['Nivel OK'] == i and Step1_lastLevel == 10000:
			Step1_lastLevel = i
			continue
		if Step1_lastLevel == i:
			if row['Nivel OK'] > Step1_lastLevel:
				Step1_UpLevel +=1
				Step1_lastLevel = 10000
				continue
			elif row['Nivel OK'] < Step1_lastLevel:
				Step1_DownLevel +=1
				Step1_lastLevel = 10000
				continue
			elif row['Nivel OK'] == Step1_lastLevel:
				Step1_ZeroLevel +=1
			Step1_lastLevel = 10000
	if Step1_UpLevel+Step1_DownLevel+Step1_ZeroLevel > 0:
		WT_trending["Nivel"].append(i)
		WT_trending["UpLevel"].append(f"{Step1_UpLevel/(Step1_UpLevel+Step1_DownLevel+Step1_ZeroLevel):.2%}")
		WT_trending["DownLevel"].append(f"{Step1_DownLevel/(Step1_UpLevel+Step1_DownLevel+Step1_ZeroLevel):.2%}")
		WT_trending["ZeroLevel"].append(f"{Step1_ZeroLevel/(Step1_UpLevel+Step1_DownLevel+Step1_ZeroLevel):.2%}")
	Step1_UpLevel = 0
	Step1_DownLevel = 0
	Step1_ZeroLevel = 0
	Step1_lastLevel = 10000

WT_trending_df = pd.DataFrame(WT_trending)

WT_trending_df.to_csv(resource_path(r"images/trends.csv"), encoding='utf-8')

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

total_plus = plusaneg+plusaplus+plusazero
total_neg = plusaneg + neganeg +zeroaneg
total_zero = plusazero+negazero+zeroazero

print(f"Despues de un número positivo, el {plusaplus/total_plus:.2%} de las veces, siguió un número positivo, el {negaplus/total_plus:.2%} fue un numero negativo y el {zeroaplus/total_plus:.2%} siguió un 0 ")
print(f"Despues de un número negativo, el {plusaneg/total_neg:.2%} de las veces, siguió un número positivo, el {neganeg/total_neg:.2%} fue un numero negativo y el {zeroaneg/total_neg:.2%} siguió un 0 ")
print(f"Despues de un cero, el {plusazero/total_zero:.2%} de las veces, siguió un número positivo, el {negazero/total_zero:.2%} fue un numero negativo y el {zeroazero/total_zero:.2%} siguió un 0 ")
print(f"El total de la información es de:{len(Step2_Data['Slope'])}")
print(plusaplus, negaplus, zeroaplus, plusaneg, neganeg, zeroaneg, plusazero, negazero, zeroazero)




