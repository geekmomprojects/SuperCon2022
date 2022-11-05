import audiobusio
import board
import math


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
class MIC(audiobusio):
    def __init__(self, nsamples=160):
        self.mic = audiobusio.PDMIn(board.PDM_CLK, board.PDM_DATA, frequency=16000, bit_depth=16)
        self.nsamples=nsamples
        self.samples = array.array('H',[0]*self.nsamples)

    # Must call this regularly to collect samples
    def record_sample():
        self.record(self.samples, self.nsamples)

    def get_volume():
        return normalized_rms(self.samples)
