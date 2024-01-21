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

    def to_representation(self, instance):   
            serializer = super().to_representation(instance)
            if hasattr(self, 'mapping'):
                for old, new in self.mapping.items():
                    if old in serializer:
                        serializer[new] = serializer.pop(old, None)
            return serializer
    
    
class DynamicMixin:

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        instance = context.get('instance', None)
        action = context.get('action', None)
        request_user = getattr(context['request'], 'user', None)
        request_method = getattr(context['request'],'method', None)
        custom_action = self.get_custom_action(instance, action, request_method)
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

    def get_custom_action(self, instance, action, request_method):
        if action:
            return action
        if bool(request_method == 'GET' and not instance):
            return 'list'
        if bool(request_method == 'POST' and not instance):
            return 'create'
        if bool(request_method == 'GET' and instance):
            return 'retrieve'
        if bool(request_method == 'DELETE' and instance):
            return 'destroy'
        if bool(request_method == 'PUT' and instance):
            return 'update'
        if bool(request_method == 'PATCH' and instance):
            return 'partial_update'


class MappingModelSerializer(MappingMixin, ModelSerializer):    
    pass

class DynamicModelSerializer(MappingMixin, DynamicMixin, ModelSerializer):    
    pass