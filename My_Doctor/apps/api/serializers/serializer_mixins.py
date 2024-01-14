from rest_framework.serializers import ModelSerializer


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
    
    
class MappingModelSerializer(MappingMixin, ModelSerializer):    
    pass