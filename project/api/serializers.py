from rest_framework import serializers 
from accounts.models import Products
 
 
class ProductSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Products
        fields = ('id',
                  'title',
                  'description',
                  'published')