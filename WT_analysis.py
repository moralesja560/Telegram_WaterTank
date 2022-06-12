from hashlib import new
import pandas as pd
import sys
import os

slope = {"FechaHora":[],"Slope":[]}

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

df = pd.read_csv (resource_path(r"images/data_WT.csv"),header=0)

df1= df.loc[(df['Minute'].eq('ok'))]
df1.to_csv(resource_path(r"images/filtered_data.csv"), encoding='utf-8')

lastLevel = 0
newLevel = 0

for index, row in df1.iterrows():
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
WT_Dataframe = pd.DataFrame(slope)

#print(WT_Dataframe)
WT_Dataframe.to_csv(resource_path(r"images/processed_data.csv"), encoding='utf-8')

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

for index, row in WT_Dataframe.iterrows():
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

print(f"El total de la información es de: {len(WT_Dataframe['Slope'])}. \nHay una probabilidad del {plusaplus/len(WT_Dataframe['Slope']):.2%} que un número positivo, siga a uno positivo")
print(f"Hay una probabilidad del {negaplus/len(WT_Dataframe['Slope']):.2%} que un número negativo, siga a uno positivo")
print(f"Hay una probabilidad del {zeroaplus/len(WT_Dataframe['Slope']):.2%} que un zero, siga a uno positivo")
print(f"Hay una probabilidad del {plusaneg/len(WT_Dataframe['Slope']):.2%} que un número positivo siga a uno negativo")
print(f"Hay una probabilidad del {neganeg/len(WT_Dataframe['Slope']):.2%} que un número negativo, siga a uno negativo")
print(f"Hay una probabilidad del {zeroaneg/len(WT_Dataframe['Slope']):.2%} que un zero, siga a uno negativo")
print(f"Hay una probabilidad del {plusazero/len(WT_Dataframe['Slope']):.2%} que un número positivo siga a zero")
print(f"Hay una probabilidad del {negazero/len(WT_Dataframe['Slope']):.2%} que un número negativo, siga a un cero")
print(f"Hay una probabilidad del {zeroazero/len(WT_Dataframe['Slope']):.2%} que un zero, siga a un zero")
print(plusaplus, negaplus, zeroaplus, plusaneg, neganeg, zeroaneg, plusazero, negazero, zeroazero)




