import yahoo_finance as YF
import numpy
import collections
import copy
import csv

# =================[Raw Data]=================

Stock = YF.Share('VRTX')    
Historical = Stock.get_historical('2013-07-13', '2016-08-15')
with open('VRTX.csv', 'w') as csvfile:    
    fieldnames = ['Date', 'Open', 'Low', 'High', 'Close', 'Volume']
    outfile = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #outfile.writeheader()
    
    for line in Historical:
        outfile.writerow({  'Date': line['Date'],
                            'Open': line['Open'],
                             'Low': line['Low'],
                            'High': line['High'],
                           'Close': line['Close'],
                          'Volume': line['Volume']
                                    })

# =================[Training Data]=================

#Historical data from 2013-2016 for Vertex Pharmaceuticals (VRTX)
infile = open('VRTX.csv', 'r')
Titles = ['Date', 'Open', 'Low', 'High', 'Close', 'Volume']
RawData = []
for line in infile:
    CSVdata = line.split(',')
    DICdata = {'Data': CSVdata[0]}
    for i in range(1, 6):
        DICdata[Titles[i]] = float(CSVdata[i])
    RawData.append(DICdata)
infile.close()

#Slow Stochastic Oscilator
def SSO(Historical):
    Lows = []
    Highs = []
    for Day in Historical:
        Lows.append(Day['Low'])
        Highs.append(Day['High'])
    L = min(Lows)
    H = max(Highs)
    LC = float(Historical[0]['Close'])
    return round(100*((LC-L)/(H-L)),2)

#Relative Strength Index
def RSI(Historical):
    Gains = []
    Losses = []
    for Day in Historical:
        Change = Day['Close']-Day['Open']
        if Change > 0:
            Gains.append(Change)
        elif Change < 0:
            Losses.append(-Change)
    AVG_Gain = sum(Gains)/len(Gains)
    AVG_Loss = sum(Losses)/len(Losses)
    return round(100-(100/(1+(AVG_Gain/AVG_Loss))),2)

#Daily Percent Change
def DPC(Day):
    return round(100*((Day['Close']-Day['Open'])/Day['Open']),3)

#Daily Trading Volume
def DTV(Day):
    return round((Day['Volume']/100000),2)

with open('TrainingData.csv', 'w') as csvfile:
    fieldnames = ['SSO', 'RSI', 'DTV', 'DPC']
    outfile = csv.DictWriter(csvfile, fieldnames=fieldnames)
    outfile.writeheader()
    i = 1
    j = 14
    DataEnd = len(RawData)
    while j < DataEnd:
        Group = []
        for k in range(i,j+1):
            Group.append(RawData[k])
        
        outfile.writerow({  'SSO': SSO(Group),
                            'RSI': RSI(Group),
                            'DTV': DTV(RawData[i]),
                            'DPC': DPC(RawData[i-1])
                                    })    
        i += 1
        j += 1
