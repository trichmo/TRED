
def Startup():
	frequency = 13
	sampleRate = 20
	range = 5000
	delay = 0
	amplitude=10
	wave = getSinusoid(frequency, sampleRate, range, delay, amplitude)
	frequency = 7
	wave.extend(getSinusoid(frequency, sampleRate, range, delay, amplitude))
	amplitude = 6
	delay = 5
	wave.extend(getSinusoid(frequency, sampleRate, range, delay, amplitude)
	

