import mysql.connector
import pandas as pd
from tqdm import tqdm
import yaml
from generate_data import generate_data
from get_data import get_employee

with open('config.yaml', 'r', encoding='utf-8') as file:
    try:
        # Load nội dung YAML thành Python data structure
        config = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        print(exc)


connections = {
    "history_db": {
    'user': config['user'],
    'password': config['password'],
    'host': config['host'],
    'database': 'history_db',
    'raise_on_warnings': True
    }
}

# Connection parameters
config_ = connections['history_db']
cnx = mysql.connector.connect(**config_)
cursor = cnx.cursor()


def execute_insert(insert_query):
    try:
        # Executing the query
        cursor.execute(insert_query)
        cnx.commit()
    except Exception as e:
        print(e)

if __name__ == '_main_':
    # Get Employee's ID's
    get_employee()
    # Generate Data:
    generate_data()
    
    df = pd.read_csv('data/gen_data.csv')
    for i in tqdm(range(len(df))):
        row = df.iloc[i]
        if row['report_type'] != 'Chưa chấm công':
            insert_query = "INSERT INTO history_db.first_in_last_out_histories \
                        (    camera_id,   employee_id,      location_id      ,     shift_id,            report_type,              first_in,          check_in_date,	    shift_time_id,            department_id,        last_out,         created_at,       updated_at) \
                values	(   \'{}\'      ,	 \'{}\'    ,	    \'{}\'             ,     \'{}\',	            \'{}\'	,                   \'{}\'   ,	        \'{}\'	    ,	        \'{}\'	       ,            \'{}\'     ,            \'{}\',             \'{}\',             \'{}\');"\
            .format(config['camera_id'],    row['employee'],    config['location_id'],   config['shift_id'],    row['status'],      row['first_in'],    row['check_in_date'],   config['shift_time_id'],    row['department'],      row['last_out'],    row['first_in'],    row['last_out'])
            execute_insert(insert_query)
        
        if row['report_type'] != "0" and config['run_notifications'] != '0':
            insert_query = "INSERT INTO history_db.notification_histories \
                        (    camera_id,   employee_id,      location_id      ,     shift_id,            report_type,         notify_date,	        shift_time_id,            department_id,         created_at,       updated_at        ,time             ,type          ) \
                values	(   \'{}\'      ,	 \'{}\'    ,	    \'{}\'             ,     \'{}\',	            \'{}\'	,              \'{}\'	    ,	        \'{}\'	       ,            \'{}\'     ,            \'{}\',             \'{}\'              ,\'{}\'             ,\'{}\'          );"\
            .format(config['camera_id'],    row['employee'],    config['location_id'],   config['shift_id'],    row['report_type'],    row['check_in_date'],    config['shift_time_id'],    row['department'],      row['first_in'],    row['last_out']     ,row['first_in']    ,'Chấm công' )
            execute_insert(insert_query)
        # break
        
        
    cursor.close()
    cnx.close()