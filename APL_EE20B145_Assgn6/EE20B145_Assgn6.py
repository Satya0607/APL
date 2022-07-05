from pylab import *
import scipy.signal as sp 
import numpy as np

#Defining function which returns the transfer function for arbitrary values of decay and frequency
def tran_fun(fre,decay):
    pol =  np.polymul([1.0,0,2.25],[1,2*decay,fre*fre + decay*decay]) #multiplying two polynomials
    return sp.lti([1,decay],pol) #dividing two polynomials
#Question1
#Decay is 0.5
t1,x1 = sp.impulse(tran_fun(1.5,0.5),None,np.linspace(0,50,5001)) #This computes the impulse response of transfer function
figure(0)
#plot
plot(t1,x1)
title("The time response of the spring with decay of 0.5")
xlabel(r'$t\rightarrow$')
ylabel(r'$x(t)\rightarrow$')
grid(True)

#Question 2
#Decay is 0.05
t2,x2 = sp.impulse(tran_fun(1.5,0.05),None,np.linspace(0,50,5001)) #This computes the impulse response of transfer function
figure(1)
#plot
plot(t2,x2)
title("The time response of the spring with decay of 0.05")
xlabel(r'$t\rightarrow$')
ylabel(r'$x(t)\rightarrow$')
grid(True)

#Question 3
H = sp.lti([1],[1,0,2.25])    #Transfer function
for w in arange(1.4,1.6,0.05): #varying frequency from 1.4 to 1.6 in steps of 0.05
	t = linspace(0,50,500)
	f = cos(w*t)*exp(-0.05*t)
	t3,x3,svec = sp.lsim(H,f,t)  #This stimulates the convolution of f and h

# The plot of x(t) for various frequencies vs time.
	figure(2)
	plot(t3,x3,label='w = ' + str(w))
	title("x(t) for different frequencies")
	xlabel(r'$t\rightarrow$')
	ylabel(r'$x(t)\rightarrow$')
	legend(loc = 'upper left')
	grid(True)
#Question 4
# We are given two set of equations, we have to solve those equations in s domain and convert it into time domain
#function x in laplace domain
X4 = sp.lti([1,0,2],[1,0,3,0])
#function of y in laplace domain
Y4 = sp.lti([2],[1,0,3,0])
#In time domain
t4,x4 = sp.impulse(X4,None,linspace(0,20,500))
t4,y4 = sp.impulse(Y4,None,linspace(0,20,500))
#plot
figure(3)
plot(t4,x4,label='x(t)')
plot(t4,y4,label='y(t)')
title("x(t) and y(t)")
xlabel(r'$t\rightarrow$')
ylabel(r'$functions\rightarrow$')
legend(loc = 'upper right')
grid(True)

#Question 5
#To plot magnitude and phase response of steady state transfer function given two port network
L = 1e-6
C = 1e-6
R = 100
H5 = sp.lti([1],[L*C,R*C,1])
w,S,phi = H5.bode()
#magnitude plot
figure(4)
semilogx(w,S)
title("Magnitude Bode plot")
xlabel(r'$\omega\rightarrow$')
ylabel(r'$20\log|H(j\omega)|\rightarrow$')
grid(True)
#phase plot
figure(5)
semilogx(w,phi)
title("Phase Bode plot")
xlabel(r'$\omega\rightarrow$')
ylabel(r'$\angle H(j\omega)\rightarrow$')
grid(True)

#Question 6
#obtaining the output voltage from given input voltage
t6 = arange(0,10e-3,1e-7)
vi = cos(1e3*t6) - cos(1e6*t6)  #input voltage
t6,vo,svec = sp.lsim(H5,vi,t6)  #stimulates vo = convolution of vi and H5
#plot of vo vs t for large time interval
figure(6)
plot(t6,vo)
title("The Output Voltage for large time interval")
xlabel(r'$t\rightarrow$')
ylabel(r'$V_o(t)\rightarrow$')
grid(True)
#plot of vo vs t for small time interval
#Here we are taking first 300 terms ie., 0<t<300*10^-7 == 0<t<30micro
figure(7)
plot(t6[0:300],vo[0:300])
title("The Output Voltage for small time interval")
xlabel(r'$t\rightarrow$')
ylabel(r'$V_o(t)\rightarrow$')
grid(True)

show()


