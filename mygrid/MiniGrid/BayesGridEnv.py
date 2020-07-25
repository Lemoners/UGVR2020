from .BasicGridEnv import BasicGridEnv
from .Generator.BayesGene import BayesGene 
from .Generator.HyperPara import DATA_BEFORE_UPDATE, RANDOM_DATA_BEFORE_UPDATE, RANDOM_PARA_BEFORE_UPDATE, Z_DIM
from .Utils import smooth, average_pooling
import numpy as np


class BayesGridEnv(BasicGridEnv):
    def __init__(self, generator=BayesGene()):
        super(BayesGridEnv, self).__init__(generator=generator)
        # self.generator = generator
        self.this_z = self.generator.z
        self.data = []
        self.random_para = 0
        self.random_data = []
    
    def step(self, action):
        obs, reward, done, info = super().step(action)
        if (done):
            result = 0
            if (info.get("success")):
                result = 1
            self._update_model(result)
        return obs, reward, done, info
    
    def _update_model(self, result):
        if (len(self.data) < DATA_BEFORE_UPDATE):
            self.data.append(result)
        elif (self.random_para < RANDOM_PARA_BEFORE_UPDATE):
            if (len(self.random_data) < RANDOM_DATA_BEFORE_UPDATE):
                self.random_data.append(result)
            else:
                self.generator.update(np.mean(self.random_data))
                self.random_data.clear()
                self.random_para += 1
                self.generator.set_z(np.random.randn(Z_DIM))
        else:
            data = average_pooling(smooth(self.data, 3), 2)
            for d in data:
                self.generator.update(d, z=self.this_z)
            self.generator.update_z()

            # update z
            self.this_z = self.generator.z

            self.data.clear()
            self.random_para = 0
            self.random_data.clear()

    def reset(self):
        return super().reset()
