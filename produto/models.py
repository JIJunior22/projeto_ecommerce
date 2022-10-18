from django.db import models
from django.conf import settings

class Categoria(models.Model):
    nome = models.CharField(max_length=30)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=150, unique=True)
    foto = models.ImageField()
    descricao = models.TextField()
    preco = models.DecimalField(decimal_places=2, max_digits=100000000)
    importado = models.BooleanField(default=False)
    estoque_atual = models.IntegerField()
    estoque_min = models.IntegerField()
    data = models.DateField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    avaliacao = models.IntegerField(blank=True)

    def __str__(self):
        return self.nome
    
User = settings.AUTH_USER_MODEL

class CartManager(models.manager):
    def new_or_get(self,request):
        cart_id=request.session.get('cart_id',None)
        qs=self.get_queryset().filter(id=cart_id)
        if qs.count==1:
            new_obj=False
            cart_obj=qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user=request.user
                cart_obj.save()
                
        else:
            cart_obj=Cart.objects.new(user=request.user)
            new_obj=True
            request.session ['cart_id']=cart_obj.id
            return cart_obj,new_obj
        
        def new(self,user=None):
            user_obj=None
            if user.is_authenticated:
                user_obj=user
                return self.model.objects.create(user=user_obj)
                     

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    produto = models.ManyToManyField(Produto,blank=True) 
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    objects=CartManager()

    def __str__(self):
        return str(self.id)
     
 
