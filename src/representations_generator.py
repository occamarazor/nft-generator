import json
from numpy import random
# from pprint import pprint


# Generates representations including unique ones
def generate_representations(traits_json_path: str,
                             representations_json_path: str,
                             trait_props_names: list,
                             representation_prop_id: str,
                             representations_sample: int,
                             representations_count: int,
                             unique_representations_count: int) -> None:
    with open(traits_json_path) as traits_file:
        unique_representations = []
        dynamic_representations = []
        # TODO: 3 positional props same for each trait
        # name, chance, order
        [attribute_prop_name, attribute_prop_chance, _] = trait_props_names
        traits = json.load(traits_file)

        # Generate unique representations
        for i in range(unique_representations_count):
            unique_representations.append({representation_prop_id: i + 1})
            for trait_name in traits:
                unique_representations[i][trait_name] = 'none'

        # Generate dynamic representations
        for trait_name in traits:
            trait_attributes = traits[trait_name]
            trait_attributes_chances = [attr[attribute_prop_chance] for attr in trait_attributes]
            random_trait_attributes = random.choice(trait_attributes,
                                                    representations_sample,
                                                    p=trait_attributes_chances)

            for i, random_attr in enumerate(random_trait_attributes):
                attribute_name = random_attr[attribute_prop_name]

                # Add attributes pairs until dynamic reps are filled with all selected attributes for current trait
                if len(dynamic_representations) == i:
                    dynamic_representations.append({trait_name: attribute_name})
                else:
                    dynamic_representations[i][trait_name] = attribute_name

                    # TODO: unique case, if mask present - no neck nor head
                    if trait_name == 'mask' and dynamic_representations[i]['mask'] != 'none':
                        dynamic_representations[i]['neck'] = 'none'
                        dynamic_representations[i]['head'] = 'none'

        # Sort out dynamic unique representations
        dynamic_representations_unique = list(
            map(dict, set(tuple(sorted(rep.items())) for rep in dynamic_representations)))
        print('Dynamic unique representations:', len(dynamic_representations_unique))

        # Add ids to dynamic unique representations
        for i, rep in enumerate(dynamic_representations_unique):
            rep[representation_prop_id] = unique_representations_count + 1 + i

        # Write total representations to JSON
        representations = (unique_representations + dynamic_representations_unique)[:representations_count]

        print('Total representations:', len(unique_representations + dynamic_representations_unique))
        # pprint(representations)
        with open(representations_json_path, 'w') as representations_file:
            json.dump(representations, representations_file)
