from API.models import Post, Category, Seller
import json
import os

base = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(base, 'classified.json')

def run():
    with open(filename) as f:
        data = json.load(f)
    
    i = 0

    for obj in data:
        
        seller = Seller.objects.filter(id=obj.get('sellerID'))
        if not seller.exists():
            seller = Seller(
                id = obj.get('sellerID'),
                type = obj.get('sellerType'),
            )
            seller.save()
        seller = Seller.objects.filter(id=obj.get('sellerID')).first()
        
        categories_dict_arr = [
            obj.get('categories').get('category0'),
            obj.get('categories').get('category1'),
            obj.get('categories').get('category2'),
            obj.get('categories').get('category3'),
            obj.get('categories').get('category4'),
            obj.get('categories').get('category5'),
            obj.get('categories').get('category6')
        ]

        categories_obj = [
        ]
        
        for category_dict in categories_dict_arr:
            if category_dict.get('id') is None or category_dict.get('title') is None:
                continue
            if not Category.objects.filter(id=category_dict.get('id')).exists():
                category = Category(
                    id = category_dict.get('id'),
                    title = category_dict.get('title'),
                )
                category.save()
            categories_obj.append(Category.objects.filter(id=category_dict.get('id')).first())
   
        post = Post(
            id = obj.get('id'),
            seller = seller,
            title = obj.get('title'),
            description = obj.get('description'),
            price = obj.get('price'),
            date = obj.get('date'),
            expiryDate = obj.get('expiryDate'),
            live = obj.get('live'),
            status = obj.get('status'),
            adminID = obj.get('adminID')
        )
    
        post.save()
        
        for category_obj in categories_obj:
            post.categories.add(category_obj)
    
        post.save()
        