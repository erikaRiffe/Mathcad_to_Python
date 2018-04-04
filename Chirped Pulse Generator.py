# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 14:58:52 2018

@author: errif
"""
import numpy


sample_rate = 10 #Gs/s
Chirp_Duration = 0.25 #microseconds
Overall_Chirp_Start = 350 #MHz chirp stope 4600
Width = 4250 #MHz pulse width
Chirp_Delay = 2 #microseconds
Ch1_on= 0.4 #microseconds time for tranistion to HI
Ch1_off=1.4
Buffer = 8.75 #microseconds
Overall_Chirp_Stop = Overall_Chirp_Start + Width
waveform_time = Chirp_Delay + Chirp_Duration
if Ch1_off > waveform_time:
    waveform_time = Ch1_off
waveform_time = int(waveform_time + Buffer)
#print(waveform_time)
waveform_points = numpy.ceil((waveform_time*10**-6)*(sample_rate*(10**9)))
#print(waveform_points)

def chirp_pulse(waveform_time,v):
    chirp_pulse = numpy.sin((2*numpy.pi*(v*10**6)*waveform_time)+2*numpy.pi*(Width*10**6)*((waveform_time)**2/(2*Chirp_Duration*10**-6)))
    print(chirp_pulse)
def one_chirp(f):
    N = (Chirp_Duration*10**-6)*(sample_rate*10**9)
    out=[]
    for i in numpy.arange(0,N,1):
        t = 1/(i*(sample_rate*10**9))
        out.append(chirp_pulse(t,f))
        print(out)
def chirp_waveform():
    N_delay = numpy.floor((Chirp_Delay*10**-6)*(sample_rate*10**9))
    for n in range(0,N_delay-1):
        C=[0]
    f=Overall_Chirp_Start
    temp= one_chirp(f)
    C=numpy.column_stack(C,temp)
    start = C.shape[0]-1
    for n in range(start,waveform_points-1):
        C=[0]
    return C
def marker1():
    N_on = numpy.floor((Ch1_on*10**-6)*(sample_rate*10**9))
    N_off =numpy.ceil((Ch1_off*10**-6)*(sample_rate*10**9))
    for n in range(0,N_on-2):
        M=[0]
    for n in range(N_on-1,N_off-1):
        M=[1]
    for n in range(N_off-1,waveform_points-1):
        M=[0]
    return M

#print(chirp_waveform)
        

#chirp_pulse(waveform_time,Overall_Chirp_Start)