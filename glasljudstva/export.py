import csv

from zahteve.models import Demand, DemandAnswer, Election, Party, WorkGroup


def prettify_answer(answer):
    if not answer:
        return ""
    if answer.agree_with_demand:
        return "DA"
    return f"NE | {answer.comment}"


election = Election.objects.filter(slug="predsedniske-2022").first()
work_groups = WorkGroup.objects.filter(election=election).order_by("id")
# parties = Party.objects.filter(finished_quiz=True).order_by("id")
parties = Party.objects.filter(election=election).order_by("id")
filtered_parties = parties.filter(
    party_name__in=[
        "Anže Logar",
        "Nataša Pirc Musar",
        "Milan Brglez",
        "Miha Kordiš",
        "Gregor Bezenšek ml.",
        "Sabina Senčar",
        "Janez Cigler Kralj",
        "Vladimir Prebilič",
    ]
)

for workgroup in work_groups:
    with open(f"stranke/{workgroup.name}.csv", "w") as outfile:
        writer = csv.writer(outfile, delimiter=",", quotechar='"')
        # write top row
        writer.writerow(["zahteva"] + [party.party_name for party in parties])

        for demand in Demand.objects.filter(workgroup=workgroup).order_by("id"):
            party_answers = []
            for party in parties:
                demand_answer = DemandAnswer.objects.filter(party=party, demand=demand)
                if demand_answer.count() == 1:
                    party_answers.append(demand_answer.first())
                else:
                    party_answers.append(None)

            writer.writerow(
                [demand.title] + [prettify_answer(answer) for answer in party_answers]
            )

    with open(f"stranke/strinjanje.csv", "w") as outfile:
        writer = csv.writer(outfile, delimiter=",", quotechar='"')
        # write top row
        writer.writerow(["zahteva", "strinjanje"])

        for demand in Demand.objects.filter(workgroup=workgroup).order_by("id"):
            writer.writerow(
                [
                    demand.title,
                    DemandAnswer.objects.filter(
                        demand=demand,
                        party__in=filtered_parties,
                        agree_with_demand=True,
                    ).count(),
                ]
            )
