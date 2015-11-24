import pybrain
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

num_input_neurons = 300
num_hidden_neurons = 100
num_output_neurons = 1
net = buildNetwork(num_input_neurons, num_hidden_neurons, num_output_neurons, bias=True)
print n.activate([1, 2])
ds = SupervisedDataSet(2, 1)
ds.addSample((0, 0), (0,))
ds.addSample((0, 1), (1,))
ds.addSample((1, 0), (1,))
ds.addSample((1, 1), (0,))
trainer = BackpropTrainer(net, ds)
print trainer.train()
print trainer.trainUntilConvergence()
print
