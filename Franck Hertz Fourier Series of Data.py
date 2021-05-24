import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks_cwt
from scipy.signal import savgol_filter

# Read any data saved as text. Make sure to check the delimiter!
Volts = '3'
FilePath = '/Users/Foster/Documents/Python Scripts/5-60V '+Volts+'V Retarding Bias.csv'
all_data = np.genfromtxt(FilePath, delimiter=' ',dtype='float')

# Low and High are in STEPS, not volts, we have 0.2 steps so low 5 = 1 volt
# Use this to look at different sections of the graph.
low = 0
high = len(all_data)
Period = .2*(high-low)

# Set up Arrays of the independent and dependent variables from all_data
x = np.array([.2*i+5 for i in range(low,high)])
y = np.array([all_data[i] for i in range(low,high)])

# ######## This is Fourier Series stuff, which I stopped using, but keeping it here as a comment.
# # NumberofTerms of the fourier series you want.
# NumberofTerms = 100
# # This calculates a_n for the cos term and b_n for the sin term. Also the constant out front.
# a = np.array([(2*.2/Period)*np.sum(np.cos(2*np.pi*i*x/Period)*y) for i in range(NumberofTerms+1)])
# b = np.array([(2*.2/Period)*np.sum(np.sin(2*np.pi*i*x/Period)*y) for i in range(NumberofTerms+1)])
# Const = a[0]/2
# # A function which calculates "NumberofTerms" functions and sums them up to get your total fourier series.
# def f(M, Nh):
#   f = np.array([a[i]*np.cos(2*np.pi*i*M/Period)+b[i]*np.sin(2*np.pi*i*M/Period) for i in range(1,NumberofTerms+1)])
#   return f.sum()+Const
# # Create a linespace from this new function to use for graphing.
# x2 = np.linspace(.2*low+5,.2*high+5,2000)
# y2 = np.array([f(t,NumberofTerms) for t in x2])
# ###########################################################################################

# Smooth the raw data to get cleaner peaks and reduce noise. Looks at 9 data points and fits them to an order 3 polynomial
Data_Smoothing = savgol_filter(y, 9, 3)

# Calculate the local maximums of the data. The second term clears away noisy peaks.
Peaks = find_peaks_cwt(Data_Smoothing, np.arange(1,15))

#Find the difference between the Peaks. Manually check which ones we care about.
diff = [0 for i in range(len(Peaks)-1)]
for i in range(len(Peaks)-1):
    diff[i] = .2*(Peaks[i+1]-Peaks[i])
print(diff)
    
# Plot the different graphs we calculated.
plt.plot(x,y, label = 'Raw Data')
#plt.plot(x2,y2, label = 'Fourier Series')
plt.plot(x,Data_Smoothing, "--", color= 'black', label = 'Smoothed Data')
plt.plot(.2*Peaks+.2*low+5, Data_Smoothing[Peaks], "x", color = 'red', label = 'Peaks')

# Populate Labels and other info
plt.title(Volts+" Volt Retarding Bias")
plt.xlabel("Accelerating Voltage")
plt.ylabel("Current")
axes = plt.gca()
axes.set_ylim([0,3e-9])
plt.legend()

