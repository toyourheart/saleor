import graphene
import graphql_jwt
from graphene_django.debug import DjangoDebug
from graphene_django.filter import DjangoFilterConnectionField

from ..page import models as page_models
from .core.filters import DistinctFilterSet
from .page.types import Page, resolve_pages
from .product.filters import ProductFilterSet
from .product.types import (
    Category, Product, ProductAttribute, resolve_attributes,
    resolve_categories, resolve_products)
from .utils import get_node


class Query(graphene.ObjectType):
    attributes = DjangoFilterConnectionField(
        ProductAttribute,
        filterset_class=DistinctFilterSet,
        in_category=graphene.Argument(graphene.ID))
    categories = DjangoFilterConnectionField(
        Category, filterset_class=DistinctFilterSet,
        level=graphene.Argument(graphene.Int))
    category = graphene.Field(Category, id=graphene.Argument(graphene.ID))
    page = graphene.Field(
        Page, id=graphene.Argument(graphene.ID), slug=graphene.String())
    pages = DjangoFilterConnectionField(
        Page, filterset_class=DistinctFilterSet,
        level=graphene.Argument(graphene.Int))
    product = graphene.Field(Product, id=graphene.Argument(graphene.ID))
    products = DjangoFilterConnectionField(
        Product, filterset_class=ProductFilterSet)
    node = graphene.Node.Field()
    debug = graphene.Field(DjangoDebug, name='__debug')

    def resolve_category(self, info, id):
        return get_node(info, id, only_type=Category)

    def resolve_categories(self, info, level=None, **kwargs):
        return resolve_categories(info, level)

    def resolve_page(self, info, id=None, slug=None):
        if slug is not None:
            return page_models.Page.objects.get(slug=slug)

        return get_node(info, id, only_type=Page)

    def resolve_pages(self, info):
        return resolve_pages()

    def resolve_product(self, info, id):
        return get_node(info, id, only_type=Product)

    def resolve_products(self, info, **kwargs):
        return resolve_products(info)

    def resolve_attributes(self, info, in_category=None, **kwargs):
        return resolve_attributes(in_category, info)


class Mutations(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(Query, Mutations)
