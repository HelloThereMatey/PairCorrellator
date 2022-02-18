# Crypto Pair Correlation Calculator
Crypto pair correlator. Choose any two coins that are listed on CoinGecko and plot the prices, price ratio and correlation over a variety of periods. Inputs are specified in the "PairCorrInput.csv" file. The coin-gecko API ID name must be used in the A2 and B2 cells to specify the coins.  Enter the number of days for which you want to calculate the data in cell C2. In column D starting from D2, enter numbers to indicate the periods over which you wish to calculate the correlation moving averages. This can be arbitray numbers and number of averages yet having too many will make the correlation graph too busy to be useful. An output file is generated that contains price data and the correlation and covariance moving averages. You will of course need the python packages that are imported by the file at the top of the script, already installed on your python distribution. You'll also need to specify the directory on your computer containing the input and output files where necessary in the code (currently lines 15, 141 and 142). 
  
This tool should be useful for assessing whether a given pair of coins are a good match for yield farming or whether you'll get smashed by impermanent loss. Highly correlated assets will generally have very slow change in the price ratio of the two assets (shown on top graph). This change is what causes impermanent loss. The optimal situation for minimizing IL is to have a pair with very high correlation which will manifest in these graphs as the top  graph being close to a horizontal line, the middle graph having the two assets always following eachother in price and all CC averages being close to 1 at all times. CC is the Pearson Corrleation Co-efficient and this = 1 when the assets are perfectly correlated, 0 if they have no correlation (prices move randomly with respect to eachother) and - 1 for perfect anti-correlation. Anti-correlation means that whenever one goes up the other will go down and vice-versa. For yield farming, correllation is optimal and IL increases as you head towards CC = -1. 

I'm aiming to add a panel interface and make into a self-contained application eventually. I'll also build in other functions. I'll also add in different API calls to take data from trading view and other sources. Anyone keen to help out, send me DM on twitter @DegenYieldMan.

How to use (this is written for a complete NOOB, disregard it if you know some coding basics):

- What you'll need: spreadsheet editor (excel, open office etc). Windows terminal (windows).
- Look through my code here to assure yourself that there is nothing malicous hidden there. 
- It's just a simple script to pull price data from coin-gecko API, calculate the correlation of an asset pair and graph it. 
- Download the script and input/ouput csv files: code -> Download Zip.
- Unzip the zip file to location of your choice. You'll need to note the path to this folder.
- Open windows command prompt. You'll need the latest version of cmd prmpt where linux commands support has been
integrated. If you have the latest version of windows you should have this. If not go to microsoft store and search terminal, install windows terminal. 
- Pin terminal to the taskbar for future use. Note it's still called 'Command Prompt' 
-By enter 'command', I mean type the text command within the quotes into terminal and hit enter. Don't inlcude the quotes ''.
- In terminal enter: 'python --version', if no python installed, enter: 'python'
- This should bring up the windows store on python page. Alternatively bring up the store and search python. 
- Install python. 
- python --version should now show something like: PYTHON 3.10.
- Let's test python, enter 'python' again, this should open python interpreter, you can run python commands here. It works quite well as a calculator. 
enter 'quit()' to leave the interpreter and get back to regular terminal.  
- Now we'll need to install the packages used by my python script.
- Enter pip --version
- If you don't have pip, follow the steps listed here: https://phoenixnap.com/kb/install-pip-windows
- Try upgrading pip in case you don't have latest version: enter 'pip install --upgrade pip'
- Install packages: numpy, requests, pandas, io, matplotlib. To install a package enter: pip install 'package name' e.g: pip install numpy
- Let the installion complete each time before installing next package. 
- Now we just have to make one small change to the script. Open script with notepad or similar:
- The line number is listed at bottom on notepad. Go to line 14. Replace the full path to "PairCorrInput.csv" file, to the path to the same file on your system.
- A shortcut to get the path is to drag and drop the PairCorrInput.csv file onto the terminal. Copy the path shown on terminal, paste this text within the quotes
on line 14. 
- Do the same on lines 141 and 142 for the output file. Paste the same path within the quotes on 141 and 142 yet change 'Input" to 'Output". 
- Save file.
- Now we can run the file. In terminal, enter 'python' with a space after and then drag and drop the 'Correllatooorrr_V1.py' file onto terminal. Hit enter. 
- Script should run and the figure with graphs come up. You can save this to .png using the icon at bottom. 
- To choose the coins you want to compare: 
	- Go to coin-gecko: https://www.coingecko.com/
        - Search your coins. Copy the "API ID" for each coin.
	- Paste into cells A2 and B2 on the PairCorrInput.csv file using excel or similar. 
	- Set cell C2 to the number of days of data that you want. Generally this would be the number of days that the more recently launched coin has existed for -1. 
	- In column D "CC Averages" enter the correlation moving averages that you'd like to plot. Default is 9, 20, 50 and 200 day correlation averages. 
	- Save file. Run the script through through terminal again. 
- If using Mac or linux, the only real difference for the whole process will be the notation of the paths to the input and output files. Windows uses 'C:\Users' while mac and linux will start just with Users\
- This was tested on mac, linux and windows using python 3. 
