def mixing(**kwargs):
    return sorted(
        kwargs.get('old_population') + kwargs.get('children'), key=lambda individual: individual.fitness, reverse=True
    )[:kwargs.get('population_size')]
