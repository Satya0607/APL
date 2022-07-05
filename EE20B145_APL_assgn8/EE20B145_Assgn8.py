from pylab import *
#defining a function
def Dft(function, N, range, x_lim,name):
    t = linspace(-range, range, N + 1)
    t = t[:-1]
    y = function(t)
    Y = fftshift(fft(y))/N
    w = linspace(-64, 64, N + 1) 
    w = w[:-1]
    if(name =="gauss"): 
        Y = fftshift(abs(fft(y)))/N
        Y = Y*sqrt(2*pi)/max(Y)
        Y0 = exp(-w**2/2)*sqrt(2*pi)
        print("maximum error is {} at time range={} and period={}".format(abs(Y-Y0).max(),format(2*range),format(N)))
    figure()
    subplot(2, 1, 1) #subplots are used to represent sub figures in same picture
    plot(w, abs(Y), lw = 2)
    xlim([-x_lim, x_lim])
    ylabel(r"$|y|$", size = 16)
    title(r"Spectrum of ${}$".format(name))
    grid(True)
    subplot(2,1,2)
    ii=where(abs(Y)>1e-3)
    if(name!="cos(20t+5cos(t))"):
        plot(w,angle(Y),'ro',lw=2)
    plot(w[ii],angle(Y[ii]),'go',lw=2)
    xlim([-x_lim, x_lim])
    ylabel(r"Phase of $Y$",size=16)
    xlabel(r"$k$",size=16)
    grid(True)
    savefig("plot{}.png".format(fignum[0]))
    fignum[0] += 1
    show()
fignum = [0]
#questions
Dft(lambda x : sin(5*x), 256, 2*pi, 15,"sin(5t)")    #lambda is used to identify the required function 
Dft(lambda x : (1 + 0.1 * cos(x))*cos(10*x), 512, 4*pi, 15,"(1 + 0.1cos(t))cos(10t)")
Dft(lambda x : cos(x)**3, 512, 4*pi, 15,"cos^3(t)")
Dft(lambda x : sin(x)**3,512, 4*pi, 15,"sin^3(t)")
Dft(lambda x : cos(20*x+5*cos(x)),512, 4*pi, 40,"cos(20t+5cos(t))")
Dft(lambda x : exp(-x**2/2),512, 4*pi, 10,"gauss")
Dft(lambda x : exp(-x**2/2),512, 6*pi, 10,"gauss")
Dft(lambda x : exp(-x**2/2),512, 8*pi, 15,"gauss")
Dft(lambda x : exp(-x**2/2),256, 4*pi, 10,"gauss")
Dft(lambda x : exp(-x**2/2),1024, 4*pi, 10,"gauss")