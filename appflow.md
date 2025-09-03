Application process flow
On start up, when the UI is loaded, the app must wait for the user to either input a company and ticker in the single company analysis tab, or go to the ratio’s config tab.
If the user opens the ui and navigates to the ratio config tab, before inputting anything into the single company analysis tab, the program will prompt the user for company and ticker. 
This will then populate the single analysis tab as well.
If they choose to enter the company and ticker into the single company analysis tab, a data/{ticker}_ratio_rules.md file is created in the data/{ticker} folder, as default. 
The user is informed of this with a message in the single company analysis window.
If they choose to go straight to ratio config, the ratios they choose, and click save ratio rules will create the file, this will also display a message in the single company analysis window.
When the user clicks the start analysis button, the following flow must happen:
Check if there is a data/{ticker}.json file in the {ticker} folder. 
If there is, we only fetch the market data from yahoo finance, using the yfinance library
If this is not present, we collect all the data as required by the all_ratio.md file in root.
This information is then saved as {ticker}.json in the data/{ticker} folder
Use this json file to work out all the ratios in the app, creating a {ticker}_all_ratios.md file in the data/{ticker} folder
We also create the {ticker}_agent_ratios.md file in the data/{ticker} folder, which uses the {ticker}_ratio_rules.md to populate this file, as it may not be all the ratios available.
Then we need to validate the {ticker}_all_ratios.md file to ensure that we have information, so if more than 20% of the ratios are 0 or not present, we need to present an error to the user, stating the issue. 
We do not need to stop the app, just a message on the analysis page is enough for now.
We also need to check that there are files in the data/{ticker} folder to be analyzed, so we need to check for files using pattern recognition or search such as. *results*.md, *finance*.md, *report*.md, *balance*.md, *cash*.md etc.
Now we kick of the crew.
