import json
# from pprint import pprint


# Generates traits, returns trait props names
def generate_traits(traits_csv_path: str, traits_json_path: str, trait_props_count: int) -> list:
    with open(traits_csv_path) as data:
        traits = {}
        # Collect all trait names
        trait_names = data.readline().strip().replace(',,', '').split(',')
        # TODO: 3 positional props same for each trait
        # Collect all trait props (same for each trait)
        trait_props_names = data.readline().strip().split(',', trait_props_count + 1)[:trait_props_count]

        # Read the rest of the lines
        for line in data:
            trait_start = 0
            trait_props_line = line.strip().split(',')

            # Add all possible attributes to each trait
            for trait_name in trait_names:
                trait_end = trait_start + trait_props_count
                trait_attribute_name = trait_props_line[trait_start]
                trait_props = trait_props_line[trait_start:trait_end]
                trait_attribute = dict(zip(trait_props_names, trait_props))
                trait_start = trait_end

                # If first trait prop (name) not empty
                if trait_attribute_name:
                    if trait_name in traits:
                        traits[trait_name].append(trait_attribute)
                    else:
                        traits[trait_name] = [trait_attribute]

        # Write traits to JSON
        # pprint(traits)
        with open(traits_json_path, 'w') as traits_file:
            json.dump(traits, traits_file)

    return trait_props_names
