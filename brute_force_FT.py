import numpy as np
#import matplotlib as plt
np.set_printoptions(formatter={'float_kind':'{:f}'.format})

MOLNAM = str('OFT')
FID_LEN = 6

PDRO = 27200
GATE_START = 0.9       	#best for med-low, 1.1 is better for high
GATE_STOP = GATE_START + FID_LEN        	#for 6 microsecond FID
SAMPLE_RATE = 40000000000  #40 GHz in Hz
N1 = int(np.floor(GATE_START*SAMPLE_RATE*(10**-6)))
N2 = int(np.floor(GATE_STOP*SAMPLE_RATE*(10**-6)))


chirp1 = np.fromfile("OFT_high_250M_4mT-12C_chirp0.csv",sep = " ")
#print(chirp1[0])
chirp2 = np.fromfile("OFT_high_250M_4mT-12C_chirp1.csv",sep = " ")
#print(chirp2[0])
blank1 = np.fromfile("OFT_high_250M_4mT-12C_blank0.csv",sep = " ")
blank2 = np.fromfile("OFT_high_250M_4mT-12C_blank1.csv",sep = " ")

chirps = np.add(chirp1,chirp2)
print("Chirps added")
blanks = np.add(blank1,blank2)
print("Blanks added")
full_FID = np.subtract(chirps, blanks)
print("Chirps and blanks combined")
full_FID = chirp1

CUT = full_FID[N1:N2]
print("FID cut")
CUT_blanks = blanks[N1:N2]
Npts = CUT.size
print('Npts=')
print(Npts)
Kaiser = np.kaiser(Npts,9.5)
NoWindow = np.full(Npts,1)

def Correct_FID_Length_Window(FID,Window): #this operatioin is zero filling to boost resoltuion at minimal cost of intensity
	Npts = FID.size
	Nfid = np.ceil(np.log2(Npts))+4
	Nnew = np.power(2,Nfid)
	New_FID = np.multiply(FID, Window)
	Nbuffer = int(Nnew - Npts)
	Zerofill = np.zeros(Nbuffer)
	FID_buffer = np.concatenate((New_FID, Zerofill), axis=0)
	return FID_buffer

def Freq_Spectrum(FID,sample):
	ftcalc = np.fft.fft(FID)
	ftcalc = np.absolute(ftcalc)
	NumFreq = ftcalc.size
	Freq = np.zeros(NumFreq)
	for m in range(NumFreq-1):
        Freq[m]=PDRO-((m*sample)/FID.size)*(10**-6)
	Ft = np.column_stack((Freq,ftcalc))
	Ft = np.flip(Ft, 0)
	return Ft


#FID_None = Correct_FID_Length_Window(CUT,NoWindow)  
FID_Kaiser = Correct_FID_Length_Window(CUT,Kaiser)
print("close")
#Spectrum_None = Freq_Spectrum(FID_None,SAMPLE_RATE)
Spectrum_Kaiser = Freq_Spectrum(FID_Kaiser,SAMPLE_RATE)
#print(Spectrum_None)
print("Fted! Now writting")

#np.savetxt(MOLNAM+'.txt', Spectrum_None, delimiter=', ')
#np.savetxt('OFTFFT.txt', Spectrum_None, fmt='%.16f', delimiter=', ')
#np.savetxt('OFTFFT.txt', Spectrum_None, delimiter=', ')
np.savetxt(MOLNAM+'_FFT.txt', Spectrum_Kaiser, delimiter=', ')
print("written!")


Blank_Kaiser = Correct_FID_Length_Window(CUT_blanks,Kaiser)
print("close")
Blank_Kaiser = Freq_Spectrum(Blank_Kaiser,SAMPLE_RATE)
print("Blank Fted! Now writting")
np.savetxt(MOLNAM+'_Blank_FFT.txt', Blank_Kaiser, delimiter=', ')
print("Blank written!")


print("done!")



 
