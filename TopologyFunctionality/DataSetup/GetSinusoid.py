import numpy

def getSinusoid(frequency, sampleRate, amplitude, delay, range):
	time = numpy.arange(delay,range+delay)
	wave = amplitude * [numpy.sin(2*numpy.pi*frequency * (i/sampleRate)) for i in numpy.arange(sampleRate*range)]
	wave = list(wave)
	return wave