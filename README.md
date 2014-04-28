streamingplot
=============
Matplotlib based real time plotting
    
Installation
============
There isn't any. You may want to move the `streamingplot.py` file to somewhere on your `$PATH`, remove the `.py` extension and make it executable. For example:
```
$ cp /path/to/streamingplot.py ~/bin/streamingplot
$ chmod +x ~/bin/streamingplot
```

Documentation
=============
The `streamingplot.py` file contains a class and driver for reading and plotting a stream of incoming data from stdin in real time. Any line beginning with with `PLOT_MARKER` (defaults to `'>>'`) is input to be plotted. Everything else will print to stdout.

The stream can contain data for multiple subplots (separated by `ROW_SEP`) and multiple lines per plot (separated by `COL_SEP`). `ROW_SEP` and `COL_SEP` default to `';'` and `','` respectively. The first line beginning with `PLOT_MARKER` defines the number of plots and number of lines per plot and all other lines are assumed to follow the same format.

Sometimes an example is worth a thousand words. If we wanted to have 3 separate plots having 3, 2, and 4 lines respectively, the input stream should look something like:
```
>> 1, 2, 3; 4, 5; 6, 7, 8, 9;
>> 0.5, 1.5, 2.5; 3.5, 4.5; 5.5, 6.5, 7.5, 8.5;
some status message
>> 0, 1, 2; 3, 4; 5, 6, 7, 8; 
another status message
```

Usage
=====
streamingplot is designed for use within a command line environment. All the following examples assume you've moved `streamingplot.py` somewhere on your `$PATH`, removed the `.py` extension, and made it executable as described in the Installation section above. The simplest use case is
```
$ somedatageneratingprocess | python streamingplot.py
```
Buffering issues with pipes can cause the plot to not show until the the first process finishes. The simplest way to deal with this is use the [expect](http://expect.sourceforge.net/) [unbuffer](http://linuxcommand.org/man_pages/unbuffer1.html) command.
```
$ unbuffer -p somedatageneratingprocess | streamingplot
```
streamingplot also can also save the final image to a file by passing an output file name with an extension supported by your matplotlib install.
```
$ somedatageneratingprocess | streamingplot img.png
```
For a list of available extensions in a python prompt type
```python
>> import matplotlib.pyplot as plt
>> print plt.gcf().canvas.get_supported_filetypes()
```
To specify an alternate `PLOT_MARKER` use `-p`
```
$ somedatageneratingprocess | streamingplot -p 'error ='
```
To specify alternate `ROW_SEP` or `COL_SEP` use `-R` or `-C`
```
$ somedatageneratingprocess | streamingplot -R $'\t' -C ' '
```
To add labels use `-l`
```
$ somedatageneratingprocess | streamingplot -l 'a1, a2, a3; b1, b2; c1'
```
To specify colors use `-c`
```
$ somedatageneratingprocess | streamingplot -l 'r, r, r; b, b; g'
```
To save the plot every time is is updated use the `-a` and an output format string
```
$ somedatageneratingprocess | streamingplot -a ./plots/iteration{0}.png
```
For full usage information type
```
$ streamingplot -h
usage: streamingplot.py [-h] [-p PLOT_MARKER] [-R ROW_SEP] [-C COL_SEP]
                        [-l LABELS] [-c COLORS] [-a]
                        [output]

positional arguments:
  output                output file name

optional arguments:
  -h, --help            show this help message and exit
  -p PLOT_MARKER, --plot-marker PLOT_MARKER
                        string indicating line contains data to plot
                            default: '>'
  -R ROW_SEP, --row-sep ROW_SEP
                        delimits data for different subplots
                            default: ';'
  -C COL_SEP, --col-sep COL_SEP
                        delimits data for the same subplot
                            default: ','
  -l LABELS, --labels LABELS
                        string of labels
                            ';' delimits sets of labels for different subplots
                            ',' delimits different labels
                            example:
                                'a1, a2; b1, b2, b3'
  -c COLORS, --colors COLORS
                        string of colors
                            Uses the same format as labels.
                            Can be any valid matplotlib color.
                            examples:
                                'red, blue; red, blue, green'
                                'r, b; r, b, g'
  -a, --animate         save the plot each time it is updated
                            Requires output which is assumed to be a format
                            string with a single place holder for time.
                            example:
                                './res/img{0}.png'
```
Demo
====
The streamingplot repository also includes a simple script for generating random data for demo purposes. To run the demo 
```
$ python randomstream.py | streamingplot
```

Here's an example of the output ![demo](https://raw.github.com/thomlake/streamingplot/master/demo.gif)


Uncomment different `numlines` definitions in `randomstream.py` to produce different example plots.


TODO
====
- [x] Add legend functionality
- [x] Add support for color specification
- [x] Add support for creating animations

About
-----
streamingplot is just a proof of concept. It works for my own purposes but YMMV. It would be easy to inherit from the `StreamPlotter` class and add needed functionality.

streamingplot is free software licensed under the [GNU General Public License](http://www.gnu.org/licenses/gpl.html).

| author | email |
|:--:| :--: |
| tllake | thom.l.lake@gmail.com |

