from django.db import models
from django.urls import reverse


class Category(models.Model):
    name=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(max_length=250,unique=True)
    description=models.TextField(blank=True)
    image=models.ImageField(upload_to='category/',blank=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)


    class Meta:
        ordering=('name',)
        verbose_name = ("Category")
        verbose_name_plural = ("Categories")

    def __str__(self):
        return '{}'.format( self.name)
    

    def get_url(self):
        return reverse('home:products_by_category',args=[self.slug])

class Product(models.Model):
    name=models.CharField(max_length=250,unique=True)   
    slug=models.SlugField(max_length=250,unique=True)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    category=models.ForeignKey(Category,on_delete=models.CASCADE) 
    image=models.ImageField(upload_to='products',blank=True)
    stock=models.IntegerField()
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
  


    class Meta:
       ordering=('name',)
       verbose_name='Product'
       verbose_name_plural='Products'

    def __str__(self):
        return '{}'.format(self.name)

    def get_url(self):
       return reverse('home:prodetail',args=[self.category.slug,self.slug])

    def get_final_price(self):
        """Returns the product price after applying the higher discount (product or category)."""
        applicable_discount = max(self.discount_percentage, self.category.discount_percentage)
        discounted_price = self.price - (self.price * (applicable_discount / 100))
        return round(discounted_price, 2)

    def get_discount_percentage(self):

        """Returns the higher of product-level or category-level discount."""
        return max(self.discount_percentage, self.category.discount_percentage)
