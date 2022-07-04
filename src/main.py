from traits_generator import generate_traits
from representations_generator import generate_representations
from attributes_stats_generator import generate_attributes_stats
from images_generator import generate_images

# TODO: Traits matching
# Config variables
traits_csv_path = 'traits.csv'
# TODO: 3 positional props same for each trait
trait_props_count = 3
# TODO: representations_count & sample to csv?
representations_sample = 13000
representations_count = 10000
unique_representations_count = 10
traits_images_path = 'traits'
background_path = 'background'
unique_images_path = 'unique'
images_extension = 'png'
images_resolution = None

# Script variables
traits_json_path = 'traits.json'
representations_json_path = 'representations.json'
attributes_stats_json_path = 'attributes_stats.json'
representation_prop_id = 'id'
images_path = 'images'

# 1. Generate traits, get trait props names
trait_props_names = generate_traits(traits_csv_path, traits_json_path, trait_props_count)
# 2. Generate representations including unique ones
generate_representations(traits_json_path,
                         representations_json_path,
                         trait_props_names,
                         representation_prop_id,
                         representations_sample,
                         representations_count,
                         unique_representations_count)
# 3. Generate attributes stats for dynamic images
generate_attributes_stats(representations_json_path,
                          attributes_stats_json_path,
                          representation_prop_id,
                          unique_representations_count)
# 4. Generate dynamic & unique images
generate_images(traits_json_path,
                representations_json_path,
                trait_props_names,
                representation_prop_id,
                unique_representations_count,
                traits_images_path,
                images_path,
                background_path,
                unique_images_path,
                images_extension,
                images_resolution)
