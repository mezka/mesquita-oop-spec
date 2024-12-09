from typing import Dict

def generate_dimension_attribute_mixin(name: str, start: int, end: int, step: int, offset: int) -> Dict:
    values = [
        {
            'id': f'product_attribute_value_{name.lower().replace(" ", "_")}_{dim}_mt_{dim + offset}',
            'name': f'{name.upper()}: {dim}MM, MT: {dim + offset}MM',
            'attribute_id/id': f'product_attribute_{name.lower().replace(" ", "_")}',
            'is_custom': 'FALSE'
        }
        for dim in range(start, end + 1, step)
    ]
    return {
        'product_attribute_name': name.upper(),
        'product_attribute_values': values,
        'product_attribute_display_type': 'select'
    }

