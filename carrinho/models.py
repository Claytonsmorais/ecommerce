from django.db import models
from produtos.models import Produto
from uuid import uuid4

# Create your models here.
class Carrinho(models.Model):
    identificador = models.CharField(default=uuid4, max_length=200)
    produtos = models.ManyToManyField(Produto,through='ProdutoNoCarrinho')


class ProdutoNoCarrinho(models.Model):
    produto = models.ForeignKey(Produto,on_delete=models.DO_NOTHING)
    quantidade = models.IntegerField()
    carrinho = models.ForeignKey(Carrinho, on_delete=models.DO_NOTHING)






