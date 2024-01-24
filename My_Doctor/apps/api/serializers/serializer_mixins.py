from rest_framework.serializers import ModelSerializer
from rest_framework.reverse import reverse


def reverse_url(self, obj, name=None, kwargs=None):
    request=self.context.get('request', None)
    action = self.context.get('action', None)
    if not request:
        return None
    if not name:
        name = self.Meta.model.__name__.lower()
    if not kwargs:
        kwargs = {'pk': obj.pk}
    if not action:
        return  reverse(f'apps.api:instance-{name}-view', kwargs=kwargs, request=request)
    return reverse(f'apps.api-vs:{name}-detail', kwargs=kwargs, request=request)


class MappingMixin:
    '''
    Mixin override to representation method to allow
    to remapping fields {'old':'New'} 
    '''
    mapping={}
    pop_fields=set()

    def to_representation(self, instance):   
        serializer = super().to_representation(instance)
        self.perform_to_representation(serializer)
        if hasattr(self, 'pop_fields'):
            if self.pop_fields:
                for field in self.pop_fields:
                    if field in serializer:
                        serializer.pop(field, None)
        if hasattr(self, 'mapping'):
            if self.mapping:
                for old, new in self.mapping.items():
                    if old in serializer:
                        serializer[new] = serializer.pop(old, None)
        return serializer


    def perform_to_representation(self, serializer):
        return serializer
    

class DynamicMixin:

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        instance = context.get('instance', None)
        custom_action = context.get('custom_action', None)
        request_user = getattr(context['request'], 'user', None)
        self.perform_init(context)
        fields = self.get_dynamic_fields(instance, custom_action, request_user)
        
        super().__init__(*args, **kwargs)
        all_fields = set(self.fields)
        for field_pop in all_fields - fields:
            self.fields.pop(field_pop)


    def perform_init(self, context):
        pass

        
    def get_dynamic_fields(self, instance, custom_action, request_user):
        fields = set()
        # Fields logic
        return fields


class MappingModelSerializer(MappingMixin, ModelSerializer):    
    pass


class DynamicModelSerializer(MappingMixin, DynamicMixin, ModelSerializer):    
    pass