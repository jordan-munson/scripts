# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 09:48:33 2019

@author: riptu
"""

import pandas as pd
import numpy as np

concArray = np.empty((24,90, 90))

df = pd.DataFrame(columns=['Column','Row','Metric','Seasonal Metric','Annual Metric','Values'])
