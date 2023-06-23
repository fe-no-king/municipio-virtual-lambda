import itertools

def line_mount(data):

    line_mount = ''
    check = 1
    line_length = data.get('length', 0)
    number = data.get('number')
    data_list = data.get('data', [])

    if isinstance(data_list, list) and len(data_list) > 0:

        line_break = "\n" if number > 1 else ''

        if line_length > 0:
            for val in data_list:
                length = val.get('length', 0)
                text = str(val.get('text', ''))
                complete = val.get('complete', ' ')
                position = val.get('position', 'right')

                complete_cycle = itertools.cycle(complete)
                line = ''

                for item in range(length):
                    check +=1
                    if item < len(text):
                        line += text[item]
                    else:
                        if position == 'right':
                            line += next(complete_cycle)
                        elif position == 'left':
                            line = next(complete_cycle) + line
                    
                line_mount += line

    return f"{line_break}{line_mount}"