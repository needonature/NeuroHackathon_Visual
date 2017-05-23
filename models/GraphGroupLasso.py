__author__ = 'Haohan Wang'

from numpy import random
import numpy as np

np.set_printoptions(precision=5, suppress=True)  # suppress scientific float notation
import math

# define GcFlasso 0
# define GwFlasso 1
class GFlasso:
    def __init__(self, X=None, y=None, corr_coff=None, beta=None, lambda_flasso=0., gamma_flasso=0., flasso_type=0,
                 edge_vertex_matrix=None, mau=0., alpha_matrix=None, L1=0.):
        self.X = X
        self.y = y
        self.corr_coff = corr_coff
        self.beta = beta
        self.lambda_flasso = lambda_flasso
        self.gamma_flasso = gamma_flasso
        self.flasso_type = flasso_type
        self.edge_vertex_matrix = edge_vertex_matrix
        self.mau = mau
        self.alpha_matrix = alpha_matrix
        self.L = L1

    def setXY(self, X, y):
        self.X = X
        self.y = y
        row = X.shape[1]
        col = y.shape[1]
        self.beta = np.zeros([row, col])
        s= np.linalg.svd(self.X, full_matrices=False)[1]
        L1 = np.max(s)
        L1 = L1*L1
        self.L = L1

    def setGroupFeatureIndex(self, ind):
        '''
        :param ind: a list of indices, for example: [[0, 1, 2], [3, 4, 5, 6, 7], [8, 9]]
        :return: None
        '''
        self.indices = [np.array(a) for a in ind]

    def gflasso_fusion_penalty(self):
        num_rows = self.corr_coff.shape[0]
        num_cols = self.corr_coff.shape[1]
        total_sum = 0.
        sign = 1
        mul_factor = 1
        for i in range(0, num_rows):
            for j in range(0, num_cols):
                if self.corr_coff[i, j] < 0:
                    sign = -1
                elif self.corr_coff[i, j] > 0:
                    sign = 1
                mul_factor = 1
                if self.flasso_type == 1:  # GwFlasso
                    mul_factor = self.corr_coff[i, j]
                total_sum = total_sum + mul_factor * abs(
                    (self.beta[:, i]).sum() - sign * (self.beta[:, j]).sum())  # the order of the algorithm
        return total_sum

    def cost(self):
        return (
            ((self.y - self.X.dot(self.beta)) * (self.y - self.X.dot(self.beta))).sum() +
            self.lambda_flasso * np.sum([np.linalg.norm(self.beta[ind,:], ord=2) for ind in self.indices]) +
            self.gamma_flasso * (self.gflasso_fusion_penalty())  # 1e5
        )

    def get_num_edges(self):
        row = self.corr_coff.shape[0]
        col = self.corr_coff.shape[1]
        num_edges = 0
        for i in range(0, row):
            for j in range(0, col):
                if self.corr_coff[i, j] != 0:
                    num_edges = num_edges + 1
        return num_edges

    def update_edge_vertex_matrix(self):
        self.edge_vertex_matrix = random.random(size=(self.get_num_edges(), self.beta.shape[0]))
        self.edge_vertex_matrix = 2. * self.edge_vertex_matrix - 1
        # self.edge_vertex_matrix=np.zeros((self.get_num_edges(),self.beta.shape[0]))
        num_rows = self.corr_coff.shape[0]
        num_cols = self.corr_coff.shape[1]
        sign = 1
        present_row = 0
        for i in range(0, num_rows):
            for j in range(0, num_cols):
                if self.corr_coff[i, j] == 0:
                    continue
                if self.corr_coff[i, j] < 0:
                    sign = -1
                elif self.corr_coff[i, j] > 0:
                    sign = 1
                for k in range(0, self.beta.shape[0]):
                    if k == i:
                        self.edge_vertex_matrix[present_row, k] = abs(self.corr_coff[i, j]) * self.gamma_flasso
                    elif k == j:
                        self.edge_vertex_matrix[present_row, k] = -sign * abs(self.corr_coff[i, j]) * self.gamma_flasso

                present_row = present_row + 1

    def update_alpha_matrix(self):
        self.alpha_matrix = random.random(size=(self.get_num_edges(), self.beta.shape[1]))
        self.alpha_matrix = 2 * self.alpha_matrix - 1
        self.alpha_matrix = self.edge_vertex_matrix.dot(self.beta)
        self.alpha_matrix = self.alpha_matrix / self.mau
        self.alpha_matrix[self.alpha_matrix > 1.] = 1.
        self.alpha_matrix[self.alpha_matrix < -1.] = -1.

    def gradient(self):
        self.update_edge_vertex_matrix()
        self.update_alpha_matrix()
        return self.X.T.dot(self.X.dot(self.beta) - self.y) + self.edge_vertex_matrix.T.dot(self.alpha_matrix)

    def getL(self):
        return self.L + (self.edge_vertex_matrix * self.edge_vertex_matrix).sum() / self.mau

    def proximal_operator(self, B, f):
        t = f * self.lambda_flasso / self.getL()
        result = np.zeros_like(B)
        for ind in self.indices:
            normTmp = np.linalg.norm(B[ind], ord=2)
            if normTmp > t:
                result[ind] = B[ind] - B[ind]/normTmp

        return result


if __name__ == '__main__':
    pass
