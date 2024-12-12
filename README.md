https://help.solidworks.com/2021/english/SolidWorks/sldworks/c_bend_calculation_tables.htm
https://steeldoor.org/sdi-135/

# Odoo Custom Door BOM Generator - Codebase Walkthrough

This repo provides a system for dynamically generating Bills of Materials (BOMs) for custom doors within Odoo. Here's a programmer-oriented walkthrough of the codebase:

## Core Idea

We define door components and assemblies as Python classes. When a product variant is created in Odoo, we instantiate these classes with the variant's attribute values and recursively save them to Odoo, creating the BOM on the fly.

## Code Structure and Explanation

Let's break down the key files and their roles:

**1. `base_classes.py`:**

*   **`Component` (ABC):** The base class for all parts.
    *   `get_attributes()`: Returns component attributes, excluding subcomponents.
    *   `OdooMixin`: Handles Odoo interactions (explained below).
*   **`Assembly` (inherits `Component`):**
    *   `components`: A dictionary to store subcomponents (name: (quantity, Component)).
    *   `show_components()`: Prints the component tree (useful for debugging).
    *   `OdooAssemblyMixin`: Extends `OdooMixin` for BOM-specific logic.
*   **`Core`, `WallPlate`, `Hinge`, `IntumescentSeal`, `SheetMetalCut`:**
    *   Basic, non-configurable component classes with default attributes.
*   **`BendSingleDoorLeafBase`, `BendSingleDoorLeafCover`, `BendUChannel`, `SingleDoorLeaf`, `ProfileFrameDoubleRabbet`, `ProfileFrameDoubleRabbetWithBackbendReturn`, `DoorFrameDoubleRabbet`, `SingleDoor`:**
    *   More complex assembly classes. They calculate dimensions based on input parameters and bend allowances (see `calculate_bend_allowance_solidworks.py`).

**2. `specific_parts.py`:**

*   **`IntumescentSeal10x1`, `LiteHingeRight`, `LiteHingeLeft`, `FireproofPanel`:**
    *   Concrete implementations of base component classes with specific default values.

**3. `lite.py`:**

*   Contains classes specific to the "Lite" door model.
*   **`LiteProfileFrameDoubleRabbet...`:** Different frame profiles for the Lite model.
*   **`LiteBendSingleDoorLeafBase`, `LiteBendSingleDoorLeafCover`, `LiteSingleDoorLeaf`:** Components and assemblies specific to the Lite door leaf.
*   **`LiteDoorFrameDoubleRabbet`, `LiteSingleDoor`:** The frame and the complete Lite door assembly.
*   **`get_hinge_from_sentido()`, `get_frame_profile_for_frame()`:** Helper functions within `LiteSingleDoor` to select the correct hinge and frame profile based on door attributes.

**4. `odoo_mixins3.py`:**

*   **`OdooMixin` (ABC):**  The heart of the Odoo integration.
    *   `get_name()`, `get_default_code()`: Abstract methods, implemented by subclasses to provide the component's name and default code for Odoo.
    *   `_get_product_product_id_by_product_template_id()`, `_get_product_template_id_by_default_code()`: Search for existing products in Odoo.
    *   `_create_product_template()`, `_create_product_product()`: Create new product templates and variants.
    *   `save_to_odoo()`:  **Crucially**, this method saves a component to Odoo. It either finds an existing product or creates a new one. It returns the `product_template_id` and `product_product_id`.
*   **`OdooAssemblyMixin` (inherits `OdooMixin`):**
    *   `is_door()`: A simple check to see if the assembly is a door (can be used for special logic).
    *   `save_to_odoo()`: **Overridden** to handle assemblies.
        1. Recursively calls `save_to_odoo()` on each subcomponent.
        2. Gets or creates a BOM (`_get_bom()`, `_create_bom()`).
        3. Creates BOM lines for each subcomponent.

**5. `attributes.py`:**

*   **`EnumToOdooProductAttributeMixin`:** A mixin to easily convert Python Enums into Odoo product attributes.
*   **`BaseEnum`:** Inherits from `EnumToOdooProductAttributeMixin` making easier to create enums.
*   **`Sentido`, `Marco`, `Grampa`, `Acabado`:** Enums for door attributes. `to_attribute_config_mixin()` generates the data structure for creating these attributes in Odoo.

**6. `generate_dimension_attribute_mixin.py`:**

*   **`generate_dimension_attribute_mixin()`:** Generates Odoo attribute data for dimensions like width and height. You specify the start, end, step, and offset for the range of values.

**7. `product_templates.py`:**

*   Defines dictionaries representing Odoo product templates (e.g., `product_template_rf30_lite_simple`). These specify the attributes to be used for each door type.

**8. `generate_odoo_data_from_product_templates.py`:**

*   This script generates CSVs to import into Odoo:
    *   `extract_attributes_and_values()`: Parses the product templates and extracts unique attributes and values. Also creates attribute lines.
    *   `generate_csvs_from_product_templates()`: Generates `product.template.csv`, `product.attribute.csv`, `product.attribute.value.csv`, and `product.template.attribute.line.csv`.

**9. `calculate_bend_allowance_solidworks.py`:**

*   Implements SolidWorks formulas for calculating bend allowances for sheet metal parts.

**10. `product_template.py`:**

*   **`CustomProductTemplate` (Odoo Model):** Extends Odoo's `product.template`.
    *   `is_custom_door`: A field to flag custom door templates.
    *   `_get_door_attributes()`: Gets attribute values from a product variant.
    *   `_create_product_variant()`: **The most important override.** When a new variant is created:
        1. It gets the attribute values (width, height, etc.).
        2. It creates a `LiteSingleDoor` instance (or another door type) using these values.
        3. It calls `save_to_odoo()` on the door instance, passing the product template and variant IDs. This triggers the recursive saving of components and the BOM creation.
        4. It uses a `MesquitaEnvironment` context manager to set the Odoo environment for `OdooMixin`.

**11. `mesquita_environment.py`:**

*   **`MesquitaEnvironment`:** A simple context manager to set the `OdooMixin.env` variable, providing access to the Odoo API when saving components.

## How it Works - The Flow

1. **CSV Import:** You import the CSVs generated by `generate_odoo_data_from_product_templates.py` into Odoo. This creates the product templates and attributes.
2. **Variant Creation:** A user creates a product variant in Odoo, selecting attribute values (e.g., width: 900, height: 2000, etc.).
3. **`_create_product_variant` Trigger:** Odoo calls the overridden `_create_product_variant` method in `CustomProductTemplate`.
4. **Door Instantiation:** A `LiteSingleDoor` object (or another door type) is created using the selected attribute values.
5. **Recursive Saving and BOM Creation:** `save_to_odoo()` is called on the door object.
    *   The door's components are recursively saved to Odoo using their respective `save_to_odoo()` methods (either creating new products or finding existing ones).
    *   `OdooAssemblyMixin` creates the BOM for the door, linking it to the product variant and adding BOM lines for each component.
6. **Done!** The product variant now has a dynamically generated BOM based on its attributes.

## Key Files for Developers

*   **`base_classes.py`:** Understand the `Component`, `Assembly`, `OdooMixin`, and `OdooAssemblyMixin` classes.
*   **`lite.py`:** Focus on how the `LiteSingleDoor` and its components are defined.
*   **`odoo_mixins3.py`:** Pay close attention to the `save_to_odoo()` methods and how they interact with Odoo.
*   **`product_template.py`:** See how `_create_product_variant()` orchestrates the process.

## To-Do and Improvements

*   **Error Handling:** Add more robust error handling and logging, especially in `save_to_odoo()`.
*   **Performance:** Optimize `save_to_odoo()` for large numbers of components (e.g., batch database operations).
*   **Extensibility:** Make it easier to add new door types and components without modifying core code (consider using a registry or configuration files).
*   **Testing:** Write unit and integration tests to ensure everything works as expected.

This README should give you a solid starting point for understanding and working with the code. Let me know if you have any more questions!