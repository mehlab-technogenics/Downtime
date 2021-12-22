from rest_framework import serializers
from base.models import Website,webData,Profile,History
from django.contrib.auth.models import User


class Historyerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'
class WebDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = webData
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password']
    def create(self, validated_data):

        # create user 
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password'],
            # etc ...
        )
        print(user)

        # create profile
        profile = Profile.objects.create(
            user = user,
            name = validated_data['username'],
            email = validated_data['email'],
            # etc...
        )
        

        return user

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    class Meta:
        model = Profile
        fields = '__all__'
    def create(self, validated_data):

        # create user 
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password'],
            # etc ...
        )
        profile = Profile.objects.create(
            user = user,
            name = validated_data['name'],
            email = validated_data['email'],
            # etc...
        )
        return profile

class WebsiteSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    class Meta:
        model=Website
        fields = '__all__'
    def get_owner(self, obj):
        owner = obj.owner.all()
        serializer = ProfileSerializer(owner, many=True)
        return serializer.data
   