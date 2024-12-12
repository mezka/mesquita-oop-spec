import pandas as pd
from typing import List, Dict, Set
from product_templates import product_template_rf30_lite_simple
import os

def extract_attributes_and_values(templates: List[Dict]) -> Dict[str, pd.DataFrame]:
    attributes: Set[frozenset] = set()
    attribute_values: Set[frozenset] = set()
    attribute_lines: List[Dict] = []

    for template in templates:
        for attr in template['attributes']:
            attribute_id = f'product_attribute_{attr["product_attribute_name"].lower().replace(' ', '_')}'
            # Convert dictionary to frozenset to make it hashable
            attributes.add(frozenset({
                'id': attribute_id,
                'name': attr['product_attribute_name'],
                'create_variant': 'dynamic',
                'display_type': attr['product_attribute_display_type']
            }.items()))

            # Process attribute values uniquely
            for value in attr['product_attribute_values']:
                attribute_values.add(frozenset(value.items()))

            # Create attribute line entries for each attribute in the template
            value_ids = ','.join([value['id'] for value in attr['product_attribute_values']])
            attribute_lines.append({
                'id': f'{template["id"]}_attribute_line_{attr["product_attribute_name"].lower().replace(' ', '_')}',
                'product_tmpl_id/id': template['id'],
                'attribute_id/id': attribute_id,
                'value_ids/id': value_ids
            })

    # Return DataFrames directly for each model
    return {
        "product.attribute": pd.DataFrame([dict(items) for items in attributes]),
        "product.attribute.value": pd.DataFrame([dict(items) for items in attribute_values]),
        "product.template.attribute.line": pd.DataFrame(attribute_lines)
    }

def generate_xlsx_from_product_templates(filename: str, templates: List[Dict]):
    data_frames = extract_attributes_and_values(templates)
    template_df = pd.DataFrame(templates).drop(columns=['attributes'])  # product.template


    with pd.ExcelWriter(filename) as writer:
        template_df.to_excel(writer, sheet_name="product.template", index=False)
        for sheet_name, df in data_frames.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

def generate_csvs_from_product_templates(directory_path, templates: List[Dict]):
    data_frames = extract_attributes_and_values(templates)
    template_df = pd.DataFrame(templates).drop(columns=['attributes'])  # product.template
    
    directory_full_path = os.path.join(os.path.dirname(__file__), directory_path)

    template_df.to_csv(os.path.join(directory_full_path, 'product.template.csv'), index=False)

    for model_name, df in data_frames.items():
        csv_path = os.path.join(directory_full_path, f'{model_name}.csv')
        df.to_csv(csv_path, index=False)

if __name__ == "__main__":
    templates = [product_template_rf30_lite_simple]
    generate_csvs_from_product_templates("data", templates)
