# WOD-Predict
We're attempting to create a tool that will allow us to create models of our fitness

How to use the tool:

1.) Run the 'main.py' script. It will ask if you are a new or returning athlete. 
If you're new, it will ask for your scores for a handful of common CrossFit Benchmark WODs. 
If you're a returning athlete, you will be brought to the "Enter a WOD" prompt. 

2.) The AMRAP is the only WOD format that works right now. The Rounds For Time format can make predictions, however, I have not had time to implement the "adjusting alpha" function yet. 

3.) Once you successfully enter a WOD, you will be asked if you would like to see the prediction before or after you enter your results. Choose whichever option you prefer and be sure to enter your score in the correct format. 

4.) You will be asked if you'd like to get another prediction. If not, the program will terminate (and your results will be saved in the corresponding .csv files)

