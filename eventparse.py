import re
import copy
import logging
import sys


reload(sys)
sys.setdefaultencoding('utf-8')


def line_to_dict(line):
    # create list of terms to look up
    # iterate through list to extract target data
    # find position of each term, determine length of targets via ';' and '}' for custom dimension.

    def get_time(line):
        stop = '['
        end_pos = line.find(stop) - 1
        return line[:end_pos].strip()

    basic_events_list = [
        'category',
        'action',
        'label',
        'value'
    ]

    line_dict = {}
    line_dict['time'] = get_time(line)

    for event in basic_events_list:
        start_pos = line.find(event + ' = ') + len(event + ' = ')
        end_pos = line.find(';', start_pos)
        event_val = line[start_pos:end_pos].strip()
        if event_val != '(null)':
            line_dict[event] = event_val


    def get_custom_dims_string(line):
        start_pos = line.find('customDimentions = {') + len('customDimentions = {')
        end_pos = line.find('}', start_pos)
        return line[start_pos:end_pos].strip()

    def custom_dims_str_to_dict(dims_str):
        dims_arr = dims_str.split(';')
        customDims = {}

        for dim in dims_arr:
            if dim != '':
                key_start_pos = 1
                key_end_pos = dim.find('"', key_start_pos)

                val_start_pos = dim.find('= ') + len('= ')


                customDims[dim[key_start_pos:key_end_pos].strip()] = dim[val_start_pos:].strip()
        return customDims

    dims_str = get_custom_dims_string(line)

    if dims_str:
        dims_dict = custom_dims_str_to_dict(dims_str)
        for k, v in dims_dict.iteritems():
            line_dict[k] = v

    return line_dict


def parse_events(logs_text):
    print 'running parse_events'
    event_line = False
    output_list = []
    output_str = ''

    for line in logs_text.splitlines():
        # logging.info(line)
        if event_line:
            output_str += line
            if '}' in line:
                event_line = False
                output_list.append(output_str)
                output_str = ''
        elif 'logEventToConsole - category' in line:
            output_str = line
            event_line = True


    event_list = []
    for line in output_list:
        event_list.append(line_to_dict(line))
        # print line_to_dict(line)
        # print '\n'

    final_output_str = ''
    order_list = ['time', 'category', 'action', 'label']

    for event in event_list:
        out_event_dict = copy.deepcopy(event)

        for item in order_list:
            final_output_str += item + ': ' + out_event_dict[item] + '\n'
            print item + ': ' + out_event_dict[item]
            del out_event_dict[item]

        for k, v in out_event_dict.iteritems():
            final_output_str += k + ': ' + v + '\n'
            # print k + ': ' + v

        final_output_str += '\n'

    # logging.info(final_output_str)
    return final_output_str
