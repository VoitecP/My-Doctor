from rest_framework.serializers import ModelSerializer
from rest_framework.reverse import reverse


def reverse_url(self, obj, name=None):
        request=self.context.get('request', {})

        if not request:
            return None
        if name:
            class_name = name
        else:
            class_name = self.Meta.model.__name__.lower()
        return reverse(f'api:{class_name}-detail', kwargs={"pk": obj.pk}, request=request)


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

        self.perform_init(context)
        fields = self.get_dynamic_fields(instance, action, request_user)

        super().__init__(*args, **kwargs)

        dynamic = set(fields)
        all_fields = set(self.fields)
        for field_pop in all_fields - dynamic:
            self.fields.pop(field_pop)

    def perform_init(self, context):
        pass

    def get_dynamic_fields(self, instance, action, request_user):
        fields =[]
        # Field select logic
        return fields


class MappingModelSerializer(MappingMixin, ModelSerializer):    
    pass

class DynamicModelSerializer(MappingMixin, DynamicMixin, ModelSerializer):    
    pass