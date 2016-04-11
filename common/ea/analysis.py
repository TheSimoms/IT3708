import matplotlib.pyplot as plt


def make_plot(data, title, x_axis_name, y_axis_name, file_name=None):
    plot = plt.subplot(111)

    for i in range(len(data)):
        plot.plot(range(len(data[i][0])), data[i][0], label=data[i][1])

    plt.title(title)

    plt.xlabel(x_axis_name)
    plt.ylabel(y_axis_name)

    box = plot.get_position()
    plot.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    plot.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    if file_name is not None:
        plt.savefig('../report/images/tmp/%s.png' % file_name)
    else:
        plt.show()

    plt.clf()


def plot_results(results):
    make_plot([
        (results['fitness_data']['best'], 'Best'),
        (results['fitness_data']['worst'], 'Worst'),
        (results['fitness_data']['average'], 'Average'),
        (results['fitness_data']['standard_deviation'], 'Standard deviation'),
    ], results['problem'].name, 'Generation number', 'Fitness')


def plot_analysis_results(results, title, file_name=None):
    data = []

    for i in range(len(results)):
        data.append((results[i], 'Run %d' % (i+1)))

    make_plot(data, title, 'Generation number', 'Max fitness', file_name)
