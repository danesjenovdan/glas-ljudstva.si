from functools import reduce

from zahteve.models import Demand, DemandAnswer


def calculate_most_controversial_demands(n=40):
    demands = Demand.objects.all()
    scores = {}
    for demand in demands:
        scores[demand.id] = reduce(
            lambda acc, cur: (acc + (int(cur) * 2 - 1)),
            DemandAnswer.objects.filter(demand=demand).values_list(
                "agree_with_demand", flat=True
            ),
            0,
        )
    return dict(sorted(scores.items(), key=lambda item: item[1])[:n])
