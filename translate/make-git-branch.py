import csv
import argparse
import subprocess
import glob
import re

parser = argparse.ArgumentParser(description='Create a git branch based on a column in a CSV file.')
parser.add_argument('ColumnName', type=str, help='The name of the column in the CSV file')

args = parser.parse_args()

route_files = glob.glob('../main.yaml') + glob.glob('../segments/*.yaml')

with open('translations.csv', 'r', encoding='utf-8') as translation_file:
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
    
    print (f'Processing {args.ColumnName}')
    
    for row in reader:
      source_index = headers.index('en')
      column_index = headers.index(args.ColumnName)
      
      source = row[source_index]
      dest = row[column_index]
              
    #   print(f'Processing {source} -> {dest}')
      
      for route_file in route_files:
          with open(route_file, 'r') as file:
            
              content = file.read()              
              content = re.sub(f'(?<!-){source}', dest, content)
              with open(route_file, 'w') as file:
                  file.write(content)
              
    subprocess.run(['git', 'add', '../main.yaml', '../segments/*.yaml'])
    subprocess.run(['git', 'commit', '-m', f'Translate {args.ColumnName}'])
    subprocess.run(['git', 'checkout', 'main'])