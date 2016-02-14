from utils import get_fitness


def full_selection(**kwargs):
    return kwargs.get('children')


def over_production(**kwargs):
    return sorted(kwargs.get('children'), key=get_fitness, reverse=True)[:kwargs.get('population_size')]


def mixing(**kwargs):
    return sorted(
        kwargs.get('old_population') + kwargs.get('children'), key=get_fitness, reverse=True
    )[:kwargs.get('population_size')]


ADULT_SELECTION_FUNCTIONS = [
    ['Full selection', full_selection, None],
    ['Over-production', over_production, None],
    ['Mixing', mixing, None],
]
