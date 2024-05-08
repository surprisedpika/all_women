import yaml
import argparse

parser = argparse.ArgumentParser(description='Process a translation YAML file.')
parser.add_argument('TranslationFile', type=str, help='The translation YAML file')
args = parser.parse_args()

with open('actors.txt', 'r') as file:
  actors = file.readlines()

with open(args.TranslationFile, 'r') as file:
  translation = yaml.safe_load(file)

# Parse each line of actors.txt
for actor in actors:
  actor = actor.strip()
  for actor_name, actor_data in translation['entries'].items():
    if actor == actor_name:
      if 'contents' in actor_data:
          for content in actor_data['contents']:
              if 'text' in content:
                  print(content['text'])
                  break
      break
  else:
    print(actor)