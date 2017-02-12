import numpy as np

def getWaveEnd(waveStart):
	return waveStart + 120
	
def getPhaseData(wave,waveStart,waveEnd):
	windowSize = waveEnd-waveStart
	maxTau = np.floor(windowSize/2)
	maxTau = int(maxTau)
	acWave = AutoCorFcn(wave[waveStart:waveEnd],maxTau)
	crossX = np.where(np.diff(np.sign(acWave)))[0]
	if crossX is None:
		tauX = np.floor(maxTau*0.8)
	else:
		tauX = crossX[0]+1
	tauX = int(tauX)
	x,y = getPhaseSpace(wave[waveStart:waveEnd],tauX)
	return (x,y,tauX)
	
def AutoCorFcn(wave,maxTau):
	N = wave.size
	C = np.empty(maxTau)
	for i in range(0,maxTau):
		a = np.reshape(wave[:N-i],[1,-1])
		b = np.reshape(wave[i:],[1,-1])
		r = np.corrcoef(a,b)
		C[i]=r[0,1]
	return C
	
def slidePhaseSpace(wave, waveStart, numPoints, tauX):
	numPoints = abs(numPoints)
	x=np.empty(numPoints)
	y=np.empty(numPoints)
	for i in range(0,numPoints):
		x[i] = wave[waveStart+i]
		y[i] = wave[waveStart+i+tauX]
	return(x,y)
	
def getPhaseSpace(wave,tauX):
	dim=2
	N = wave.size
	T = N-(dim-1)*tauX
	x=np.empty(T)
	y=np.empty(T)
	for i in range(0,T):
		x[i] = wave[i]
		y[i] = wave[i+tauX]
	return (x,y)
