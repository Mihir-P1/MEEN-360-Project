# Title

# MEEN 360 - 202
# Honors Project 2
# Phase 1
# Megan Dawkins
# Modifications by Mihir
#  Plotting Eutectic temperature line
#  Converting MatLab syntax to python (very similar, just different library & no line function)

## Instructions

# Plot phase diagram curves by finding points on each line, using Excel to
# find trendline equations, then plotting these equations in python

from numpy import *
from matplotlib.pyplot import *
from math import *


def plotCurves():
    # Plot the phase diagram for Pb-Sn

    # Curve 1: from "a" to "a+L"
    x1 = linspace(0,18.3,300)
    y1 = -0.0127*x1**3 - 0.0163*x1**2 - 3.3235*x1 + 327.03

    # Curve 2: from "a+L" to "L"
    x2 = linspace(0,61.9,300)
    y2 = -2.3263*x2 + 327

    # Curve 3: from "L" to "B+L"
    x3 = linspace(61.9,100,300)
    y3 = 1.2861*x3 + 103.99

    # Curve 4: from "a" to "B" - Eutectic
    x4 = linspace(18.3,97.8,300)

    y4 = []
    for i in range(len(x4)):
        y4.append(183)

    # Curve 5: from "a" to "a+B"
    x5 = linspace(2.5,18.3,300)
    y5 = []
    for x in x5:
        y5.append(65.809*log(x) - 8.3001)

    # Curve 6: from "B+L" to "B"
    x6 = linspace(97.8,100,300)
    y6 = 22.273*x6 - 1995.3

    # Curve 7: from "a+B" to "B"
    x7 = linspace(97.8,99.2,300)
    y7 = -93.571*x7 + 9334.3
    
    # Plot phase diagram
    plot(x1,y1)
    plot(x2,y2)
    plot(x3,y3)
    plot(x4,y4)
    plot(x5,y5)
    plot(x6,y6)
    plot(x7,y7)
    title('Lead-Tin Phase Diagram')
    xlabel('wt% (Sn)')
    ylabel('Temperature (deg C)')
def plotCurves1(phase1,phase2,wt,T):
    # Generating updated phase diagram with tie line
    plotCurves()
    hlines(T,phase1,phase2,color='c')
    vlines(wt,52,T,color='k')
    # Plot alloy composition
    plot(wt,T,'ro')
    # Identifying the tie line on the plot
    annotate('Tie Line', (wt,T), xytext = (wt - 1, T + 5), horizontalalignment='right')

def validateUserInput(wt_Sn,T):
    # Ensure phase diagram is valid for
    # Provided temperature and composition values
    if wt_Sn < 0 or wt_Sn > 100:
        return (False,'wt_Sn must be between 0 and 100')

    if T < 52 or T > 350:
        return (False,'T must be between 52 and 350 C')
    return True,'Valid inputs.'

def findPhase(wt_Sn,T):
    # Figure out which phases exist (liquid, alpha, beta)
    
    # Define Curves
    
    # Curve 1: from "a" to "a+L"
    y1 = -0.0127*wt_Sn**3 - 0.0163*wt_Sn**2 - 3.3235*wt_Sn + 327.03

    # Curve 2: from "a+L" to "L"
    y2 = -2.3263*wt_Sn + 327

    # Curve 3: from "L" to "B+L"
    y3 = 1.2861*wt_Sn + 103.99

    # Curve 4: from "a" to "B" - Eutectic
    y4 = 183

    # Curve 5: from "a" to "a+B"
    y5 = 65.809*log(wt_Sn) - 8.3001
    
    # Curve 6: from "b" to "b+L"
    y6 = 22.273*wt_Sn - 1995.3

    # Curve 7: from "B" + "a+B"
    y7 = -93.571*wt_Sn + 9334.3
    
    #Phases:
    #   1: Liquid
    #   2: alpha
    #   3: alpha + Liquid
    #   4: Liquid + Beta
    #   5: Beta
    #   6: alpha + Beta

    phases = 0
    if wt_Sn <= 18.3: # Horizontal region 1
        if T >= y2:
            phases = 1
        elif T >= y1:
            phases = 3
        elif T >= y5:
            phases = 2
        else:
            phases = 6

    elif wt_Sn <= 61.9: #Horizontal region 2
        if T >= y2:
            phases = 1
        elif T >= y4:
            phases = 3
        else:
            phases = 6

    elif wt_Sn <= 97.8: #Horizontal region 3
        if T >= y3:
            phases = 1
        elif T >= y4:
            phases = 4
        else:
            phases = 6
        
    elif wt_Sn <= 100: #Horizontal region 4
        if T>= y3:
            phases = 1
        elif T >= y6:
            phases = 4
        elif T <= y7:
            phases = 6
        else:
            phases = 5
    return phases

def plotTieLine(phase1,phase2,wt,T):
    # Create a separate figure of just the tie line

    # Credits: Heavily inspired by
    # https://stackoverflow.com/questions/23186804/graph-point-on-straight-line-number-line-in-python
    
    fig = figure(figsize = (4,1))
    ax = fig.add_subplot(111)
    hlines(T,phase1,phase2)
    yticks([T])
    xticks([phase1,phase2])
    plot(wt,T,'ro')
    axis('off')
    text(phase1 - 0.1,T,f'{phase1:.1f}%',horizontalalignment = 'right')
    text(phase2 + 0.1,T,f'{phase2:.1f}%',horizontalalignment = 'left')
    annotate(f'{wt:.1f}% Sn', (wt,T), xytext = (wt - 1, T + 5), 
              arrowprops=dict(facecolor='black', shrink=0.1), 
              horizontalalignment='right')

def findComposition(wt_Sn,T,phase):
    # Define curves in terms of x in order to solve for the wt% at each T
    x1 = -6E-06*T**3 + 0.0037*T**2 - 0.8648*T + 87.149
    x2 = -0.42987*(T-327)
    x3 = 0.777545*(T-103.99)
    x5 = 1.1115*exp(0.0151*T)
    x6 = 0.044897*(T+1995.3)
    x7 = -0.011638*(T-8584.7)
    
    phases = phase

    # Variables to store potential outputs
    comp_liquid = 0
    comp_alpha = 0
    comp_beta = 0
    amount_liquid = 0
    amount_alpha = 0
    amount_beta = 0

    # Find composition and amount of each phase
    # Array to store compositions in case need to plot tie line
    phases_tieLine = []

    # Check if Eutectic composition & temperature
    if (wt_Sn == 61.9 and T == 183):
        phases = 'Liquid -> alpha + beta'
    
    # Apply Lever Rule based on phase
    
    elif(phases == 1):
        # Label the phase with its name
        phases = 'Liquid'
        
        #Only one phase is present
        comp_liquid = wt_Sn
        amount_liquid = 100
    
    elif (phases == 2):
       # Label the phase with its name
        phases = 'Alpha'
        
        #Only one phase is present
        comp_alpha = wt_Sn
        amount_alpha = 100
    
    elif (phases == 3):
        # Label the phase with its name
        phases = 'alpha + Liquid'
        
        # Solve for each phase's composition
        comp_alpha = x1
        comp_liquid = x2
        
        # Solve for the fraction # of each phase
        amount_alpha = (comp_liquid - wt_Sn) / (comp_liquid - comp_alpha) * 100
        amount_liquid = (wt_Sn - comp_alpha) / (comp_liquid - comp_alpha) * 100
        phases_tieLine = [comp_alpha,comp_liquid]

    elif (phases == 4):
        # Label the phase with its names
        phases = 'Liquid + Beta'
        
        # Solve for each phase's composition
        comp_liquid = x3
        comp_beta = x6

        # Solve for the fraction # of each phase
        amount_liquid = (comp_beta - wt_Sn) / (comp_beta - comp_liquid) * 100
        amount_beta = (wt_Sn - comp_liquid) / (comp_beta - comp_liquid) * 100
        phases_tieLine = [comp_liquid,comp_beta]

    elif (phases == 5):
        # Label the phase with its name
        phases = 'Beta'
        
        #Solve for the fraction # of each phase
        comp_beta = wt_Sn
        amount_beta = 100

    elif (phases == 6):
        # Label the phase with its name
        phases = 'Alpha + Beta'
        
        # Solve for each phase's composition
        comp_alpha = x5
        comp_beta = x7

        # Solve for the fraction # of each phase
        amount_alpha = (comp_beta - wt_Sn) / (comp_beta - comp_alpha) * 100
        amount_beta = (wt_Sn - comp_alpha) / (comp_beta - comp_alpha) * 100
        phases_tieLine = [comp_alpha,comp_beta]
    
    # Constructing dictionary that will contain all nonzero outputs
    quantities = ['Phases','Liquid Comp','Liquid Amount','Alpha Comp','Alpha Amount','Beta Comp','Beta Amount']
    vars = [comp_liquid,amount_liquid,comp_alpha,amount_alpha,comp_beta,amount_beta]

    # Storing user inputs and the phases that exist
    data = [[0,1,2],[],[]]
    data[1].append("wt% Sn")
    data[2].append(f'{wt_Sn:.1f}% Sn')
    data[1].append("Temperature")
    data[2].append(f'{T:.1f} C')
    data[1].append(quantities[0])
    data[2].append(phases)
    count = 3

    # Filling the outputs array with nonzero outputs
    for i in range(len(vars)):
        if(vars[i] != 0):
            data[0].append(count)
            count += 1
            data[1].append(quantities[i+1])
            data[2].append(f'{vars[i]:.2f}% Sn')

    # If there are two phases exist, then plot a tie line
    if(len(phases_tieLine)==2):
        plotTieLine(phases_tieLine[0],phases_tieLine[1],wt_Sn,T)
        savefig('static/my_plot2.png')
        close()

        plotCurves1(phases_tieLine[0],phases_tieLine[1],wt_Sn,T)
        savefig('static/my_plot1.png')
        close()
        return data,True
    return data,False
