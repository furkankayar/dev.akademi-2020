from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Post, Category

class AuthenticationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class PostPostSerializer(serializers.ModelSerializer):
    
    sellerID = serializers.CharField(required = True)

    class Meta:
        model = Post
        fields = [
            'sellerID',
            'title', 
            'description',
            'price', 
            'date', 
            'expiryDate'
        ]

class PostSerializer(serializers.ModelSerializer):

    categories = serializers.SerializerMethodField('set_categories')
    sellerID = serializers.SerializerMethodField('set_seller_id')
    sellerType = serializers.SerializerMethodField('set_seller_type')

    def set_categories(self, post):
        all_categories = post.categories.all()
        categories = {}
        for i in range(0, 7):
            categories['category' + str(i)] = {
                'id': all_categories[i].id if len(all_categories) > i else 0,
                'title': all_categories[i].title if len(all_categories) > i else None
            }
        return categories

    def set_seller_id(self, post):
        return post.seller.id

    def set_seller_type(self, post):
        return post.seller.type

    class Meta:
        model = Post
        fields = [
            'id', 
            'sellerID',
            'sellerType',
            'title', 
            'description',
            'categories', 
            'price', 
            'date', 
            'expiryDate',
            'live',
            'status',
            'adminID'
        ]


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(required = True)
    title = serializers.CharField(required=True)


class ManageCategorySerializer(serializers.Serializer):

    post_id = serializers.IntegerField(required = True)
    category_id = serializers.IntegerField(required = True)


class PostStatusSerializer(serializers.Serializer):

    post_id = serializers.IntegerField(required = True)
    status = serializers.CharField(required = True, max_length = 20)