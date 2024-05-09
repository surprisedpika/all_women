import csv
import argparse
import subprocess
import glob
import ruamel.yaml

parser = argparse.ArgumentParser(description='Create a git branch based on a column in a CSV file.')
parser.add_argument('ColumnName', type=str, help='The name of the column in the CSV file')

args = parser.parse_args()

route_files = glob.glob('../main.yaml') + glob.glob('../segments/*.yaml')
yaml = ruamel.yaml.YAML()

with open('translations.csv', 'r') as translation_file:
    reader = csv.reader(translation_file)
    headers = next(reader)  # Get the headers from the first line
        
    branch_name = args.ColumnName
    result = subprocess.run(['git', 'show-ref', '--verify', '--quiet', f'refs/heads/{branch_name}'])

    if result.returncode == 0:
        subprocess.run(['git', 'checkout', 'main'])
        subprocess.run(['git', 'branch', '-D', branch_name])
        subprocess.run(['git', 'checkout', '-b', branch_name])
    else:
        subprocess.run(['git', 'checkout', '-b', branch_name, 'main'])
        
    try:
        source_index = headers.index('en')
    except ValueError:
        print(f'Column "en" not found in CSV file.')
        exit(1)
    
    
        
    for row in reader:
      source_index = headers.index('en')
      column_index = headers.index(args.ColumnName)
      
      source = row[source_index]
      dest = row[column_index]
              
      print(f'Processing {source} -> {dest}')
      
      for route_file in route_files:
          with open(route_file, 'r') as file:
              
              print(f'Processing {route_file}')
              
              subprocess.run(['perl', '-i', '-pe', f's/(?<!-){source}/{dest}/g', route_file])
              
    subprocess.run(['git', 'add', '../main.yaml', '../segments/*.yaml'])
    subprocess.run(['git', 'commit', '-m', f'Translate {args.ColumnName}'])
    subprocess.run(['git', 'checkout', 'main'])