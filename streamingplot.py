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
          'red', 'silver', 'teal', 'yellow']

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
        # make the plots prettier
        for ax in self.axs:
            ax.patch.set_facecolor('0.85')
            if ax.legend_ is not None:
                lg = ax.legend_
                lg.get_frame().set_linewidth(0)
                lg.get_frame().set_alpha(0.5)
        plt.draw()

def matsplit(string, rowsep=';', colsep=',', f=None):
    if f is None:
        return [[x.strip() for x in row.strip().split(colsep)] 
                           for row in string.strip().split(rowsep)]
    return [[f(x.strip()) for x in row.strip().split(colsep)] 
                          for row in string.strip().split(rowsep)]

def parseline(line, rowsep=';', colsep=','):
    try:
        return matsplit(line, rowsep, colsep, f=float)
    except ValueError:
        return []

def streamplot(stream, plotmarker, rowsep, colsep, labelmat=None, colormat=None, animate=False, output=None):
    # priming read
    primed = False
    iteration = 0
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
                if animate: plt.savefig(output.format(iteration))
                iteration += 1 

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
                if animate: plt.savefig(output.format(iteration))
                iteration += 1
        else:
            print line
        line = stream.readline()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('output', nargs='?', 
                        help="output file name")
    hstr = '\n'.join(("string indicating line contains data to plot",
                      "    default: '>'"))
    parser.add_argument('-p', '--plot-marker', default='>>', help=hstr)
    
    hstr = '\n'.join(("delimits data for different subplots",
                      "    default: ';'"))
    parser.add_argument('-R', '--row-sep', default=';', help=hstr)

    hstr = '\n'.join(("delimits data for the same subplot",
                      "    default: ','"))
    parser.add_argument('-C', '--col-sep', default=',', help=hstr)

    hstr = '\n'.join(("string of labels",
                      "    ';' delimits sets of labels for different subplots",
                      "    ',' delimits different labels",
                      "    example:", 
                      "        'a1, a2; b1, b2, b3'"))
    parser.add_argument('-l', '--labels', default=None, help=hstr)

    hstr = '\n'.join(("string of colors",
                      "    Uses the same format as labels.",
                      "    Can be any valid matplotlib color.",
                      "    examples:", 
                      "        'red, blue; red, blue, green'",
                      "        'r, b; r, b, g'"))
    parser.add_argument('-c', '--colors', default=None, help=hstr)

    hstr = '\n'.join(("save the plot each time it is updated",
                      "    Requires output which is assumed to be a format",
                      "    string with a single place holder for time.",
                      "    example:",
                      "        './res/img{0}.png'"))
    parser.add_argument('-a', '--animate', action='store_true', help=hstr)
                        
    args = parser.parse_args()
    if args.animate and args.output is None:
        parser.error('--animate requires an output destination')

    labelmat = None if args.labels is None else matsplit(args.labels)
    colormat = None if args.colors is None else matsplit(args.colors)
    #print args.row_sep, args.col_sep
    #print labelmat
    #exit()
    try:
        streamplot(sys.stdin, 
                   args.plot_marker, 
                   args.row_sep, 
                   args.col_sep, 
                   labelmat,
                   colormat,
                   args.animate,
                   args.output)
    except KeyboardInterrupt:
        pass
    if args.output is not None and not args.animate:
        plt.savefig(args.output)
