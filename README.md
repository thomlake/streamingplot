streamplot
==========
Matplotlib based real time plotting
    
Installation
============
There isn't any. You may want to move the streamplot.py file to somewhere on your `$PATH`, remove the `.py` extension and make it executable. For example:

    $ cp /path/to/streamplot.py ~/bin/streamplot
    $ chmod +x ~/bin/streamplot

Usage
=====
streamplot is designed for use within a command line environment. All the following examples assume you've moved streamplot is somewhere on your `$PATH`, removed the `.py` extension, and made it executable as described in the Installation section above. The simplest use case is

    $ somedatageneratingprocess | python streamplot.py

Buffering issues with pipes can cause the plot to not show until the the first process finishes. The simplest way to deal with this is use the [expect](http://expect.sourceforge.net/) [unbuffer](http://linuxcommand.org/man_pages/unbuffer1.html) command.

    $ unbuffer somedatageneratingprocess | streamplot

streamplot also can also save the final image to a file by passing an output file name with an extension supported by your matplotlib install.


    $ somedatageneratingprocess | streamplot img.png

For a list of available extensions in a python prompt type

    >> import matplotlib.pyplot as plt
    >> print plt.gcf().canvas.get_supported_filetypes()

The streamplot repository also includes a simple script for generating random data for demo purposes. To run the demo 

    $ python randomfeeder.py | streamplot

Uncomment different `numlines` definitions in `randomfeeder.py` to produce different plots.

Documentation
=============
The `streamplot.py` file constains a class and driver for reading and plotting a stream of incoming data in real time. Any line beginning with `'>>'` is input to be plotted. Everything else will print to stdout.

The stream can contain data for multiple plots (separated by `';'`) and multiple lines per plot (separated by spaces `' '`).

Sometimes an example is worth a thousand words. If we wanted to have 3 separate plots having 3, 2, and 4 lines respectively, the input stream should look something like:

    >> 1 2 3; 4 5; 6 7 8 9;
    >> 0.5 1.5 2.5; 3.5 4.5; 5.5 6.5 7.5 8.5;
    some status message
    >> 0 1 2; 3 4; 5 6 7 8; 
    another status message



About
-----
streamplot is just a proof of concept. It works for my own purposes but YMMV. It would be easy to inherit from the `StreamPlotter` class and add needed functionality.

streamplot is free software licensed under the [GNU General Public License](http://www.gnu.org/licenses/gpl.html).

| author | email |
|:--:| :--: |
| tllake | thom.l.lake@gmail.com |

