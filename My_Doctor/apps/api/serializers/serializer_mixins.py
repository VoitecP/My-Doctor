
class MappingMixin:
    '''
    Mixin override to representation method to allow
    to remapping fields {'old':'New'} and pop fields ['a','b'] 
    with is not need to return
    '''
    # pop_fields=[]
    mapping={}


    def to_representation(self, instance):   
            serializer = super().to_representation(instance)
           
            # if hasattr(self, 'pop_fields'):
            #     for field in self.pop_fields:
            #         if field in serializer:
            #             serializer.pop(field, None)
            if hasattr(self, 'mapping'):
                for old, new in self.mapping.items():
                    if old in serializer:
                        serializer[new] = serializer.pop(old, None)

            print(serializer)
            return serializer
    
    

