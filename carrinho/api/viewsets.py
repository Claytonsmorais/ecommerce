from rest_framework.viewsets import ViewSet
from carrinho.models import Carrinho, ProdutoNoCarrinho
from produtos.models import Produto
from .serializers import CarrinhoSerializer, ProdutoNoCarrinhoSerializer, PostProdutoNoCarrinhoSerializer
from rest_framework.response import Response
from rest_framework.exceptions import APIException


class CarrinhoViewSet(ViewSet):

    def list(self, request):
        queryset = Carrinho.objects.all()
        serializer_class = CarrinhoSerializer(queryset,many=True)
        return Response(serializer_class.data)

    def create(self, request):
        data = PostProdutoNoCarrinhoSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            # caso seja passado o carrinho_id na requisicao
            if data.data.get('carrinho_id'):
                for x in data.data.get('produtos'):
                    try:
                        # pegar a instancia do carrinho que foi enviado para ver se existe
                        existente = Carrinho.objects.get(id=data.data.get('carrinho_id'))
                        try:
                            # verificar se o produto já existe neste carrinho
                            produto_no_carrinho = existente.produtonocarrinho_set.get(produto_id=x.get('id'))
                            produto_no_carrinho.quantidade += x.get('quantidade')
                            produto_no_carrinho.save()

                        except ProdutoNoCarrinho.DoesNotExist:
                            #não existindo este produto neste carrinho,inserir este produto no carrinho
                            try:
                                ProdutoNoCarrinho.objects.create(produto=Produto.objects.get(id=x.get('id')),
                                                                 quantidade=x.get('quantidade'),
                                                                 carrinho=existente)

                            except Produto.DoesNotExist:
                                raise APIException(detail=f'Não existe um produto com o id :{x.get("id")}')
                    except Carrinho.DoesNotExist:
                        raise APIException(detail='Não existe um carrinho com este ID')
            else:
                carrinho = Carrinho()
                carrinho.save()

                for x in data.data.get('produtos'):
                    try:
                        ProdutoNoCarrinho.objects.create(produto=Produto.objects.get(id=x.get('id')),
                                                         quantidade=x.get('quantidade'),
                                                         carrinho=carrinho)
                    except Produto.DoesNotExist:
                        raise APIException(detail=f'Não existe um produto com o id :{x.get("id")}')

            return Response(status=200)


