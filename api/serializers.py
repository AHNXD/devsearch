from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile, Skill, Message

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Review
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Profile
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at')
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Tag
        fields = '__all__'
        
class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
        
class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField()
    class Meta:
        model =  Project
        fields = '__all__'
    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data
        
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'