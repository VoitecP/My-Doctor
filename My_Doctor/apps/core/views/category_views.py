
from django.views.generic.list import ListView

from apps.core.models import Category

class CategoryListView(ListView):
    model = Category
    paginate_by = 5 
    template_name = 'category/category_list.html'
    context_object_name = 'categories'

    # def get_context_data(self, *,object_list=None, **kwargs):
    #     if object_list is not None: 
    #         queryset = object_list
    #     # else: 
    #     #     queryset=self.object_list
    #     # form=CategorySearchForm(self.request.GET)
    #     # if form.is_valid(): 
    #     #     name=form.cleaned_data.get('name')
    #     #     if name:
    #     #         queryset=queryset.filter(name__icontains=name)

    #     return super().get_context_data(
    #         #form=form,
    #         object_list=queryset,
    #         **kwargs)