import csv
from zahteve.models import Demand, Party, DemandAnswer, WorkGroup


def prettify_answer(answer):
    if not answer:
        return ""
    if answer.agree_with_demand:
        return "DA"
    return f"NE | {answer.comment}"


work_groups = WorkGroup.objects.all().order_by("id")
# parties = Party.objects.filter(finished_quiz=True).order_by("id")
parties = Party.objects.all().order_by("id")

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
