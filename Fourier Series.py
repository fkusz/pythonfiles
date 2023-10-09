import numpy as np
import matplotlib.pyplot as plt

# Read any data saved as text. Make sure to check the delimiter!
#FilePath = '/Users/Foster/Documents/Python Scripts/5-60V '+Volts+'V Retarding Bias.csv'
#all_data = np.genfromtxt(FilePath, delimiter=' ',dtype='float')
scale = 0.001
all_data = np.exp(scale*np.linspace(0,999,1000))
print(all_data)
# Low and High are in STEPS, not volts, we have 0.2 steps so low 5 = 1 volt
# Use this to look at different sections of the graph.
low = 0
high = len(all_data)-1
print(len(all_data))
Period = scale*(high-low)

# Set up Arrays of the independent and dependent variables from all_data
x = np.array([scale*i for i in range(low,high)])
y = np.array([all_data[i] for i in range(low,high)])

######## This is Fourier Series stuff, which I stopped using, but keeping it here as a comment.
# NumberofTerms of the fourier series you want.
NumberofTerms = 400
# This calculates a_n for the cos term and b_n for the sin term. Also the constant out front.
a = np.array([(scale*2/Period)*np.sum(np.cos(2*np.pi*i*x/Period)*y) for i in range(NumberofTerms)])
b = np.array([(scale*2/Period)*np.sum(np.sin(2*np.pi*i*x/Period)*y) for i in range(NumberofTerms)])
Const = a[0]/2
# A function which calculates "NumberofTerms" functions and sums them up to get your total fourier series.
def f(M, Nh):
  f = np.array([a[i]*np.cos(2*np.pi*i*M/Period)+b[i]*np.sin(2*np.pi*i*M/Period) for i in range(1,Nh)])
  return f.sum()+Const
# Create a linespace from this new function to use for graphing.
x2 = scale*np.linspace(low,high,1000)
y2 = np.array([f(t,NumberofTerms) for t in x2])
print(x2, y2)
###########################################################################################

    
# Plot the different graphs we calculated.
plt.plot(x,y, label = 'Raw Data')
plt.plot(x2,y2, label = 'Fourier Series')

# Populate Labels and other info
plt.title("Fourier Series of Discrete Data")
plt.xlabel("Independent")
plt.ylabel("Dependent")
axes = plt.gca()
plt.legend()

