import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize

#Choose file to read data from
FilePath = '/Users/Foster/Documents/Python Scripts/FinalMuonDataCopy.data'
all_data = np.genfromtxt(FilePath, delimiter=' ',dtype='float')

#Set up Binning and some information to contrain the bins further if wanted
Binning = 20 #Change range in the histogram line to include or exclude bins
Trim = True
Bin_Min = min(all_data[:,0]/1000)
Bin_Max = max(all_data[:,0]/1000)
First_Bin_Right = Bin_Min+(Bin_Max-Bin_Min)/Binning
#Plot Histogram
#Early bins will be dominated by false stops, while late bins will be dominated by background noise.
#I propose only analyzing based on the center of our data, as to mitigate both types of error
if Trim:
    Histogram = plt.hist(all_data[:,0]/1000, bins=Binning, density=True, range=[0,20], histtype='step', label="Histogram")
else:
    Histogram = plt.hist(all_data[:,0]/1000, bins=Binning, density=True, histtype='step', label="Histogram")
#Array of Left and Right Bin Bounds
Counts = Histogram[0]
Sigma = np.sqrt(Counts)
Relative = 1/Sigma
Left  = np.array([Histogram[1][j] for j in range(Binning)])
Right = np.array([Histogram[1][j+1] for j in range(Binning)])
#Independent (x) and dependent (y) variables from the histogram data
x = np.array((Left+Right)*.5)
y = np.array([Histogram[0][i] for i in range(Binning)])
#define the function
def func(M,a,b,c):
    return a*np.exp(-b*M)+c
# plot the results and print parameters
params, cv = scipy.optimize.curve_fit(func, x, y, sigma=Sigma)
a, b, c = params
#Generate Linespace for a smooth fitted curve regardless of bin size
fitx = np.linspace(x[0],x[len(x)-1],300)
plt.yscale("log")
plt.plot(fitx, func(fitx, a, b, c), '--', label="fitted")
plt.title("Fitted Exponential Curve")
plt.xlabel("MicroSeconds Before Stop Signal")
plt.ylabel("Frequency of Occurance")
T      = 1/b
Tplus  = 2.1969811
ErrorP = 0.0000022
Tminus = 2.025
ErrorM = 0.004
Stdev  = np.sqrt(np.diag(cv))
Stdev  = np.append(Stdev,Stdev[1]*T**2) #Standard Deviation is in order: a, b, c ,T where T is appended.
R      = abs((Tplus/Tminus)*((Tminus-T)/(Tplus-T)))
RPerc  = np.sqrt((ErrorP/Tplus)**2+(ErrorM/Tminus)**2+((ErrorM**2+Stdev[3]**2)/((Tminus-T)**2))+((ErrorP**2+Stdev[3]**2)/((Tplus-T)**2)))
ErrorR = R*RPerc
Stdev  = np.round(np.append(Stdev,ErrorR),8)
print("Fit Parameters:"                                            +
      f"\nInitial         = {round(a,8)}"+u" \u00B1"+f" {Stdev[0]}"+
      f"\nDecay Rate      = {round(b,8)}"+u" \u00B1"+f" {Stdev[1]}"+
      f"\nVertical Offset = {round(c,8)}"+u" \u00B1"+f" {Stdev[2]}"+
      f"\nLifetime        = {round(T,8)}"+u" \u00B1"+f" {Stdev[3]}"+
      f"\nRho             = {round(R,8)}"+u" \u00B1"+f" {Stdev[4]} ({round(100*RPerc,1)}%)")
