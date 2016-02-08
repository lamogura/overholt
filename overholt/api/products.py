# -*- coding: utf-8 -*-
"""
    overholt.api.products
    ~~~~~~~~~~~~~~~~~~~~~

    Product endpoints
"""

from flask import Blueprint, request

from ..forms import NewProductForm, UpdateProductForm
from ..services import products
from . import OverholtFormError, secured_route

bp = Blueprint('products', __name__, url_prefix='/products')


@secured_route(bp, '/')
def list():
    """Returns a list of product instances."""
    return products.all()


@secured_route(bp, '/', methods=['POST'])
def create():
    """Creates a new product. Returns the new product instance."""
    form = NewProductForm()
    if form.validate_on_submit():
        return products.create(**request.json)
    raise OverholtFormError(form.errors)


@secured_route(bp, '/<product_id>')
def show(product_id):
    """Returns a product instance."""
    return products.get_or_404(product_id)


@secured_route(bp, '/<product_id>', methods=['PUT'])
def update(product_id):
    """Updates a product. Returns the updated product instance."""
    form = UpdateProductForm()
    if form.validate_on_submit():
        return products.update(products.get_or_404(product_id), **request.json)
    raise(OverholtFormError(form.errors))


@secured_route(bp, '/<product_id>', methods=['DELETE'])
def delete(product_id):
    """Deletes a product. Returns a 204 response."""
    products.delete(products.get_or_404(product_id))
    return None, 204
