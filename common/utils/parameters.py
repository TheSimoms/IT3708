def get_boolean_parameter(text):
    while True:
        string = str(input('%s? [y, n]: ' % text))

        if string not in ('y', 'n'):
            print('Please answer y or n')

            continue

        return string == 'y'


def get_numeric_parameter(variable_name, data_type, allow_none=False):
    while True:
        try:
            answer = input('%s%s: ' % (variable_name, ' (optional)' if allow_none else ''))

            if len(answer) == 0 and allow_none:
                return None

            return data_type(answer)
        except (NameError, ValueError):
            print('You need to supply data of type %s' % data_type)


def get_choice_parameter(variable_name, choices):
    while True:
        try:
            number_of_choices = len(choices)
            choices_string = ', '.join(('%s [%i]' % (choices[i][0], i)) for i in range(number_of_choices))

            while True:
                value = int(input('%s (%s): ' % (variable_name, choices_string)))

                if 0 <= value < number_of_choices:
                    return choices[value][1], choices[value][2]
                else:
                    print('You need to supply a value in the range [0, %d]' % (number_of_choices-1))

        except ValueError:
            print('You need to supply an integer')


def get_choice_sub_parameter(sub_parameters):
    parameters = {}

    for parameter in sub_parameters:
        if parameter[2] == bool:
            parameters[parameter[1]] = get_boolean_parameter(parameter[0])
        else:
            parameters[parameter[1]] = get_numeric_parameter(parameter[0], parameter[2])

    return parameters
