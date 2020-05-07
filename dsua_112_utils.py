import datetime
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib
import numpy as np
import io
from PIL import Image


def year_fraction(date):
    start = datetime.date(date.year, 1, 1).toordinal()
    year_length = datetime.date(date.year+1, 1, 1).toordinal() - start
    return date.year + float(date.toordinal() - start) / year_length

def get_curves(gca):
    curves = {curve.get_label(): curve for curve in gca.get_children() if isinstance(curve, matplotlib.lines.Line2D)}
    return curves
    
def get_axes(gca):
    xmin, xmax = gca.xaxis.get_data_interval()[0], gca.xaxis.get_data_interval()[1]
    ymin, ymax = gca.yaxis.get_data_interval()[0], gca.yaxis.get_data_interval()[1]
    return xmin, xmax, ymin, ymax
    
def fill_contour(curve, limits):
    v = curve.get_path().vertices
    xmin, xmax, ymin, ymax = limits
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.fill(v[:,0], v[:,1], 'k')
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    
    buf = io.BytesIO()
    fig.savefig(buf, format = 'png')
    plt.close(fig = fig)
    
    buf.seek(0)
    im = Image.open(buf).convert('L')
    
    r = np.asarray(im).astype(np.float)
    r/=max(r.flat)
    
    return r

def generate_normalized_difference(gca, curve1, curve2):
    limits = get_axes(gca)
    d1 = fill_contour(curve1, limits)
    d2 = fill_contour(curve2, limits)
    return abs(d1-d2)    

def compare_curves_number(diff, value_threshold = 0.75, entry_threshold = 0.25):
    fraction = np.where(diff.flat > value_threshold, 1, 0).sum() / len(diff.flat)
    return fraction > entry_threshold

def compare_curves_chart(diff):
    figd = plt.figure()
    axd = figd.add_subplot(111)

    im = axd.imshow(diff, cmap=cm.gray)
    figd.colorbar(im)
    axd.set_title( "Maximum Difference = %f" % diff.max())

    figd.show()
    