import math

def getSinusoid(frequency, sampleRate, range, delay, amplitude):
	secPerSample = 1/sampleRate
	time = (0+delay:secPerSample:range-secPerSample+delay)
	wave = amplitude*math.sin(math.radians(2*pi*frequency*time))