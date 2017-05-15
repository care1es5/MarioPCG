import code
import numpy
import math
import os
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return numpy.array(dataX), numpy.array(dataY)

def col_translation(col_string):
	return col_string.replace("-", "0").replace("#", '1').replace("?", '2')

uncleaned_dataset = []

end_indices = []
for fn in os.listdir("./data_set_processed/"):
	if fn == "rnn.py" or fn == "classifier" or fn == 'trainer.py':
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

			uncleaned_dataset.append(int(col_translation(mario['curr']) + tickarr[1], 3))
			uncleaned_dataset.append(int(col_translation(mario['next']), 3))
	end_indices.append(len(uncleaned_dataset))


print(uncleaned_dataset)
print(len(uncleaned_dataset))
print(end_indices)

input("Press enter to continue.")
numpy.random.seed(7)

train = None

scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(uncleaned_dataset)
#dataset = uncleaned_dataset
print(dataset)
print(len(dataset))
input("Press enter to continue.")

trainX = []
trainY = []
counter = 0
for i, index in enumerate(end_indices):
	print("Creating training sets for run")
	prev = end_indices[i-1] if i-1>=0 else 0
	print(prev)
	print(index)
	for y in range(int(prev/2) + 2, int(index/2)):
		trainX.append([dataset[(y-2)*2], 
					   dataset[(y-1)*2], 
					   dataset[(y)*2]])
		trainY.append(dataset[y*2+1])

trainX = numpy.array(trainX)
trainY = numpy.array(trainY)

print(trainX)
print(trainY)
print(len(trainX))
print(len(trainY))
input("Press enter to continue.")

loop_back = 3
trainX = numpy.reshape(trainX, (trainX.shape[0], trainX.shape[1], 1))

code.interact(local=dict(globals(), **locals()))

model = Sequential()
model.add(LSTM(4, input_shape=(loop_back, 1)))
model.add(Dense(1))
model.compile(loss='sparse_categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

model.fit(trainX, trainY, epochs = 10, batch_size = 1, verbose = 2, shuffle=True)
model.save('trained2.h5')
trainPredict = model.predict(trainX)

trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainY])

print(trainPredict)
print(trainY)
#trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
#print('Train Score: %.2f RMSE' % (trainScore))

