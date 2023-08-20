"""
    @author: Matheus José Oliveira dos Santos
    Last Edit: 24/05/2023 by Matheus José Oliveira dos Santos
"""

from datetime import date, timedelta, datetime

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.dates import MonthLocator, YearLocator, DayLocator
import numpy as np
import pandas as pd


class SerieTemporal:

    def __init__(self,dados:pd.DataFrame) -> None:
        self.dados = dados.copy()
        self.meuymax = np.max(self.dados.iloc[:, 1:].values) * 1.03
        self.meuymin = np.min(self.dados.iloc[:, 1:].values) * 0.97
        self.txtXLabel = "Date"
        self.txtYLabel = "NAV"
        self.txtTitle = "Chart"
        self.dLocator = False
        self.mLocator = False
        self.ligarGrid = True
        self.legenda=""
        self.cores = ['b', 'g', 'r','y']
        self.destacarPrimeira = False

    def montar(self) -> None:
        fig = plt.figure(figsize=(8, 5))
        ax = fig.add_subplot(111)

        for i in range(1,self.dados.shape[1]):
            if self.destacarPrimeira:
                ax.plot(self.dados.iloc[:,0],self.dados.iloc[:,i],self.cores[i-1],linewidth = 3)
                self.destacarPrimeira = False
            else:
                ax.plot(self.dados.iloc[:, 0], self.dados.iloc[:, i], self.cores[i - 1])

        plt.xticks(rotation=30)
        ax.set_xlabel(self.txtXLabel)
        ax.set_ylabel(self.txtYLabel)
        ax.set_title(self.txtTitle)
        ax.grid(self.ligarGrid)

        if self.dLocator != False:
            ax.xaxis.set_minor_locator(DayLocator(self.dLocator))
        if self.mLocator != False:
            ax.xaxis.set_major_locator(MonthLocator(self.mLocator))

        ax.set_xlim(xmin=self.dados.iloc[0,0],xmax=self.dados.iloc[-1,0])
        ax.set_ylim(ymin=self.meuymin, ymax = self.meuymax)

        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height*0.25, box.width, box.height*0.75])
        plt.legend(self.legenda,loc = "lower left", bbox_to_anchor=(0,-0.4))

        self.fig = fig
        self.ax = ax

    def salvar(self,filename:str) -> None:
        self.montar()
        self.fig.savefig(filename)

    def mostrar(self) -> None:
        self.montar()
        self.fig.show()