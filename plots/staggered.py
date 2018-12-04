
from __future__ import print_function
from __future__ import unicode_literals
import matplotlib
from .utils import _get_duration_string
from .common import _prepare_data, _make_plot, _add_legend, _adapt_plot_ratio, _default_options

def _ratio_values(n_entries):
    if n_entries < 12:
        return (16, n_entries+1)
    else:
        return (16, 12)

_adapt = {
    'ratio': _ratio_values,
    'ticks': lambda x: 16,
    'auto': lambda x: 12,
    'legend': lambda x: 18,
}

def _setup(data):
    options = dict(_default_options)
    options['legend']['title'] = ''
    ## Set ratio according to number of y-axis entries
    _adapt_plot_ratio(data, options, _adapt)
    ## Prepare data for the plotting
    data = _prepare_data(data)
    ## Additional legend options
    ncol = len(data['payload'])
    options['legend']['ncol'] = ncol

    return data, options

def staggered(data, plot_options = None, legend_options = None, output = None, summary = None):
    data, options = _setup(data)
    ## Overwrite options if any were set
    if plot_options:
        options['plot'].update(plot_options)
    if legend_options:
        options['legend'].update(legend_options)
    fig, ax = _make_plot(data, **options['plot'])
    _add_legend(ax, **options['legend'])
    if output:
        fig.savefig(output, bbox_inches = 'tight')
    if summary:
        summary.savefig(fig, bbox_inches = 'tight')
