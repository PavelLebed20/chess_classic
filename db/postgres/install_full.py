#########################################
# MODULE: Install database environment  #
# AUTHOR: Lebed' Pavel                  #
# LAST UPDATE: 10/04/2019               #
#########################################
import os

password = 'postgres'
user = 'postgres'
host = 'localhost'
database = 'Chess'
port = '5432'

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)


def get_execution_command(file_rel_path):
    return ' && PGPASSWORD={6} psql -h {0} -d {1} -U {2} -p {3} -a -w -f {4}\\{5}' \
           ''.format(host, database, user, port, dir_path, file_rel_path, password)


commands_str = 'set PGPASSWORD={0}'.format(password)

commands_str += get_execution_command('SCH\\tables_full.sql')

commands_str += get_execution_command('SCH\\tables_data.sql')

# add api scripts
api_files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(dir_path + '\\API\\'):
    for file in f:
        api_files.append(os.path.join(file))

for file in api_files:
    commands_str += get_execution_command('API\\{0}'.format(file))

os.system(commands_str)

