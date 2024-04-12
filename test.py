from neuxus.nodes import correct, io, filter, select, read

data_path = r'C:\Users\Victor\Documents\GitHub\neuxus_test\P05_eyes_open_mrion.vhdr'

fs = 5000
tr = 1.3
# signal = io.RdaReceive(rdaport=51244)
# signal = io.LslReceive('name', 'MNE-LSL-Player', 'signal')
signal = read.Reader(data_path)

signal_ga = correct.GA(signal.output, marker_input_port=signal.marker_output, fs=fs, tr=tr, start_marker=['Stimulus/S128'])  # 'Response/R128' is the marker of the start of every MRI volume (in case the data is read from a Brain Vision file; in case it's streamed by Brain Vision Recorder, it is 'R128')

signal_ds = filter.DownSample(signal_ga.output, int(5000 / 250))
signal_ga_lsl = io.LslSend(signal_ga.output, 'corrected', type='EEG')
