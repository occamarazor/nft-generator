import json
from pprint import pprint


# Generates attributes stats for dynamic images
def generate_attributes_stats(representations_json_path: str,
                              attributes_stats_json_path: str,
                              representation_prop_id: str,
                              unique_representations_count: int) -> None:
    with open(representations_json_path) as representations_file:
        dynamic_attr_map = {}
        representations = json.load(representations_file)
        # First 10 are unique reps
        dynamic_representations = representations[unique_representations_count:]

        for dynamic_rep in dynamic_representations:
            dynamic_attrs = [f'{key}/{val}'
                             for key, val in sorted(dynamic_rep.items())
                             if key != representation_prop_id
                             ]

            for dynamic_attr in dynamic_attrs:
                if dynamic_attr in dynamic_attr_map:
                    dynamic_attr_map[dynamic_attr] = dynamic_attr_map[dynamic_attr] + 1
                else:
                    dynamic_attr_map[dynamic_attr] = 1

        # Transform fractions to percentages
        dynamic_attr_chances = {key: f'{val / 100}%' for key, val in dynamic_attr_map.items()}

        # Write attributes stats to JSON
        print('Attributes count:', len(dynamic_attr_chances))
        pprint(dynamic_attr_chances)
        with open(attributes_stats_json_path, 'w') as attributes_stats_file:
            json.dump(dynamic_attr_chances, attributes_stats_file, indent=4)
