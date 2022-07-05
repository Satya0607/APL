from pylab import *
import scipy.special as sp


def g(t, A, B):
    y = A * sp.jn(2, t) + B * t
    return y


# QUESTION 2

N = 101
k = 9
data = []
t = loadtxt('fitting.dat', usecols=0)

for i in range(1, 10):
    data.append(loadtxt('fitting.dat', usecols=i))

sigma = logspace(-1, -3, 9)

y = g(t, 1.05, -0.105)

# QUESTION 3 & 4

for i in range(0, 9):
    figure(0)
    plot(t, data[i], label="sigma" + str(i + 1) + " = " + str(sigma[i].round(3)))
plot(t, y, label='True Value', color='black')
grid(True)
legend(loc='upper right')
xlabel(r'$t$', size=20)
ylabel(r'$f(t)+noise$', size=20)
title(r'Data to be fitted to the theory')

# QUESTION 5

figure(1)
stdev = std(data[0])
errorbar(t[::5], data[0][::5], sigma[0], fmt='ro', label='Error bar')
plot(t, y, label='True value', color='black')
xlabel(r'$t$', size=20)
title(r'Data points for sigma = ' + str(sigma[0]) + ' along with exact function')
grid(True)

# QUESTION 6

J = sp.jn(2, t)
M = c_[J, t]
A0 = 1.05
B0 = -0.105
coeff = array([A0, B0])
g1 = M.dot(coeff)
if (array_equal(g1, g(t, A0, B0))):
    print("Both arrays are same")

# QUESTION 7 & 8

A = arange(0, 2, 0.1)
B = arange(-0.2, 0, 0.01)
error = array([zeros(len(A))] * len(B))
for i in range(0, len(A)):
    for j in range(0, len(B)):
        error[i][j] = square(data[0] - g(t, A[i], B[j])).mean()
figure(2)
W = contour(A, B, error)
clabel(W, inline=True, fontsize=10)
Min = error.min()
for i in range(0, len(A)):
    for j in range(0, len(B)):
        if (error[i][j] == Min):
            figure(2)
            scatter(A[i], B[j], color='red', label='Exact location')
            print("The Minimum Error occurs at points A = %f  B = %f " % (A[i], B[j]))
AErr = zeros(9)
BErr = zeros(9)
xlabel(r'$A$', size=20)
ylabel(r'$B$', size=20)
title(r'Contour plot of Error')
legend()

# QUESTION 9 & 10

for i in range(0, len(data)):
    AErr[i] = abs(linalg.lstsq(M, data[i])[0][0] - coeff[0])
    BErr[i] = abs(linalg.lstsq(M, data[i])[0][1] - coeff[1])
figure(3)

plot(sigma, AErr, label='AErr', linestyle='--', marker='o', color='r')
plot(sigma, BErr, label='BErr', linestyle='--', marker='o', color='g')

legend(loc='upper left')
grid(True)
xlabel(r'Noise standard deviation')
ylabel(r'MS Error')
title(r'Variation of error with noise')

# QUESTION 11
figure(4)
loglog(sigma, AErr, 'ro', label='AErr')
loglog(sigma, BErr, 'go', label='BErr')
errorbar(sigma, AErr, sigma, fmt='ro')
errorbar(sigma, BErr, sigma, fmt='go')
legend(loc='upper left')

xlabel(r'Noise standard deviation')
ylabel(r'MS Error')
title(r'Variation of error with noise')
grid(True)
show()
