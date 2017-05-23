__author__ = 'Haohan Wang'

import sys
sys.path.append('../')

from models.GroupLasso import GFlasso
from models.Lasso import Lasso
from models.ProximalGradientDescent import ProximalGradientDescent

import numpy as np

if __name__ == '__main__':
    X = None # features
    Y = None # responses)

    learningRate = 1e-3
    lam = 1

    ###############################################
    # Vanilla Lasso Example

    model = Lasso(lam=lam, lr=learningRate)
    model.fit(X, Y)
    beta = model.getBeta()

    ###############################################
    # Graph-fused Lasso example
    pgd = ProximalGradientDescent(learningRate=learningRate)
    model = GFlasso(lambda_flasso=lam, gamma_flasso=0.5, mau=0.1)

    # Set X, Y, correlation
    model.setXY(X, Y)
    graph_temp = np.cov(Y.T)
    graph = np.zeros((Y.shape[1], Y.shape[1]))
    for i in range(0, Y.shape[1]):
        for j in range(0, Y.shape[1]):
            graph[i, j] = graph_temp[i, j] / (np.sqrt(graph_temp[i, i]) * (np.sqrt(graph_temp[j, j])))
            if (graph[i, j] < 0.5):
                graph[i, j] = 0
    model.corr_coff = graph

    pgd.run(model)
    beta = model.beta