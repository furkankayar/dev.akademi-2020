from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from . import exceptions
from .serializers import PostSerializer, ManageCategorySerializer, PostStatusSerializer, CategorySerializer, PostPostSerializer
from .models import Post, Category, Seller
from .paginators import ListViewPagination
from django.db.utils import IntegrityError
import random


def response_message(status, message):
    return Response({
        'status': status,
        'message': message
    })

class AuthTokenView(ObtainAuthToken):
   
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'status': 'Valid'})
        else:
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            if username and password:
                try:
                    posts = Post.objects.filter(adminID__gt = 0)
                    random_num = random.randint(0, len(posts))
                    random_id = posts[random_num].adminID
                    while get_user_model().objects.filter(id = random_id).exists():
                        random_num = random.randint(0, len(posts))
                        random_id = posts[random].adminID
                    user = get_user_model()(id = random_id, username=username)
                    user.set_password(password)
                    user.save()
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key, 'status': 'Valid'})
                except IntegrityError:
                    raise AuthenticationFailed(detail='Invalid password.', code=None)
            else:
                raise exceptions.BadRequest(detail='Missing arguments')
            

class PostView(APIView):
    
    def get(self, request):
        post_id = request.query_params.get('id')
        if post_id:
            post = Post.objects.filter(id = post_id).first()
            if post == None:
                return response_message(False, 'Post is not found')
            return Response(PostSerializer(post).data)

    def post(self, request):
        serializer = PostPostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            post_id = serializer.data.get('id')
            seller_id = serializer.data.get('sellerID')
            if Post.objects.filter(id = post_id).exists():
                return response_message(False, 'Post is already exists')
            if not Seller.objects.filter(id = seller_id):
                return response_message(False, 'Given seller does not exists')
            seller = Seller.objects.filter(id = seller_id).first()
            post = Post(
                seller = seller,
                title = serializer.data.get('title'),
                description = serializer.data.get('description'),
                price = serializer.data.get('price'), 
                date = serializer.data.get('date'),
                expiryDate = serializer.data.get('expiryDate'),
                status = "WAITING_APPROVAL",
                adminID = 0,
            )
            post.save()
            return response_message(True, 'Post is added successfully (id = ' + str(post.id) + ')')
        else:
            return response_message(False, 'Request body missing or invalid')


class ListView(APIView):

    def get(self, request):
        page_num = 1
        page_size = 10
        if request.query_params.get('page') is not None:
            page_num = int(request.query_params.get('page'))
        if request.query_params.get('size') is not None:
            page_size = int(request.query_params.get('size'))
        posts = Post.objects.all()
        post_count = Post.objects.count()
        paginator = ListViewPagination()
        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(result_page, many=True, context={'request': request})
        result = {
            'content': serializer.data,
            'pageable': {
                'sort': {
                    'sorted': False,
                    'unsorted': True,
                    'empty': True
                },
                'pageNumber': page_num,
                'pageSize': page_size,
                'offset': page_size * page_num,
                'unpaged': False,
                'paged': True
            },
            'totalPages': int(post_count / page_size),
            'totalElements': post_count,
            'last': True if page_num == (post_count / page_size) else False,
            'first': True if page_num == 1 else False,
            'sort': {
                    'sorted': False,
                    'unsorted': True,
                    'empty': True
            },
            'numberOfElements': len(result_page),
            'size': page_size,
            'number': page_num,
            'empty': True if len(result_page) == 0 else False 
        }
        return Response(result)


class MyListView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        page_num = 1
        page_size = 10
        if request.query_params.get('page') is not None:
            page_num = int(request.query_params.get('page'))
        if request.query_params.get('size') is not None:
            page_size = int(request.query_params.get('size'))
        posts = Post.objects.filter(adminID = request.user.id)
        post_count = Post.objects.count()
        paginator = ListViewPagination()
        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(result_page, many=True, context={'request': request})
        result = {
            'content': serializer.data,
            'pageable': {
                'sort': {
                    'sorted': False,
                    'unsorted': True,
                    'empty': True
                },
                'pageNumber': page_num,
                'pageSize': page_size,
                'offset': page_size * page_num,
                'unpaged': False,
                'paged': True
            },
            'totalPages': int(post_count / page_size),
            'totalElements': post_count,
            'last': True if page_num == (post_count / page_size) else False,
            'first': True if page_num == 1 else False,
            'sort': {
                    'sorted': False,
                    'unsorted': True,
                    'empty': True
            },
            'numberOfElements': len(result_page),
            'size': page_size,
            'number': page_num,
            'empty': True if len(result_page) == 0 else False 
        }
        return Response(result)


class ManageCategoryView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ManageCategorySerializer

    def check(self, post_id, category_id):
        if not Category.objects.filter(id = category_id).exists():
            return response_message(False, 'Category is not found')
            
        if not Post.objects.filter(id = post_id).exists():
            return response_message(False, 'Post is not found')
        
        return True

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=False):
            post_id = serializer.data.get('post_id')
            category_id = serializer.data.get('category_id')
            result = self.check(post_id, category_id)
            if not result == True: 
                return result
            post = Post.objects.filter(id = post_id).first()
            category = Category.objects.filter(id = category_id).first()
            if len(post.categories.all()) >= 7:
                return response_message(False, 'Post has maximum number of categories')
            if not category in post.categories.all():
                post.categories.add(category)
            post.save()
            return response_message(True, 'Category is added successfully')
        else:
            return response_message(False, 'Request body missing or invalid')


    def delete(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=False):
            post_id = serializer.data.get('post_id')
            category_id = serializer.data.get('category_id')
            result = self.check(post_id, category_id)
            if not result == True: 
                return result
            post = Post.objects.filter(id = post_id).first()
            category = Category.objects.filter(id = category_id).first()
            if len(post.categories.all()) == 0:
                return response_message(False, 'Post does not have any category')
            if not category in post.categories.all():
                return response_message(False, 'Post does not have this category')
            post.categories.remove(category)   
            post.save()
            return response_message(True, 'Category is removed successfully')
        else:
            return response_message(False, 'Request body missing or invalid')


class PostStatusView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostStatusSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=False):
            post_id = serializer.data.get('post_id')
            status = serializer.data.get('status')

            if not Post.objects.filter(id = post_id).exists():
                return response_message(False, 'Post is not found')

            valid_status = [
                'ACTIVE',
                'REJECTED',
            ]

            if status.upper() not in valid_status:
                return response_message(False, 'Status is not valid. ACTIVE and REJECTED are valid.')

            post = Post.objects.filter(id = post_id).first()
            
            if post.status != 'WAITING_APPROVAL':
                return response_message(False, 'You can not change the status of this post. Post status must be WAITING_APPROVAL')
            
            post.status = status.upper()
            post.adminID = request.user.id
            post.save()

            return response_message(True, 'Post status is updated')


        else:
            return response_message(False, 'Request body missing or invalid')



class CategoryView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

    def get(self, request):
        page_num = 1
        page_size = 10
        if request.query_params.get('page') is not None:
            page_num = int(request.query_params.get('page'))
        if request.query_params.get('size') is not None:
            page_size = int(request.query_params.get('size'))
        categories = Category.objects.all()
        category_count = Category.objects.count()
        paginator = ListViewPagination()
        result_page = paginator.paginate_queryset(categories, request)
        serializer = CategorySerializer(result_page, many=True, context={'request': request})
        result = {
            'content': serializer.data,
            'pageable': {
                'sort': {
                    'sorted': False,
                    'unsorted': True,
                    'empty': True
                },
                'pageNumber': page_num,
                'pageSize': page_size,
                'offset': page_size * page_num,
                'unpaged': False,
                'paged': True
            },
            'totalPages': int(category_count / page_size),
            'totalElements': category_count,
            'last': True if page_num == (category_count / page_size) else False,
            'first': True if page_num == 1 else False,
            'sort': {
                    'sorted': False,
                    'unsorted': True,
                    'empty': True
            },
            'numberOfElements': len(result_page),
            'size': page_size,
            'number': page_num,
            'empty': True if len(result_page) == 0 else False 
        }
        return Response(result)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=False):
            category_id = serializer.data.get('id')
            category_title = serializer.data.get('title')
            if Category.objects.filter(id = category_id).exists():
                return response_message(False, 'Category already exists')
            category = Category(
                id = category_id,
                title = category_title
            )
            category.save()
            return response_message(True, 'Category is added successfully')
        else:
            return response_message(False, 'Request body missing or invalid')

    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=False):
            category_id = serializer.data.get('id')
            category_title = serializer.data.get('title')
            if not Category.objects.filter(id = category_id).exists():
                return response_message(False, 'Category does not exists')
            category = Category.objects.filter(id = category_id).first()
            category.title = category_title
            category.save()
            return response_message(True, 'Category is updated successfully')
        else:
            return response_message(False, 'Request body missing or invalid')
        
        

