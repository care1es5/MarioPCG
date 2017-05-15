import code
import numpy
import math
import os
import random
from keras.models import Sequential
from keras.layers import Dropout
from keras.layers import Dense
from keras.layers import LSTM
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.cross_validation import train_test_split
from sklearn.metrics import mean_squared_error

MAP_HEIGHT = 12

def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return numpy.array(dataX), numpy.array(dataY)

def col_translation(col_string):
	return col_string.replace("-", "0").replace("#", '1').replace("?", '2')

def col_to_array(col_string):
	return [{'-': numpy.float64(0.0),
			 '?': numpy.float64(0.5),
			 '#': numpy.float64(1.0)}[c] for c in col_string]

def build_tick_training_array(button_presses, map_data, starting_index = 0, ending_index = MAP_HEIGHT):
	arr = []
	for button in button_presses:
		arr.append(button)
	for tile in map_data[starting_index:MAP_HEIGHT]:
		arr.append(tile)
	return arr

def build_col_array(map_data, starting_index = 0, ending_index = MAP_HEIGHT):
	arr = []
	for tile in map_data[starting_index:ending_index]:
		arr.append(tile)
	return arr

button_presses = []
uncleaned_dataset = []

end_indices = []
for fn in os.listdir("./data_set_processed/"):
	if fn == "rnn.py" or fn == "classifier" or fn == 'trainer.py':
		continue

	skip = random.choice([False,False,False,False,True])
	if skip:
		print("Skipping {0}".format(fn))
		continue
	cf = ""
	with open("./data_set_processed/" + fn, "r") as f:
		cf = f.read()
	ticks = cf.split("\n")
	print(fn)
	parsed_ticks = []
	for tick in ticks[15:]:
		if tick == "":
			print("Empty")

		else:
			b_presses = []
			tiles = []
			tickarr = tick.split("\t")
			mario = {"ticknum":int(tickarr[0]),
                    "left":int(tickarr[1][0]),
                     "right":int(tickarr[1][1]),
                     "down":int(tickarr[1][2]),
                     "jump":int(tickarr[1][3]),
                     "speed":int(tickarr[1][4]),
                     "xpos":int(tickarr[2]),
                     "ypos":int(tickarr[3]),
                     "2prev":tickarr[4],
                     "prev":tickarr[5],
                     "curr":tickarr[6],
                     "next":tickarr[7]}

			b_presses.append(mario['left'])
			b_presses.append(mario['right'])
			b_presses.append(mario['down'])
			b_presses.append(mario['jump'])
			b_presses.append(mario['speed'])
			button_presses.append(b_presses)
			col_array = col_to_array(mario['curr'])
			for tile in col_array:
				tiles.append(tile)

			#uncleaned_dataset.append(int(col_translation(mario['curr']), 3))

			next_col_array = col_to_array(mario['next'])
			for tile in next_col_array:
				tiles.append(tile)
			uncleaned_dataset.append(tiles)
			#uncleaned_dataset.append(int(col_translation(mario['next']), 3))
	end_indices.append(len(uncleaned_dataset))


print(uncleaned_dataset[:MAP_HEIGHT*2*5])
print(len(uncleaned_dataset))
print(button_presses[:5*5])
print(end_indices)

input("Press enter to continue.")
numpy.random.seed(7)

train = None

scaler = MinMaxScaler(feature_range=(0, 1))
#dataset = scaler.fit_transform(uncleaned_dataset)
dataset = numpy.array(uncleaned_dataset)
button_dataset = scaler.fit_transform(button_presses)

print(dataset)
print(len(dataset))
input("Press enter to continue.")

trainX = []
trainY = []
for i, index in enumerate(end_indices):
	print("Creating training sets for run")
	prev = end_indices[i-1] if i-1>=0 else 0
	print(prev)
	print(index)
	for y in range(int(prev) + 2, int(index)):
		pprev_buttons = button_dataset[y-2]
		pprev_map = dataset[y-2]
		pprev_arr = build_tick_training_array(pprev_buttons, pprev_map)
		prev_buttons = button_dataset[y-1]
		prev_map = dataset[y-1]
		prev_arr = build_tick_training_array(prev_buttons, prev_map)
		curr_buttons = button_dataset[y]
		curr_map = dataset[y]
		curr_arr = build_tick_training_array(prev_buttons, prev_map)

		next_arr = build_col_array(dataset[y], starting_index=MAP_HEIGHT, ending_index = MAP_HEIGHT*2)
		trainX.append([pprev_arr, prev_arr, curr_arr])
		trainY.append(next_arr)

trainX = numpy.array(trainX)
trainY = numpy.array(trainY)

print(trainX)
print(trainY)
print(len(trainX))
print(len(trainY))
input("Press enter to continue.")
#code.interact(local=dict(globals(), **locals()))

loop_back = 3
trainX = numpy.reshape(trainX, (trainX.shape[0], trainX.shape[1], 17))

#code.interact(local=dict(globals(), **locals()))
model = Sequential()
model.add(LSTM(128, input_shape=(loop_back, 17)))
model.add(Dropout(0.2))
model.add(Dense(12, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
model.fit(trainX, trainY, epochs = 10, batch_size = 1, verbose = 2, shuffle=True)
model.save('trained6.h5')

trainPredict = model.predict(trainX)

code.interact(local=dict(globals(), **locals()))
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainY])

print(trainPredict)
print(trainY)
code.interact(local=dict(globals(), **locals()))
#trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
#print('Train Score: %.2f RMSE' % (trainScore))

