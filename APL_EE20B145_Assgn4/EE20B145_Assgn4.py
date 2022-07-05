from pylab import *
from scipy.integrate import quad
import math
import numpy as np 

#QUESTION 1
#Defining the cos(cos(x)) and exp(x) functions that are periodic with the period 2*pi 
#the defined function can return output to both the scalae and the vector input  

def exp(x):
    return np.exp(x)

def cos(x):
    return np.cos(np.cos(x))

t = linspace(-2*pi,4*pi,401)
Exp = exp(t)
Cos = cos(t)        
Exp2 = exp(t%(2*pi))

figure(1)                                                                          #plotting the original exp(t) function and the exp(t) periodic with the period 2*pi over the interval -4*pi to 2*pi
plt.semilogy(t,Exp,label = 'original_exp(t)')
plt.semilogy(t,Exp2,label = 'periodic_exp(t) with period 2*pi')
plt.grid(True, color = "grey", linewidth = "1.4", linestyle = "--") 
xlabel(r'$t$'     ,size = 20)
ylabel(r'exp($t$)',size = 20)
legend(loc='upper right')
title(r'exponential of $t$ in semilog axis')

figure(2)                                                                          #plotting the function cos(cos(x)) over the interval -4*pi to 2*pi
plot(t,Cos)
plt.grid(True, color = "grey", linewidth = "1.4", linestyle = "--") 
xlabel(r'$t$'          ,size = 20)
ylabel(r'cos(cos($t$))',size = 20)
title(r'cosine of cos(cos($t$)) in linear axis')

#QUESTION 2
def u(x,k):                                                                        #defning the functions that are needed to be integrable
    return np.cos(k*x)*f(x)                                                        #integrating the u(x,k) gives the a_n coefficients of fourier series   
def v(x,k):                                                                         
    return np.sin(k*x)*f(x)                                                        #integrating the u(x,k) gives the b_n coefficients of fourier series
    
coef1 = np.zeros(51)                                                               #arrays to store the coefficients of the two functions
coef2 = np.zeros(51)   
def f(x):
    return exp(x)
for i in range(51):                                                                #integrating the function then scaling and finding the fourier coefficients for exp(x)
    if(i == 0):
        coef1[i] =quad(u,0,2*pi,args=(i))[0]/(2*pi)
    elif(i%2 != 0):
        coef1[i] =quad(u,0,2*pi,args=((i+1)/2))[0]/pi
    elif(i%2 == 0):
        coef1[i] =quad(v,0,2*pi,args=(i/2))[0]/pi
   

def f(x):                                                                         #integrating the function then scaling and finding the fourier coefficients for cos(cos(x))
    return cos(x)
for i in range(51):
    if(i == 0):
        coef2[i] =quad(u,0,2*pi,args=(i))[0]/(2*pi)
    elif(i%2 != 0):
        coef2[i] =quad(u,0,2*pi,args=((i+1)/2))[0]/pi
    elif(i%2 == 0):
        coef2[i] =quad(v,0,2*pi,args=(i/2))[0]/pi

#QUESTION 3 
n = linspace(0,50,51)                                                              #creating the linespace vector for the coefficients   
figure(3)                                                                          #plotting the fourier coefficients of exp(x) on semi-log axis
plt.semilogy((n),abs(coef1),'ro',label = 'fourier_coeff')
plt.grid(True, color = "grey", linewidth = "1.4", linestyle = "--") 
xlabel(r'$n$ ')
ylabel(r'coefficient[$n$] ')
legend(loc='upper right')
title(r'fourier coefficients of $exp(t)$ in the semilog scale')


figure(4)                                                                          #plotting the fourier coefficients of exp(x) on log-log axis 
plt.loglog((n),abs(coef1),'ro',label = 'fourier_coeff')
plt.grid(True, color = "grey", linewidth = "1.4", linestyle = "--") 
xlabel(r'$n$ ')
ylabel(r'coefficient[$n$] ')
legend(loc='upper right')
title(r'fourier coefficients of $exp(t)$ in the loglog scale')


figure(5)                                                                          #plotting the fourier coefficients of cos(cos(x)) on semi-log axis
plt.semilogy((n),abs(coef2),'ro',label = 'fourier_coeff')
plt.grid(True, color = "grey", linewidth = "1.4", linestyle = "--") 
xlabel(r'$n$ ')
ylabel(r'coefficient[$n$] ')
legend(loc='upper right')
title(r'fourier coefficients of $cos(cos(t))$ in the semilog scale')


figure(6)                                                                          #plotting the fourier coefficients of cos(cos(x)) on log-log axis
plt.loglog((n),abs(coef2),'ro',label = 'fourier_coeff')
plt.grid(True, color = "grey", linewidth = "1.4", linestyle = "--") 
xlabel(r'$n$ ')
ylabel(r'coefficient[$n$] ')
legend(loc='upper right')
title(r'fourier coefficients of $cos(cos(t))$ in the loglog scale')


#QUESTION 4    
#finding the fourier coefficients by the least squares method  

x = linspace(0,2*pi,401)                                                            #defining the time space array for the least square method
x = x[:-1] 
b1 = np.exp(x)                                                                      #the source array for the least square matrix
b2 = np.cos(x)
A = np.zeros((400,51))                                                              #the coefficient matrix of the variables for the least square method
A[:,0] = 1                                                                          

for k in range(1,26):                                                               #applying the least squares method
    A[:,2*k-1] = np.cos(k*x) 
    A[:,2*k] = np.sin(k*x)
c1=lstsq(A,b1,rcond = 1)[0]         
c2=lstsq(A,b2,rcond = 1)[0]

#QUESTION 5
n = linspace(0,50,51)                                                               #creating the linespace vector for the coefficients

figure(7)                                                                           #plotting both the fourier coefficients and the least squares coefficients of exp(x) on the semi-log axis
plt.semilogy((n),abs(coef1),'ro',label = 'fourier_coeff')
plt.semilogy((n),abs(c1),'go',label = 'least_sq_coeff')
plt.grid(True, color = "grey", linewidth = "1.4", linestyle = "--") 
xlabel(r'$n$ ')
ylabel(r'coefficient[$n$] ')
legend(loc='upper right')
title(r'fourier coefficients of $exp(t)$ in the semilog scale')

figure(8)                                                                           #plotting both the fourier coefficients and the least squares coefficients of exp(x) on the log-log axis       
plt.loglog((n),abs(coef1),'ro',label = 'fourier_coeff')
plt.loglog((n),abs(c1),'go',label = 'least_sq_coeff')
plt.grid(True, color = "grey", linewidth = "1.4", linestyle = "--") 
xlabel(r'$n$ ')
ylabel(r'coefficient[$n$] ')
legend(loc='upper right')
title(r'fourier coefficients of $exp(t)$ in the loglog scale')

figure(9)                                                                           #plotting both the fourier coefficients and the least squares coefficients of cos(cos(x))on the semi-log axis
plt.semilogy((n),abs(coef2),'ro',label = 'fourier_coeff')
plt.semilogy((n),abs(c2),'go',label = 'least_sq_coeff')
plt.grid(True, color = "grey", linewidth = "1.4", linestyle = "--") 
xlabel(r'$n$ ')
ylabel(r'coefficient[$n$] ')
legend(loc='upper right')
title(r'fourier coefficients of $cos(cos(t))$ in the semilog scale')

figure(10)                                                                           #plotting both the fourier coefficients and the least squares coefficients of cos(cos(x))on the log-log axis
plt.loglog((n),abs(coef2),'ro',label = 'fourier_coeff')
plt.loglog((n),abs(c2),'go',label = 'least_sq_coeff')
plt.grid(True, color = "grey", linewidth = "1.4", linestyle = "--") 
xlabel(r'$n$ ')
ylabel(r'coefficient[$n$] ')
legend(loc='upper right')
title(r'fourier coefficients of $cos(cos(t))$ in the loglog scale')


#QUESTION 6
#finding the error in the fourier coefficients and the least square coefficients
experr = np.zeros(51)
coserr = np.zeros(51)
for i in range(51):                                                                 #finding the error in the coefficients of ourier coefficients and the least square coefficients for exp(x)
    experr[i] = abs(coef1[i] - c1[i]) 
for i in range(51):                                                                 #finding the error in the coefficients of ourier coefficients and the least square coefficients for cos(cos(x))
    coserr[i] = abs(coef2[i] - c2[i])
figure(11)                                                                         #plotting the error in the coefficients  as a function of the coefficient index for the exp(x) and the cos(cos(x))
plot(n,experr,'bo',label = 'error magnitude for the exp($t$)')
plot(n,coserr,'mo',label = 'error magnitude for the cos(cos($t$))')
plt.grid(True, color = "grey", linewidth = "1.4", linestyle = "--") 
legend(loc='upper right')
xlabel(r'$n$',size = 20)
ylabel(r'error_coeff[$n$]',size = 20)
title(r'magnitude error in the coefficients')
  
#finding the maximum value of the error in the coefficients     

#printing the largest error in the coefficients 

print("the largest error in the coefficients of the exp($x$) is %f" %(max(experr))) 
print("the largest error in the coefficients of the cos(cos($x$)) is %f" %(max(coserr)))



#QUESTION 7   
#finding the variation of the function given by the fourier coefficient and the exact function                                                               
Exp2 = np.dot(A,coef1)                                                             #finding the function given by the first 51 fourier coefficients 
Cos2 = np.dot(A,coef2)

t = linspace(0,2*pi,401)
t = t[:-1]
Exp = exp(t)
Cos = cos(t)

figure(12)                                                                          #plotting the variation of the function given by the fourier coefficient and the original exp(x)
plt.semilogy(t,Exp2,'go',label = 'exp(t)_from_fourier')
plt.semilogy(t,Exp,label = 'actual_exp(t)',color = 'black')
plt.grid(True, color = "grey", linewidth = "1.4", linestyle = "--") 
xlabel(r'$t$',size = 20)
ylabel(r'exp($t$) ',size = 20)
legend(loc='upper right')
title(r'variation of the exp($t$)')

figure(13)                                                                         #plotting the variation of the function given by the fourier coefficient and the original cos(cos(x))
plot(t,Cos2,'go',label = 'cos(cos(t))_from_fourier')
plot(t,Cos,label = 'actual cos(cos(t))',color = 'black')
plt.grid(True, color = "grey", linewidth = "1.4", linestyle = "--") 
xlabel(r'$t$',size = 20)
ylabel(r'cos(cos($t$))',size = 20)
legend(loc='upper right')
title(r'variation of cos(cos($t$))')

show()























          
         
       
       
          
       










    
        
