#!/usr/bin/env python
"""
author:
    tllake 
email:
    <thom.l.lake@gmail.com>
date:
    2013.12.25
file:
    streamplot.py
description:
    Class and driver for reading and plotting
    a stream of incoming data in real time.
"""

import sys, random, math, argparse
import matplotlib.pyplot as plt

COLORS = ['aqua', 'black', 'blue', 'fuchsia',
          'gray', 'green', 'lime', 'maroon', 
          'navy', 'olive', 'orange', 'purple', 
          'red', 'silver', 'teal', 'white', 'yellow']

def get_dimensions(n):
    """Find height and width of plot grid. Kinda Hacky"""
    sr = math.sqrt(n)
    h = int(math.ceil(sr))
    w = int(sr)
    if h * w < n:
        w += 1
    return h, w

class Subplot(object):
    """Class for storing subplot configuration and data."""
    def __init__(self, size, labels=None, colors=None):
        self.size = size
        self.labels = labels
        if colors is None:
            self.colors = random.sample(COLORS, size)
        else:
            self.colors = colors
        self.xss = [[] for i in range(size)]
        self.yss = [[] for i in range(size)]
        self.time = 0

    def append(self, data):
        for xs, ys, y in zip(self.xss, self.yss, data):
            xs.append(self.time)
            ys.append(y)
        self.time += 1

    def draw(self, ax):
        for i, (xs, ys, color) in enumerate(zip(self.xss, self.yss, self.colors)):
            try:
                label = self.labels[i]
            except (IndexError, TypeError):
                ax.plot(xs, ys, color=color)
            else:
                ax.plot(xs, ys, color=color, label=label)
                self.labels[i] = '_nolegend_'
                ax.legend(loc='best')

class StreamPlotter(object):
    """Class for representing the entire plot."""
    def __init__(self, subplots):
        self.numplots = len(subplots)
        self.subplots = subplots
        # initialize plot
        fig = plt.figure()
        h, w = get_dimensions(self.numplots)
        self.axs = [fig.add_subplot(h, w, i) for i in range(1, h * w + 1)]
        # turn on interactive mode and show the plot
        plt.ion()
        plt.show()
    
    def append(self, mat):
        """Add data to the subplots. mat is assumed to
        be a jagged iterable of iterables. The jth element
        of the ith iterable is added to the 
        jth line of the ith subplot.
        """
        for subplot, row in zip(self.subplots, mat):
            subplot.append(row)

    def draw(self):
        for subplot, ax in zip(self.subplots, self.axs):
            subplot.draw(ax)
        plt.draw()

def matsplit(string, rowsep=';', colsep=' ', f=None):
    if f is None:
        return [[x.strip() for x in row.strip().split(colsep)] 
                           for row in string.strip().split(rowsep)]
    return [[f(x.strip()) for x in row.strip().split(colsep)] 
                          for row in string.strip().split(rowsep)]

def parseline(line, rowsep=';', colsep=' '):
    try:
        return matsplit(line, rowsep, colsep, f=float)
    except ValueError:
        return []

def streamplot(stream, plotmarker, rowsep, colsep, labelmat=None, colormat=None):
    # priming read
    primed = False
    while not primed:
        line = stream.readline()
        if line.startswith(plotmarker):
            data = parseline(line[len(plotmarker):], rowsep, colsep)
            if not len(data):
                print line
            else:
                subplots = []
                for i, row in enumerate(data):
                    try:
                        labels = labelmat[i]
                    except (IndexError, TypeError):
                        labels = None
                    try:
                        colors = colormat[i]
                    except (IndexError, TypeError):
                        colors = None
                    subplot = Subplot(len(row), labels, colors)
                    subplots.append(subplot)
                plotter = StreamPlotter(subplots)
                plotter.append(data)
                plotter.draw()
                primed = True
        else:
            print line,
    # read data until eof
    line = stream.readline()
    while line:
        line = line.strip()
        if line.startswith(plotmarker):
            data = parseline(line[len(plotmarker):], rowsep, colsep)
            if not len(data): 
                print line
            else:
                plotter.append(data)
                plotter.draw()
        else:
            print line
        line = stream.readline()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('output', nargs='?', 
                        help="output file name")
    parser.add_argument('-p', '--plot-marker', default='>>', 
                        help="string indicating line contains data to plot. Defaults to '>>'")
    parser.add_argument('-R', '--row-sep', default=';',
                        help="delimits data for different subplots. Defaults to ';'")
    parser.add_argument('-C', '--col-sep', default=' ',
                        help="delimits data for the same subplot. Defaults to ' '")
    parser.add_argument('-l', '--labels', default=None, 
                        help="string of labels. \
                              ' ' delimits labels for the same subplot. \
                              ';' delimits lists of subplot labels \
                              example: 'a1 a2; b1 b2 b3'")
    parser.add_argument('-c', '--colors', default=None, 
                        help="string of colors using the same format as labels.\
                              Can be any valid matplotlib color")
    args = parser.parse_args()
    labelmat = None if args.labels is None else matsplit(args.labels)
    colormat = None if args.colors is None else matsplit(args.colors)
    #print args.row_sep, args.col_sep
    #exit()
    try:
        streamplot(sys.stdin, args.plot_marker, args.row_sep, args.col_sep, labelmat, colormat)
    except KeyboardInterrupt:
        pass
    if args.output is not None:
        plt.savefig(args.output)
