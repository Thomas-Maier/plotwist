
def _format_percentile_label(label):
    label = str(label)
    if label.endswith('1'):
        label += 'st'
    elif label.endswith('2'):
        label += 'nd'
    elif label.endswith('3'):
        label += 'rd'
    else:
        label += 'th'

    return label

# def _get_duration_string(time_seconds):
def _get_duration_string(payload, metric_label, label):
    time_seconds = payload[metric_label][label]
    minutes, seconds = divmod(time_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    ## Weird case in which hours get a minus prepended
    if hours == 0 and minutes == 0:
        hours = abs(hours)
    if hours < 25:
        return '{:.0f}:{:02.0f}:{:02.0f}'.format(hours, minutes, seconds)
    days, hours = divmod(hours, 24)
    if days < 366:
        return '{:.0f}d {:.0f}:{:02.0f}:{:02.0f}'.format(days, hours, minutes, seconds)
    years, days = divmod(days, 365)
    
    return '{:.0f}y {:.0f}d {:.0f}:{:02.0f}:{:02.0f}'.format(years, days, hours, minutes, seconds)

def _get_value(payload, metric_label, label):
    return '{:.0f}'.format(payload[metric_label][label])

class ExtendedBars:
    def __init__(self, bars = None, aux = None):
        self.bars = bars
        self.aux = aux

def _autolabel(ax, rects, rotation = 0, auto_label_size = 8, unit = '', gap_width = 0, axis_scale = None):
    offset = ax.get_xbound()[-1] / 100.
    for rect, value in zip(rects.bars, rects.aux):
        rect_value = rect.get_width()
        ## If axis has log scale, take relative offset instead
        if axis_scale == 'log':
            offset = 0.05 * rect_value
        x_pos = rect_value + offset
        ha = 'left'
        y_pos = rect.get_y() + 0.4*rect.get_height()
        va = 'center'
        ## Skip if position is 0
        if x_pos == 0: continue
        # if value_func is not None:
        #     value = value_func(value)
        #     unit = ''
        # else:
        #     value = '{:.0f}'.format(value)
        # if unit:
        #     value += ' {}'.format(unit)
        ## Set label
        ax.text(x_pos, y_pos, value, ha = ha, va = va, rotation = rotation, size = auto_label_size)
