from rest_framework import serializers
from carrinho.models import Carrinho, ProdutoNoCarrinho
from produtos.api.serializers import ProdutoSerializer
from produtos.models import Produto


class ProdutoNoCarrinhoSerializer(serializers.ModelSerializer):
    produto = ProdutoSerializer()
    quantidade = serializers.IntegerField()

    class Meta:
        model = ProdutoNoCarrinho
        fields = ['produto','quantidade']

class CarrinhoSerializer(serializers.ModelSerializer):
    produtos=ProdutoNoCarrinhoSerializer(source='produtonocarrinho_set',many=True)
    class Meta:
        model = Carrinho
        fields =['identificador','produtos','id']

class InsertProdutoNoCarrinhoSchema(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Produto.objects.all())
    quantidade = serializers.IntegerField()

    class Meta:
        model = Produto
        fields = ['id','quantidade']

class PostProdutoNoCarrinhoSerializer(serializers.Serializer):
    produtos= serializers.ListField(
        child=InsertProdutoNoCarrinhoSchema()
    )
    carrinho_id = serializers.IntegerField(allow_null=True,required=False)
