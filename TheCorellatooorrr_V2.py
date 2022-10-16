import numpy as np
from numpy import NaN, ceil, floor
import pandas as pd
import requests
import io
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.gridspec import GridSpec
import os
from YieldFarming import ImportDataFromCG
import matplotlib.dates as mdates
from datetime import timedelta

CURR_DIR = os.path.dirname(os.path.realpath(__file__))

def CovCorrCalc(AssetPrice1: np.ndarray, AssetPrice2: np.ndarray) -> np.ndarray:           #Function for the cov and Corr. 
    num = len(AssetPrice1)
    Numerator = 0; Coin1_std = 0; Coin2_std = 0
    mean_Coin1 = np.mean(AssetPrice1)
    mean_Coin2 = np.mean(AssetPrice2)
    CovCorr = []

    for i in range(int(num)):   
        Numerator += (AssetPrice1[i] - mean_Coin1)*(AssetPrice2[i] - mean_Coin2)
        Coin1_std += (AssetPrice1[i] - mean_Coin1)**2
        Coin2_std += (AssetPrice2[i] - mean_Coin2)**2
    Denominator = np.real((Coin1_std**0.5)*(Coin2_std**0.5))
    CovCorr.append(Numerator/(num-1))     #Co-variance of asset pair over the datasets.
    CovCorr.append(np.real(Numerator/Denominator))  #Correlation co-efficient of asset pair over the datasets.
    
    return CovCorr       #Returns a two number list that has the covariance in the first slot and correlation in the second.

########################## Correlation for certain periods calculated like a moving average function:
def CovCorrMA(period: int, AssetPrice1: np.ndarray, AssetPrice2: np.ndarray, index) -> pd.DataFrame:
    ProperLength = len(index)
    count = 0;  Numerator = 0; Coin1_std = 0; Coin2_std = 0
    num = len(AssetPrice1)
    mean_Coin1 = np.mean(AssetPrice1)
    mean_Coin2 = np.mean(AssetPrice2)
    
    CovColName = 'CV_'+str(period)+'day'
    CorrColName = 'CC_'+str(period)+'day'
    Cov = np.array([]); Corr = np.array([])
    for i in range(num):            
        if(i > (num-int(period))):
            break 
        for j in range(int(period)):
            count = i + j
            Numerator += (AssetPrice1[count] - mean_Coin1)*(AssetPrice2[count] - mean_Coin2)
            Coin1_std += (AssetPrice1[count] - mean_Coin1)**2
            Coin2_std += (AssetPrice2[count] - mean_Coin2)**2
        Denominator = np.real((Coin1_std**0.5)*(Coin2_std**0.5))
        PeriodCorr = (np.real(Numerator/Denominator))
        PeriodCov = (np.real(Numerator/(num-1)))
        Cov = np.append(Cov,PeriodCov)
        Corr = np.append(Corr,PeriodCorr)
        Numerator = 0        ## Reset the counter variables.
        Coin1_std = 0
        Coin2_std = 0
    
    Cov = np.pad(Cov,((ProperLength-len(Cov),0)),constant_values=(np.nan))
    Corr = np.pad(Corr,((ProperLength-len(Corr),0)),constant_values=(np.nan))
    CovCorrDict = {CovColName:Cov,CorrColName:Corr}
    CovCorrDF = pd.DataFrame(CovCorrDict, index=index)
    #print('CovCorrDF length: ',len(CovCorrDF), CovCorrDF)
    return CovCorrDF       #Dataframe containing the MA for the given period, 1st column co-variance, second column correlation co-efficient. 

def Correlation(Series1:pd.Series, Series2:pd.Series,period='Full'): #Calculate Pearson COrrelation co-efficient between two series with time frame: period. 
    if (period=='Full'):
        Cor = round(Series1.corr(other=Series2,method='pearson', min_periods=len(Series1)),3)
        print('The correlation over the entire length between the two series: '+Series1.name+' and '+Series1.name+' is: '+str(round(Cor,3))+'.')
    else:
        Cor = Series1.rolling(period).corr(Series2) ##Using Pandas to calculate the correlation. 
    return Cor    

 #You can change to manual coin and time length selection instead of auto selection based on what you've already saved in the input .csv file
# by commenting out the relevant 6 lines below here and uncommenting lines 23 - 25. 
#Auto input of coin selection and parameters:
dfIn = pd.read_csv(CURR_DIR+"\PairCorrInput.csv")  #We need to make sure the little r is there next to the path string to make it a raw string.
Coin1 = str(dfIn.loc[0].at["Coin1"])                                   #Windows requires directory designators of "\\" instead of just "\" which works for mac and linux.
Coin2 = str(dfIn.loc[0].at["Coin2"])
CCAvs = pd.Series.dropna(dfIn["CC Averages"])
numCCAvs = len(CCAvs)
print("Correlation averages to calculate: \n",CCAvs,numCCAvs)
print('Coin 1 is: '+Coin1)
print('Coin 2 is: '+Coin2)
TimeLength = str(dfIn.loc[0].at["NumDays"])
#print(Coin1,Coin2,TimeLength)
#Call API for selected coins with manual input:
#Coin1 = input("Give a coin gecko API for coin 1: ")
#Coin2 = input("Give a coin gecko API for coin 2: ")
#TimeLength = input('Provide number of days into the past that you wish to get the historical data for: ')

#Call CoinGecko API:
df = ImportDataFromCG.CoinGeckoPriceHistory(Coin1,TimeLength)
dtIndex = pd.DatetimeIndex(df.index); df.set_index(dtIndex)
df2 = ImportDataFromCG.CoinGeckoPriceHistory(Coin2,TimeLength)
dtIndex2 = pd.DatetimeIndex(df2.index); df2.set_index(dtIndex2)
df = df[::-1]; df2 = df2[::-1]
length = len(df)
length2 = len(df2)
if(length < length2):
    comLength = length
else:
    comLength = length2
print('Coin1 length: '+str(length)+ ', Coin2 length: '+str(length2)+'.')
if(length != length2):     #Check that the two data matrices pulled from the API are of equal length:
    print("Warning: Length of the two price matrices are not equal, pull out. Set numDays parameter to: "+str(comLength-1)+'.')
    quit()
else:
    numDays = comLength
    print("Number of days into the past before today tracked here: "+str(numDays)+'\r')
    PriceMatrix1 = pd.DataFrame(df)
    PriceMatrix2 = pd.DataFrame(df2); print(PriceMatrix1, PriceMatrix2)
    Price1 = pd.Series.to_numpy(PriceMatrix2['Price (USD)'])
    Price2 = pd.Series.to_numpy(PriceMatrix2['Price (USD)'])

    #Use my covariance, correlation function: 
    CovCorr = CovCorrCalc(Price1, Price2)
    CovString = 'Asset pair co-variance over the whole \ntime period (manual): '+str(round(CovCorr[0], 4))
    CorrString = 'Asset pair correlation over the whole \ntime period (manual): '+str(round(CovCorr[1], 4))
    print(CovString); print(CorrString)

    #Check it with numpy and pandas correlation calculations:
    print('Standard deviation (numpy) coin1, coin2: ',np.std(Price1),np.std(Price2))
    NumpyCorr = np.corrcoef(Price1,Price2)
    NumpyCov = np.cov(Price1,Price2)
    PandasCorr = Correlation(PriceMatrix1['Price (USD)'], PriceMatrix2['Price (USD)'])
    NPCorrString = 'Asset pair correlation over the whole \ntime period (from numpy): '+str(round(NumpyCorr[1,0], 4))
    pdCorrString = 'Asset pair correlation over the whole \ntime period (from pandas): '+str(PandasCorr)
    NPCovString = 'Asset pair covariance over the whole \ntime period (from numpy): '+str(round(NumpyCov[1,0], 4))
    print(NPCorrString); print(pdCorrString); print(NPCovString)

    MasterDF = pd.concat([PriceMatrix1,PriceMatrix2],axis=1) # Create the master dataframe to output to csv.  
    Index = pd.DatetimeIndex(MasterDF.index)
    Series1 = PriceMatrix1['Price (USD)']; Series2 = PriceMatrix2['Price (USD)']
    for i in range(numCCAvs):
        CorrAv = CovCorrMA(int(CCAvs[i]),Price1, Price2,Index)
        PDCor = Correlation(Series1, Series2, period=int(CCAvs[i]))
        PDCor = pd.Series(PDCor, name='Pandas rolling corr ('+str(int(CCAvs[i]))+'d)')
        MasterDF = pd.concat([MasterDF, CorrAv, PDCor],axis=1)
    CovCorr_Full = CovCorrMA(numDays, Price1, Price2,Index)
    MasterDF = pd.concat([MasterDF, CovCorr_Full],axis=1)
    MasterDF.to_csv(CURR_DIR+"\PairCorrOutput.csv", index = False)  #We need to make sure the little r is there next to the path string to make it a raw string.
    print('Data output to: '+CURR_DIR+"\PairCorrOutput.csv") #We need to make sure the little r is there next to the path string to make it a raw string. 

    #Calculate normalised price ratio wave and normalized percentage changed from median wave.
    PriceRatio = PriceMatrix1['Price (USD)']/PriceMatrix2['Price (USD)']
    Ratio_norm = (PriceRatio - PriceRatio.min())/ (PriceRatio.max() - PriceRatio.min())
    Percentage = PriceRatio
    midpoint = np.median(PriceRatio)
    points = len(PriceRatio)
    print('Median of the '+str(Coin1)+'/'+str(Coin2)+' data is: '+ str(midpoint))

    for i in range(int(points)):
        Percentage.iloc[i] = ((Percentage.iloc[i] - midpoint)/midpoint)*100

    # # ################################### #Plot figures #############################################################

    #Price ratio plot.
    fig = plt.figure(figsize=(8.3,9.5))
    gs1 = GridSpec(3, 1, top = 0.96, bottom=0.07, left=0.11, right=0.88, wspace=0.01, height_ratios=[2,2,1], hspace=0)
    ratString = Coin1+'/'+Coin2
    ax1 = fig.add_subplot(gs1[0])
    TitleString = 'Price ratio '+Coin1+'/'+Coin2+r', $\Delta$% from median'
    ax1.set_title(TitleString, fontsize=12, fontweight = 'bold')
    trace3 = ax1.plot(PriceMatrix1.index,Percentage, c = 'black', label=ratString)
    ax1.invert_xaxis()
    ax1.set_ylabel(r'$\Delta$ price from median (%)', fontsize=14)
    ax1b = ax1.twinx()
    ax1b.plot(PriceMatrix1.index,Percentage, c = 'black')
    ax1.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax1b.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax1.legend(loc=2)
    for axis in ['top','bottom','left','right']:
            ax1.spines[axis].set_linewidth(1.5)  
    xleft = PriceMatrix1.index[0] - timedelta(days = 5); xright = PriceMatrix1.index[len(PriceMatrix1)-1] + timedelta(days = 5)
    ax1.set_xlim(xleft, xright)
    ax1.minorticks_on(); ax1b.minorticks_on(); ax1.grid(visible=True,which='both',linewidth=0.55,linestyle=':')   
    ax1.set_xticklabels([])
    ax1.tick_params(axis='x', labelsize='x-small',labelrotation=90)      

    #Price of both assets on the one graph.

    ax2 = fig.add_subplot(gs1[1],sharex=ax1)
    TitleString = Coin1+' vs left axis, '+Coin2+' vs right axis'
    ax2.set_ylabel('Price (USD)', fontsize=14)
    #ax2.set_title(TitleString, fontsize=12)
    trace1 = ax2.plot(PriceMatrix1['Price (USD)'], c='black',label =Coin1+'\n(left)')
    ax2b = ax2.twinx()
    trace2 = ax2b.plot(PriceMatrix2['Price (USD)'], c='red',label =Coin2+'\n(right)')
    ax2b.set_ylabel('Price (USD)', fontsize=14)
    ax2.legend(loc=2,fontsize='small'); ax2b.legend(loc=1,fontsize='small')
    for axis in ['top','bottom','left','right']:
            ax2.spines[axis].set_linewidth(1.5)  
    ax2.minorticks_on(); ax2b.minorticks_on()        
    ax2.grid(visible=True,which='both',linewidth=0.55,linestyle=':')   
    ax2.set_xticklabels([])
    ax2.tick_params(axis='x', labelsize='x-small',labelrotation=90)     

    # Correlation fig.:
    CorrString = 'Pair correlation over the whole period: '+str(round(float(NumpyCorr[1,0]), 4))
    ax3 = fig.add_subplot(gs1[2],sharex=ax1)
    ax3.set_title(CorrString, fontsize=9)
    ax3.set_ylabel('Correlation', fontsize=14)
    for i in range(numCCAvs):
        traceName = 'CC_'+str(int(CCAvs[i]))+'day'
        traceName2 = 'Pandas rolling corr ('+str(int(CCAvs[i]))+'d)'
        tracelabel = '$CC_{'+str(int(CCAvs[i]))+'d}$'
        r = (i/(numCCAvs-1)); g = 0; b = 1 - (i/(numCCAvs-1))
        LW = 1+(i*0.25)
        ax3.plot(MasterDF[traceName], c =(r, g, b), label = tracelabel, linewidth = LW)
        #ax3.plot(MasterDF['Pandas rolling corr ('+str(int(CCAvs[i]))+'d)'], c =(r, g, b), label = tracelabel, linewidth = LW)
    ax3.legend(loc=1, fontsize='small',bbox_to_anchor=(1.15, 0.9))
    ax3.set_ylim(-1.1, 1.1)
    for axis in ['top','bottom','left','right']:
            ax3.spines[axis].set_linewidth(1.5)  
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%y-%b'))
    xmin = Percentage.index[0]; xmax = Percentage.index[len(Percentage)-1]; tick_count = 13
    stepsize = (xmax - xmin) / tick_count        
    ax3.xaxis.set_ticks(np.arange(xmin, xmax, stepsize))
    ax3.tick_params(axis='x', labelsize='small',labelrotation=45)

    plt.show() # Show figure. Function will remain running until you close the figure. 
