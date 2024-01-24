from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (CreateAPIView, 
                                    ListCreateAPIView, 
                                    RetrieveUpdateAPIView,  
                                    RetrieveDestroyAPIView,
                                    RetrieveUpdateDestroyAPIView)


class ContextMixin:
    def get_serializer_context(self):
        try:
            instance = self.get_object()
        except:
            instance = None
        action = getattr(self, 'action', None)
        request_method = getattr(self.request, 'method', '')
        context = super().get_serializer_context()
        custom_action = self.get_custom_action(instance, action, request_method)
        context.update({
            'request': self.request,  
            'action': action,
            'instance': instance,
            'custom_action': custom_action,
        })
        return context 
    
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
        return ''


class ContextModelViewSet(ContextMixin, ModelViewSet):
    pass


class ContextListCreateAPIView(ContextMixin, ListCreateAPIView):
    pass


class ContextAPIView(ContextMixin, RetrieveUpdateDestroyAPIView):
    pass


class ContextCreateAPIView(ContextMixin, CreateAPIView):
    pass


class ContextUpdateAPIView(ContextMixin, RetrieveUpdateAPIView):
    pass


class ContextDestroyAPIView(ContextMixin, RetrieveDestroyAPIView):
    pass