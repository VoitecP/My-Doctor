from django.db import models # Value, Manager
from django.db.models.functions import Coalesce
from collections import OrderedDict


class VisitYearSummary(models.Manager):
    def get_queryset(self):
        queryset = (super().get_queryset()
                    .values('date__year')
                    .annotate(total=models.Count('price'))
                    .annotate(sum=models.Sum('price'))
                    .order_by('date__year')
                    .values('date__year','total','sum')
                    )
        return queryset
    

class VisitMonthSummary(models.Manager):
    def get_queryset(self):
        queryset = (super().get_queryset()
                    .values('date__month','date__year')
                    .annotate(total=models.Count('price'))
                    .annotate(sum=models.Sum('price'))
                    .order_by('date__year','date__month')
                    .values('date__month','date__year','total','sum')
                    )
        return queryset
    

	