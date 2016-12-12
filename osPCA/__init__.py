import csv
import datetime
import os
import pandas
import sys
import time
from sklearn.decomposition import PCA
import matplotlib.pyplot
import numpy



DEFAULT_MULTIPLIER = 0.05



def angleBetween(m1, m2):
  return numpy.arctan((m1 - m2) / (1 - m1 * m2))



def sigmoid(t):
  return 1/(1+numpy.exp(-t))



def osPCA(filename, osMultiplier=DEFAULT_MULTIPLIER, plot=False, outp=sys.stdout):
  matplotlib.pyplot.ion()
  data = pandas.read_csv(
    os.path.abspath(os.path.expanduser(filename)),
    parse_dates=[0],
    date_parser=lambda ts: time.mktime(
      datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S").timetuple()),
    header=0
  )

  scores = [0]
  colors = ["k"]

  csvout = csv.writer(outp)
  csvout.writerow(("timestamp","value","anomaly_score","label"))
  outData = data.head(0).values[0].tolist()
  outData[0] = str(datetime.datetime.fromtimestamp(outData[0]))
  csvout.writerow(outData + [0, 0])

  for i in xrange(2, len(data)+1):

    subdata = data[:i]

    repeat = 0.1 * len(subdata)

    outData = subdata[-1:].values[0].tolist()
    outData[0] = str(datetime.datetime.fromtimestamp(outData[0]))

    x = subdata["timestamp"].values
    x_oversampled = numpy.append(x, numpy.repeat(x[-1], repeat))
    x_oversample_centered = x_oversampled - x_oversampled.mean()
    x_centered = x - x.mean()

    y = subdata["value"].values
    y_oversampled = numpy.append(y, numpy.repeat(y[-1], repeat))
    y_oversample_centered = y_oversampled - y_oversampled.mean()
    y_centered = y - y.mean()

    # Oversampled PCA

    ospca = PCA()
    ospca.fit(numpy.array(zip(x_oversample_centered, y_oversample_centered)))

    osSlope = ospca.components_[1][0]

    if i > 2:
      score = sigmoid(100000*angleBetween(osSlope, pcaSlope))
    else:
      score = 0

    scores.insert(i, score)

    pca = PCA()
    pca.fit(numpy.array(zip(x_centered, y_centered)))

    pcaSlope = pca.components_[1][0]

    p_ = numpy.percentile(scores, 100 * (1 - osMultiplier))
    if score > p_:
      colors.insert(i, "r")
      label = 1
    else:
      colors.insert(i, "k")
      label = 0

    csvout.writerow(outData + [float(score), label])

    if plot:
      matplotlib.pyplot.clf()
      matplotlib.pyplot.scatter(x_centered, y_centered, c=colors)
      matplotlib.pyplot.plot(x_centered, x_centered * osSlope, "r")
      matplotlib.pyplot.plot(x_centered, x_centered * pcaSlope, "g")
      matplotlib.pyplot.pause(0.01)

