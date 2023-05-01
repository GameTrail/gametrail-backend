import json
import os

def split_json():
    json_file = os.path.join(os.getcwd(),'src', 'population', 'database.json')

    with open(json_file) as f:
        data = json.load(f)

    sorted_data = sorted(data, key=lambda x: x["id"])

    lotes = [sorted_data[i:i + 500] for i in range(0, len(sorted_data), 500)]

    for i, lote in enumerate(lotes):
        filename = f'database{i}.json'
        with open(os.path.join(os.getcwd(),'src', 'population', filename), 'w') as f:
            json.dump(lote, f)

split_json()




