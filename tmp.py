import cv2
from scipy import fftpack
from scipy.optimize import curve_fit
import numpy as np
import pylab as py

#from scipy.signal import argrelextrema
# Kameraquelle wählen
from scipy.signal import argrelextrema

#Einfügen aus Bilbliothek mit RPI.GPi.GPIO2
import RPI.GPIO as GPIO
import os, time

RECEIVER_PIN = 23 #Verbindung muss aufgebaut werden damit es funktioniert
def callback_func (channel) :
    if GPIO.input (channel) :
        print ("Lichtschranke wurde unterbrochen")

a: int
a=0
while (a<5) :



#Bild aufnehmen
i = None
for i in range(1):
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    cv2.imwrite('DVM22_Penetration_'+str(i+1)+'.jpg', image)
del(camera)

# Bild einlesen und grau skalieren
img = cv2.imread('DVM22_Penetration_1.jpg', cv2.IMREAD_GRAYSCALE)

#shift + Transformation
F = fftpack.fftshift(fftpack.fft2(img))
psd2D = np.abs(F) ** 2

def radial_profile(data, center):
    y,x = np.indices((data.shape)) # first determine radii of all pixels
    r = np.sqrt((x-center[0])**2+(y-center[1])**2)
    ind = np.argsort(r.flat) # get sorted indices
    sr = r.flat[ind] # sorted radii
    sim = data.flat[ind] # image values sorted by radii
    ri = sr.astype(np.int32) # integer part of radii (bin size = 1)
    # determining distance between changes
    deltar = ri[1:] - ri[:-1] # assume all radii represented
    rind = np.where(deltar)[0] # location of changed radius
    nr = rind[1:] - rind[:-1] # number in radius bin
    csim = np.cumsum(sim, dtype=np.float64) # cumulative sum to figure out sums for each radii bin
    tbin = csim[rind[1:]] - csim[rind[:-1]] # sum for image values in radius bins
    radialprofile = tbin/nr # the answer
    return radialprofile

psd1D = radial_profile(psd2D, np.shape(psd2D))

py.figure(1)
py.clf()
py.imshow(img, cmap = 'gray')
py.title('Input Image'), py.xticks([]), py.yticks([])
#py.savefig('image_fft_examp_image.png')
py.show()

py.subplot(121), py.imshow(np.log10(psd2D), cmap=py.cm.jet)
py.title('2D Power Spectrum')
#py.savefig('image_fft_examp_psd2d.png')

py.subplot(122), py.semilogy(psd1D)
py.title('1D Power Spectrum')
py.xlabel('Spatial Frequency')
py.ylabel('Power Spectrum')
#py.savefig('image_fft_examp_psd1d.png')
py.show()

length_x = np.shape(psd1D)
xdata = np.linspace(0, 1000, num=length_x[0], endpoint=True, retstep=False, dtype=None, axis=0)



def gaussian(x, amp1,cen1,sigma1):
    return amp1*(1/(sigma1*(np.sqrt(2*np.pi))))*(np.exp((-1.0/2.0)*(((x-cen1)/sigma1)**2)))

init_vals= [10e12, 350, 40]

best_vals, covar = curve_fit(gaussian, xdata, psd1D, p0= init_vals)

print(best_vals)

py.semilogy(xdata, psd1D)
py.show()

#maxima = argrelextrema(psd1D, np.greater)

#print(" ")
#print("Ausgabe Maxima")
#print(" ")
#print(maxima)

