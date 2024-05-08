import yaml

# Load the women.txt file
with open('women.txt', 'r') as file:
  women = file.readlines()

# Load the translate/NPC_USen.yaml file
with open('translate/NPC_USen.yaml', 'r') as file:
  translation = yaml.safe_load(file)

# Parse each line of women.txt
for woman in women:
  found = False
  woman = woman.strip()
  for actor_name, actor_data in translation['entries'].items():
    if 'contents' in actor_data:
        for content in actor_data['contents']:
            if 'text' in content and woman in content['text']:
                print(actor_name)
                found = True
                break
    if found:
        break
  else:
    print(woman)