{
    'name': 'Product Variant Hooks',
    'version': '0.1',
    'category': 'Sales',
    'summary': 'Add hooks for product variant creation',
    'depends': ['base',
                'product',
                'mrp',
                'uom'
                ],
    'data': [
        'data/product.attribute.csv',
        'data/product.attribute.value.csv',
        'data/product.template.csv',
        'data/product.template.attribute.line.csv'
        ],
    'installable': True,
    'application': False,
}
