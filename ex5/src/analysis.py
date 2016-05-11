import matplotlib.pyplot as plt


def make_plot(data_sets, title, x_axis_name='Distance', y_axis_name='Cost', file_name=None):
    plot = plt.subplot(111)

    x_min = None
    y_min = None

    markers = ['.', '+', '*']

    for i in range(len(data_sets)):
        data_set = data_sets[i]

        x_axis, x_axis_min = data_set[1], min(data_set[1])
        y_axis, y_axis_min = data_set[0], min(data_set[0])

        if x_min is None or x_axis_min < x_min:
            x_min = x_axis_min

        if y_min is None or y_axis_min < y_min:
            y_min = y_axis_min

        plot.plot(x_axis, y_axis, markers[i], label=data_set[2])

    plt.axhline(y=y_min, hold=None)
    plt.axvline(x=x_min, hold=None)

    plt.title(title)

    plt.xlabel(x_axis_name)
    plt.ylabel(y_axis_name)

    if len(data_sets) > 1:
        box = plot.get_position()
        plot.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        plot.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    if file_name is not None:
        plt.savefig('../report/images/tmp/%s.png' % file_name)
    else:
        plt.show()

    plt.clf()


def plot_single_run(data, title, label):
    x_axis = []
    y_axis = []

    for individual in data:
        x_axis.append(individual.fitness[0])
        y_axis.append(individual.fitness[1])

    make_plot([(x_axis, y_axis, label)], title)


def plot_pareto_fronts(fronts):
    data_sets = []

    for front in fronts:
        x_axis = []
        y_axis = []

        for individual in front[0]:
            x_axis.append(individual.fitness[0])
            y_axis.append(individual.fitness[1])

        data_sets.append((
            x_axis,
            y_axis,
            'Population size: %d,\n generations: %d,\n mutation: %f,\n crossover: %f' % (
                front[1]['population_size'],
                front[1]['max_number_of_generations'],
                front[1]['mutation_probability'],
                front[1]['crossover_probability'],
            )
        ))

    make_plot(data_sets, 'Pareto fronts')
