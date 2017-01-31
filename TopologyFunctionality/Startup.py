from TopologyFunctionality.DataSetup.GetSinusoid import getSinusoid
import numpy as np

def Startup():
	frequency = 13
	sampleRate = 300
	range = 1000
	delay = 0
	amplitude=10
	wave = getSinusoid(frequency, sampleRate, amplitude, delay, range)
	frequency = 7
	wave.extend(getSinusoid(frequency, sampleRate, amplitude, delay, range))
	amplitude = 6
	delay = 5
	wave.extend(getSinusoid(frequency, sampleRate, amplitude, delay, range))
	noise = np.random.normal(0,0.1,len(wave))
	wave = wave+noise
	return wave

