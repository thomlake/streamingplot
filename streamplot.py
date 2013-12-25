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

class StreamPlotter(object):
    """Class for holding data and plotting"""
    def __init__(self, plot_sizes):
        self.plot_sizes = plot_sizes
        self.num_plots = len(plot_sizes)
        self.dataseqs = [[[] for j in range(size)] for size in plot_sizes]
        self.colormat = [random.sample(COLORS, size) for size in plot_sizes]
        # initialize plot
        fig = plt.figure()
        h, w = get_dimensions(self.num_plots)
        self.axs = [fig.add_subplot(h, w, i) for i in range(1, h * w + 1)]
        plt.show(block=False)

    def append(self, mat):
        """Add data to the plots. mat is assumed to
        be a jagged iterable of iterables. The jth element
        of the ith iterable is added to the 
        jth line of the ith plot.
        """
        for subseqs, row in zip(self.dataseqs, mat):
            for seq, x in zip(subseqs, row):
                seq.append(x)

    def draw(self):
        for subseqs, colors, ax in zip(self.dataseqs, self.colormat, self.axs):
            for seq, c in zip(subseqs, colors):
                ax.plot(seq, color=c)
        plt.draw()

def parseline(line):
    try:
        return [[float(x) for x in sub.strip().split(' ')] for sub in line.split(';')]
    except ValueError:
        return []

def streamplot(f):
    # priming read
    primed = False
    while not primed:
        line = f.readline()
        if line.startswith('>>'):
            data = parseline(line[2:])
            if not len(data):
                print line
            else:
                plot_sizes = [len(row) for row in data]
                plotter = StreamPlotter(plot_sizes)
                plotter.append(data)
                plotter.draw()
                primed = True
        else:
            print line,
    # read data until eof
    line = f.readline()
    while line:
        line = line.strip()
        if line.startswith('>>'):
            data = parseline(line[2:])
            if not len(data): 
                print line
            else:
                plotter.append(data)
                plotter.draw()
        else:
            print line
        line = f.readline()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('output', nargs='?')
    args = parser.parse_args()
    try:
        streamplot(sys.stdin)
    except KeyboardInterrupt:
        pass
    if args.output is not None:
        plt.savefig(args.output)
