__author__ = 'Haohan Wang'

import numpy as np
from numpy import linalg


class GroupLasso:
    def __init__(self, lam=1., lr=1e8, tol=1e-7):
        self.lam = lam
        self.lr = lr
        self.tol = tol
        self.decay = 0.99
        self.maxIter = 1000

    def setLambda(self, lam):
        self.lam = lam

    def setLearningRate(self, lr):
        self.lr = lr

    def setMaxIter(self, a):
        self.maxIter = a

    def setTol(self, t):
        self.tol = t

    def setGroupFeatureIndex(self, ind):
        '''
        :param ind: a list of indices, for example: [[0, 1, 2], [3, 4, 5, 6, 7], [8, 9]]
        :return: None
        '''
        self.indices = [np.array(a) for a in ind]

    def fit(self, X, y):
        yall = np.copy(y)
        betaAll = np.zeros([X.shape[1], y.shape[1]])
        for i in range(yall.shape[1]):
            y = yall[:, i]
            shp = X.shape
            self.beta = np.zeros([shp[1], 1])
            resi_prev = np.inf
            resi = self.cost(X, y)
            step = 0
            while np.abs(resi_prev - resi) > self.tol and step < self.maxIter:
                keepRunning = True
                resi_prev = resi

                while keepRunning:
                    prev_beta = self.beta
                    pg = self.proximal_gradient(X, y)
                    self.beta = self.proximal_proj(self.beta - pg * self.lr)
                    keepRunning = self.stopCheck(prev_beta, self.beta, pg, X, y)
                    if keepRunning:
                        self.lr = self.decay * self.lr

                step += 1
                resi = self.cost(X, y)

            betaAll[:, i] = self.beta.reshape([shp[1]])
        self.beta = betaAll
        return self.beta

    def cost(self, X, y):
        return 0.5 * np.sum(np.square(y - (np.dot(X, self.beta)).transpose())) + self.lam * np.sum(
            [np.linalg.norm(self.beta[ind], ord=2) for ind in self.indices])

    def proximal_gradient(self, X, y):
        return -np.dot(X.transpose(), (y.reshape((y.shape[0], 1)) - (np.dot(X, self.beta))))

    def proximal_proj(self, B):
        t = self.lam * self.lr
        result = np.zeros_like(B)
        for ind in self.indices:
            normTmp = np.linalg.norm(B[ind], ord=2)
            if normTmp > t:
                result[ind] = B[ind] - B[ind]/normTmp

        return result

    def predict(self, X):
        return np.dot(X, self.beta)

    def getBeta(self):
        return self.beta

    def stopCheck(self, prev, new, pg, X, y):
        if np.square(linalg.norm((y - (np.dot(X, new))))) <= \
                                np.square(linalg.norm((y - (np.dot(X, prev))))) + np.dot(pg.transpose(), (
                                    new - prev)) + 0.5 * self.lam * np.square(linalg.norm(prev - new)):
            return False
        else:
            return True
