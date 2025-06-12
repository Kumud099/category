from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Category, Tag, Comment, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'avatar', 'website', 'location', 'birth_date', 'is_verified', 'created_at']
        read_only_fields = ['created_at', 'is_verified']


class CategorySerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'posts_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_posts_count(self, obj):
        return obj.posts.filter(status='published').count()


class TagSerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'posts_count', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_posts_count(self, obj):
        return obj.posts.filter(status='published').count()


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'parent', 'replies', 'is_approved', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'is_approved']
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []


class PostListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'excerpt', 'author', 'category', 'tags',
            'status', 'featured_image', 'is_featured', 'view_count',
            'comments_count', 'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = ['id', 'slug', 'view_count', 'created_at', 'updated_at']
    
    def get_comments_count(self, obj):
        return obj.comments.filter(is_approved=True).count()


class PostDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt', 'author', 'category', 'tags',
            'status', 'featured_image', 'is_featured', 'view_count', 'comments',
            'comments_count', 'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = ['id', 'slug', 'author', 'view_count', 'created_at', 'updated_at']
    
    def get_comments_count(self, obj):
        return obj.comments.filter(is_approved=True).count()


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)
    
    class Meta:
        model = Post
        fields = [
            'title', 'content', 'excerpt', 'category', 'tags', 'status',
            'featured_image', 'is_featured', 'published_at'
        ]
    
    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        post = Post.objects.create(**validated_data)
        post.tags.set(tags)
        return post
    
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if tags is not None:
            instance.tags.set(tags)
        
        return instance