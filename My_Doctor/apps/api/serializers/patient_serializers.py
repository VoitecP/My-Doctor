from apps.core.models import Patient, User
from rest_framework import serializers
# from apps.api.serializers import UserPublicSerializer, UserUpdateSerializer, UserPrivateSerializer  
from apps.api.serializers import user_serializers


class PatientPublicSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient's public view
    """
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = user_serializers.UserPublicSerializer(read_only=True)
    
    class Meta:
        model = Patient
        fields = ['user','tracks']
        
       

class PatientPrivateSerializer(serializers.ModelSerializer):
    """
    Only logged user can view these fields , self fields.
    """
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = user_serializers.UserPrivateSerializer(read_only=True)
    
    class Meta:
        model = Patient
        fields = ['user','adress','birth_date','tracks']


class PatientVisitSerializer(serializers.ModelSerializer):
    """
    Only connected thru common visit can see these fields
    """
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = user_serializers.UserVisitSerializer
    
    class Meta:
        model = Patient
        # fields = '__all__'
        fields = ['user','adress','birth_date','tracks']

####


# class PatientSerializer(serializers.ModelSerializer):
#     tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
#     class Meta:
#         model = Patient
#         fields = '__all__'


class PatientUpdateSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user = user_serializers.UserUpdateSerializer()
    
    class Meta:
        model = Patient
        fields = ['tracks','adress', 'birth_date','phone', 'user']
        # fields = '__all__'


    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `Snippet` instance, given the validated data.
    #     """
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.code = validated_data.get('code', instance.code)
    #     instance.linenos = validated_data.get('linenos', instance.linenos)
    #     instance.language = validated_data.get('language', instance.language)
    #     instance.style = validated_data.get('style', instance.style)
    #     instance.save()
    #     return instance
       







