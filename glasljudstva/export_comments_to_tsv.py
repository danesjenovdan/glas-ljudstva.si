with open('demands.tsv', 'w') as outfile:
    for demand in Demand.objects.all():
        for comment in Comment.objects.filter(object_pk=demand.pk):
            clean_comment = comment.comment.replace('\n', ' ').replace('\r', ' ')
            outfile.write(f'{demand.workgroup.name}\t{demand.title}\t{clean_comment}\n')

