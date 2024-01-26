import audiobusio
import digitalio
import board
import math
import time
import array


# Remove DC bias before computing RMS.
def mean(values):
    return sum(values) / len(values)


def normalized_rms(values):
    minbuf = int(mean(values))
    samples_sum = sum(
        float(sample - minbuf) * (sample - minbuf)
        for sample in values
    )
    return math.sqrt(samples_sum / len(values))
    
class MIC():
    def __init__(self):
        self.nsamples = 160
        micpwr = digitalio.DigitalInOut(board.MIC_PWR)
        micpwr.direction = digitalio.Direction.OUTPUT
        micpwr.value = True
        time.sleep(0.1)

        self.mic = audiobusio.PDMIn(board.PDM_CLK, board.PDM_DATA, bit_depth=16)
        self.samples = array.array('H',[0]*self.nsamples)

    # Must call this regularly to collect samples
    def record_sample(self):
        self.mic.record(self.samples, self.nsamples)

    def get_volume(self):
        return normalized_rms(self.samples)
