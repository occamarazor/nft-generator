import os
import shutil
import json
from PIL import Image


# Generates dynamic & unique images
def generate_images(traits_json_path: str,
                    representations_json_path: str,
                    trait_props_names: list,
                    representation_prop_id: str,
                    unique_representations_count: int,
                    traits_images_path: str,
                    images_path: str,
                    background_path: str,
                    unique_images_path: str,
                    images_extension: str,
                    images_resolution: any) -> None:
    attr_prop_trait_name = 'trait'
    attr_prop_attr_name = 'attribute'
    [attribute_prop_name, _, attribute_prop_order] = trait_props_names

    # Recreate images directory
    if os.path.exists(images_path):
        shutil.rmtree(images_path)
    os.makedirs(images_path)

    with open(traits_json_path) as traits_file:
        traits = json.load(traits_file)

        with open(representations_json_path) as representations_file:
            representations = json.load(representations_file)
            unique_representations = representations[:unique_representations_count]
            dynamic_representations = representations[unique_representations_count:]

            # Generate unique images
            # TODO: file name should match repr id
            for unique_rep in unique_representations:
                unique_rep_image = Image.open(f'{traits_images_path}/{background_path}.{images_extension}')
                unique_image = Image.open(f'{traits_images_path}/'
                                          f'{unique_images_path}/'
                                          f'{unique_rep[representation_prop_id]}.'
                                          f'{images_extension}')
                unique_rep_image.paste(unique_image, (0, 0), unique_image)
                # Resample nearest to retain resolution if resolution specified
                if images_resolution:
                    unique_rep_image = unique_rep_image.resize((images_resolution, images_resolution),
                                                               resample=Image.NEAREST)
                unique_rep_image.save(
                    f'{images_path}/{unique_rep[representation_prop_id]}.{images_extension}',
                    images_extension.upper())

            # Generate dynamic images
            for dynamic_rep in dynamic_representations:
                dynamic_reps_with_order = []
                dynamic_rep_id = dynamic_rep[representation_prop_id]
                # Open dynamic image with default background
                dynamic_rep_image = Image.open(f'{traits_images_path}/{background_path}.{images_extension}')

                # Create dynamic representations with attribute order
                for key, val in dynamic_rep.items():
                    if key != representation_prop_id:
                        dynamic_attr_order = [attr[attribute_prop_order]
                                              for attr in traits[key]
                                              if attr[attribute_prop_name] == val
                                              ][0]
                        dynamic_rep_with_order = {attr_prop_trait_name: key,
                                                  attr_prop_attr_name: val,
                                                  attribute_prop_order: dynamic_attr_order}
                        dynamic_reps_with_order.append(dynamic_rep_with_order)

                # Sort dynamic representations by attribute order
                for dynamic_rep_with_order in sorted(dynamic_reps_with_order, key=lambda r: r[attribute_prop_order]):
                    # Open image with specific attribute
                    attr_image = Image.open(f'{traits_images_path}/'
                                            f'{dynamic_rep_with_order[attr_prop_trait_name]}/'
                                            f'{dynamic_rep_with_order[attr_prop_attr_name]}.'
                                            f'{images_extension}')
                    # Merge dynamic image with specific attribute image
                    dynamic_rep_image.paste(attr_image, (0, 0), attr_image)

                # Resample nearest to retain resolution if resolution specified
                if images_resolution:
                    dynamic_rep_image = dynamic_rep_image.resize((images_resolution, images_resolution),
                                                                 resample=Image.NEAREST)

                # Save dynamic image to specified directory
                dynamic_rep_image.save(f'{images_path}/{dynamic_rep_id}.{images_extension}', images_extension.upper())
