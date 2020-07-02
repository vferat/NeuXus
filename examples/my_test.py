import sys

sys.path.append('..')
import numpy as np

from modules.nodes import (filter, io, select, epoching, epoch_function, store, generate, feature, function)

lsl_marker_reception = io.LslReceive('type', 'Markers')
lsl_reception = generate.Generator('simulation', 16, 500)

chans = select.ChannelSelector(lsl_reception.output, 'index', [1, 2, 3, 4])

butter_filter = filter.ButterFilter(chans.output, 8, 12)

time_epoch = epoching.TimeBasedEpoching(butter_filter.output, 0.5, 0.5)
square_epoch = function.ApplyFunction(time_epoch.output, lambda x: x**2)
average_epoch = epoch_function.Average(square_epoch.output)

log_epoch = function.ApplyFunction(average_epoch.output, lambda x: np.log1p(x))
average_epoch1 = epoching.StimulationBasedEpoching(log_epoch.output, lsl_marker_reception.output, 769, 0, 2)
logpower1 = function.ApplyFunction(average_epoch1.output, lambda x: np.log1p(x))
left_features = feature.FeatureAggregator(logpower1.output, '1')
tocsv = store.ToCsv(left_features.output, 'myfile')
average_epoch2 = epoching.StimulationBasedEpoching(log_epoch.output, lsl_marker_reception.output, 770, 0, 2)
logpower = function.ApplyFunction(average_epoch2.output, lambda x: np.log1p(x))
right_features = feature.FeatureAggregator(logpower.output, '0')
tocsv2 = store.ToCsv(right_features.output, 'myfile')
# featurevector = feature.featureMerger(left_features, right_features, ..., n_features)
'''toCSV(featurevector.output)
loaded_model = joblib.load('lda_model.sav')
loaded_model2 = joblib.load('ann_model.sav')
[[CH1, CH2,... CH_n]]
classify(logpower.output,loaded_model)
classify(logpower.output,loaded_model2)'''
