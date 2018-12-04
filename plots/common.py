
from __future__ import print_function
from __future__ import unicode_literals
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from collections import OrderedDict
from .utils import _autolabel, _get_value, ExtendedBars


_default_options = {
    'plot': {},
    'legend': {
        'fontsize': 14,
        'bbox_to_anchor': (0., 0.95, 1., .05),
    }
}

def _prepare_data(data):
    prep_data = OrderedDict()
    prep_data['payload'] = OrderedDict()
    prep_data['labels'] = data.keys()
    for prim in data:
        for sub in data[prim]:
            if sub not in prep_data['payload']:
                prep_data['payload'][sub] = OrderedDict()
            prep_data['payload'][sub][prim] = data[prim][sub]

    return prep_data

def _get_count_labels(counts, labels, count_total = None, count_label = '#Jobs', count_value_func = None):
    count_labels = []
    for label in labels:
        count = counts[label]
        if count_value_func is not None:
            count = count_value_func(count)
        if count_total:
            frac = '{:.0f}%'.format(float(count)/count_total * 100.)
            string = '{}: {} ({})'.format(count_label, count, frac)
        else:
            string = '{}: {}'.format(label, count)
        count_labels.append(string)

    return count_labels

def _make_plot(data, count_data = None, bar_width = 0.35, gap_width = 0.1, unit = '', x_label = '', axis_scale = None, tick_label_size = 12, colours = None, value_func = _get_value, **options):
    labels = data['labels']
    payload = data['payload']
    if count_data is not None:
        counts = count_data['counts']
        count_total = count_data['total']
        count_label = count_data['label']
        count_value_func = count_data['value_func']
        count_labels = _get_count_labels(counts, labels, count_total = count_total, count_label = count_label, count_value_func = count_value_func)

    n_entries = len(payload)
    n_values = len(payload[payload.keys()[0]])
    bars_width = n_entries * (bar_width + gap_width)
    step = bars_width + 0.5
    stop = 0.5 + step*n_values
  
    ind = np.arange(0.5, stop, step)
    fig, ax = plt.subplots()
    offset = 0
    rects_list = []
    max_val = 0
    for metric_label in payload:
        colour = None
        if colours:
            colour = colours[metric_label]
        else:
            colour = np.random.rand(3,1)
        values = []
        aux_values = []
        for label in labels:
            values.append(payload[metric_label][label])
            ## Attach auxiliary information, if configured
            if value_func:
                aux = value_func(payload, metric_label, label)
                aux_values.append(aux)
        ## Get the maximum value of all metric entries
        max_values = max(values)
        max_val = max_values if max_values > max_val else max_val
        ## Create horizontal bars
        bars = ExtendedBars()
        bars.bars = ax.barh(ind+offset, values, bar_width, color = colour, label = metric_label)
        if aux_values:
            bars.aux = aux_values
        rects_list.append(bars)
        offset += (bar_width + gap_width)
    ## Scale max value to create margin
    max_val *= 1.1

    if unit and x_label:
        x_label += ' [{}]'.format(unit)

    ## Set ticks
    ax.set_yticks(ind + bars_width/2.)
    ax.set_yticklabels(labels, size = tick_label_size)
    if count_data is not None:
        ax.set_yticks(ind, minor = True)
        ax.set_yticklabels(count_labels, minor = True, size = tick_label_size-4)
    ax.tick_params(axis = 'x', labelsize = tick_label_size)
    if axis_scale is not None: ax.set_xscale(axis_scale)
    ax.set_xlabel(x_label, size = tick_label_size)
    ## Set order or magnitude size
    ax.xaxis.get_offset_text().set_size(tick_label_size-2)
    for rects in rects_list:
        _autolabel(ax, rects, unit = unit, axis_scale = axis_scale, gap_width = gap_width, **options)
    ax.set_xbound(lower = 0, upper = max_val)
    ax.set_ybound(lower = 0, upper = 1.05*(ind[-1]+step))

    return fig, ax

def _add_legend(ax, fontsize = 14, **options):
    ## Add legend to plot
    legend = ax.legend(loc = 3, mode = 'expand', borderaxespad = 0., framealpha = 1., fontsize = fontsize, **options)
    ## Set legend title size
    plt.setp(legend.get_title(), fontsize = fontsize)

def _adapt_plot_ratio(data, options, adapt):
    n_entries = len(data)
    ## Set ratios
    matplotlib.rcParams['figure.figsize'] = adapt['ratio'](n_entries)
    ## Set options
    options['plot'].update(dict(
        tick_label_size = adapt['ticks'](n_entries),
        auto_label_size = adapt['auto'](n_entries),
    ))
    options['legend'].update(dict(
        fontsize = adapt['legend'](n_entries),
    ))
