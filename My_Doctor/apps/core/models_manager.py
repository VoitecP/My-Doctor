from django.db import models #Value, Manager
from django.db.models.functions import Coalesce
from collections import OrderedDict

from django.db.models.query import QuerySet


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
                    .values('date__month',
                            'date__year',
                            'total',
                            'sum')
                    )
        return queryset
    

class VisitMonthSummary(models.Manager):
    def get_queryset(self):
        queryset = (super().get_queryset()
                    .values('date__month','date__year')
                    .annotate(total=models.Count('price'))
                    .annotate(sum=models.Sum('price'))
                    .order_by('date__year','date__month')
                    .values('date__month',
                            'date__year',
                            'total',
                            'sum')
                    )
        return queryset	

class VisitCategorySummary(models.Manager):
    def get_queryset(self):
        queryset=(super().get_queryset()
                .annotate(category_name=Coalesce('category__name', models.Value('-No Category-')))
                .order_by('category')
                .values('category_name')
                .annotate(total=models.Count('price'))
                .annotate(sum=models.Sum('price'))
                .order_by('-category')
                .values('category_name','total','sum')
                )
        return queryset
    


class VisitDoctorSummary(models.Manager):
    def get_queryset(self):
        queryset=(super().get_queryset()
                .values('doctor_id',
                        'doctor__user__first_name',
                        'doctor__user__last_name')
                .annotate(total=models.Count('price'))
                .annotate(sum=models.Sum('price'))
                .order_by('-sum')
                .values('doctor_id',
                        'doctor__user__first_name',
                        'doctor__user__last_name',
                        'total',
                        'sum')
                )
        return queryset

