from unittest.mock import Mock

import pytest
from django.shortcuts import reverse
from prices import Money, MoneyRange, TaxedMoney, TaxedMoneyRange

from saleor.account.models import Address, User
from saleor.core.utils import (
    Country, apply_tax_to_price, create_superuser, format_money,
    get_country_by_ip, get_currency_for_country, random_data)
from saleor.discount.models import Sale, Voucher
from saleor.order.models import Order
from saleor.product.models import Product
from saleor.shipping.models import ShippingMethod

type_schema = {
    'Vegetable': {
        'category': 'Food',
        'product_attributes': {
            'Sweetness': ['Sweet', 'Sour'],
            'Healthiness': ['Healthy', 'Not really']},
        'variant_attributes': {
            'GMO': ['Yes', 'No']},
        'images_dir': 'candy/',
        'is_shipping_required': True}}


def test_apply_tax_to_price_include_tax(taxes):
    money = Money(100, 'USD')
    assert apply_tax_to_price(taxes, 'standard', money) == TaxedMoney(
        net=Money(100, 'USD'), gross=Money(123, 'USD'))
    assert apply_tax_to_price(taxes, 'medical', money) == TaxedMoney(
        net=Money(100, 'USD'), gross=Money(108, 'USD'))

    taxed_money = TaxedMoney(net=Money(100, 'USD'), gross=Money(100, 'USD'))
    assert apply_tax_to_price(taxes, 'standard', taxed_money) == TaxedMoney(
        net=Money(100, 'USD'), gross=Money(123, 'USD'))
    assert apply_tax_to_price(taxes, 'medical', taxed_money) == TaxedMoney(
        net=Money(100, 'USD'), gross=Money(108, 'USD'))


def test_apply_tax_to_price_include_tax_fallback_to_standard_rate(taxes):
    money = Money(100, 'USD')
    taxed_money = TaxedMoney(net=Money(100, 'USD'), gross=Money(123, 'USD'))
    assert apply_tax_to_price(taxes, 'space suits', money) == taxed_money


def test_apply_tax_to_price_add_tax(settings, taxes):
    settings.INCLUDE_TAXES_IN_PRICES = False

    money = Money(100, 'USD')
    assert apply_tax_to_price(taxes, 'standard', money) == TaxedMoney(
        net=Money('81.30', 'USD'), gross=Money(100, 'USD'))
    assert apply_tax_to_price(taxes, 'medical', money) == TaxedMoney(
        net=Money('92.59', 'USD'), gross=Money(100, 'USD'))


def test_apply_tax_to_price_add_tax_fallback_to_standard_rate(
        settings, taxes):
    settings.INCLUDE_TAXES_IN_PRICES = False
    money = Money(100, 'USD')
    assert apply_tax_to_price(taxes, 'space suits', money) == TaxedMoney(
        net=Money('81.30', 'USD'), gross=Money(100, 'USD'))

    taxed_money = TaxedMoney(net=Money(100, 'USD'), gross=Money(100, 'USD'))
    assert apply_tax_to_price(taxes, 'space suits', taxed_money) == TaxedMoney(
        net=Money('81.30', 'USD'), gross=Money(100, 'USD'))


def test_apply_tax_to_price_raise_typeerror_for_invalid_type(taxes):
    with pytest.raises(TypeError):
        assert apply_tax_to_price(taxes, 'standard', 100)


def test_apply_tax_to_price_no_taxes_return_taxed_money():
    money = Money(100, 'USD')
    taxed_money = TaxedMoney(net=Money(100, 'USD'), gross=Money(100, 'USD'))

    assert apply_tax_to_price(None, 'standard', money) == taxed_money
    assert apply_tax_to_price(None, 'medical', taxed_money) == taxed_money


def test_apply_tax_to_price_no_taxes_return_taxed_money_range():
    money_range = MoneyRange(Money(100, 'USD'), Money(200, 'USD'))
    taxed_money_range = TaxedMoneyRange(
        TaxedMoney(net=Money(100, 'USD'), gross=Money(100, 'USD')),
        TaxedMoney(net=Money(200, 'USD'), gross=Money(200, 'USD')))

    assert (apply_tax_to_price(
        None, 'standard', money_range) == taxed_money_range)
    assert (apply_tax_to_price(
        None, 'standard', taxed_money_range) == taxed_money_range)


def test_apply_tax_to_price_no_taxes_raise_typeerror_for_invalid_type():
    with pytest.raises(TypeError):
        assert apply_tax_to_price(None, 'standard', 100)


def test_format_money():
    money = Money('123.99', 'USD')
    assert format_money(money) == '$123.99'


@pytest.mark.parametrize('ip_data, expected_country', [
    ({'country': {'iso_code': 'PL'}}, Country('PL')),
    ({'country': {'iso_code': 'UNKNOWN'}}, None),
    (None, None),
    ({}, None),
    ({'country': {}}, None)])
def test_get_country_by_ip(ip_data, expected_country, monkeypatch):
    monkeypatch.setattr(
        'saleor.core.utils.georeader.get',
        Mock(return_value=ip_data))
    country = get_country_by_ip('127.0.0.1')
    assert country == expected_country


@pytest.mark.parametrize('country, expected_currency', [
    (Country('PL'), 'PLN'),
    (Country('US'), 'USD'),
    (Country('GB'), 'GBP')])
def test_get_currency_for_country(country, expected_currency, monkeypatch):
    currency = get_currency_for_country(country)
    assert currency == expected_currency


def test_create_superuser(db, client):
    credentials = {'email': 'admin@example.com', 'password': 'admin'}
    # Test admin creation
    assert User.objects.all().count() == 0
    create_superuser(credentials)
    assert User.objects.all().count() == 1
    admin = User.objects.all().first()
    assert admin.is_superuser
    # Test duplicating
    create_superuser(credentials)
    assert User.objects.all().count() == 1
    # Test logging in
    response = client.post('/account/login/',
                           {'username': credentials['email'],
                            'password': credentials['password']},
                           follow=True)
    assert response.context['request'].user == admin


def test_create_shipping_methods(db):
    assert ShippingMethod.objects.all().count() == 0
    for _ in random_data.create_shipping_methods():
        pass
    assert ShippingMethod.objects.all().count() == 2


def test_create_fake_user(db):
    assert User.objects.all().count() == 0
    random_data.create_fake_user()
    assert User.objects.all().count() == 1
    user = User.objects.all().first()
    assert not user.is_superuser


def test_create_fake_users(db):
    how_many = 5
    for _ in random_data.create_users(how_many):
        pass
    assert User.objects.all().count() == 5


def test_create_address(db):
    assert Address.objects.all().count() == 0
    random_data.create_address()
    assert Address.objects.all().count() == 1


def test_create_attribute(db):
    data = {'slug': 'best_attribute', 'name': 'Best attribute'}
    attribute = random_data.create_attribute(**data)
    assert attribute.name == data['name']
    assert attribute.slug == data['slug']


def test_create_product_types_by_schema(db):
    product_type = random_data.create_product_types_by_schema(
        type_schema)[0][0]
    assert product_type.name == 'Vegetable'
    assert product_type.product_attributes.count() == 2
    assert product_type.variant_attributes.count() == 1
    assert product_type.is_shipping_required


def test_create_products_by_type(db):
    assert Product.objects.all().count() == 0
    how_many = 5
    product_type = random_data.create_product_types_by_schema(
        type_schema)[0][0]
    random_data.create_products_by_type(
        product_type, type_schema['Vegetable'], '/',
        how_many=how_many, create_images=False)
    assert Product.objects.all().count() == how_many


def test_create_fake_order(db):
    for _ in random_data.create_shipping_methods():
        pass
    for _ in random_data.create_users(3):
        pass
        random_data.create_products_by_schema('/', 10, False)
    how_many = 5
    for _ in random_data.create_orders(how_many):
        pass
    assert Order.objects.all().count() == 5


def test_create_product_sales(db):
    how_many = 5
    for _ in random_data.create_product_sales(how_many):
        pass
    assert Sale.objects.all().count() == 5


def test_create_vouchers(db):
    assert Voucher.objects.all().count() == 0
    for _ in random_data.create_vouchers():
        pass
    assert Voucher.objects.all().count() == 2


def test_manifest(client, site_settings):
    response = client.get(reverse('manifest'))
    assert response.status_code == 200
    content = response.json()
    assert content['name'] == site_settings.site.name
    assert content['short_name'] == site_settings.site.name
    assert content['description'] == site_settings.description
