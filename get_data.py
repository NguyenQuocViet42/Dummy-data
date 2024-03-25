import mysql.connector
import yaml

with open('config.yaml', 'r', encoding='utf-8') as file:
    try:
        # Load nội dung YAML thành Python data structure
        config = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        print(exc)


connections = {    
    "employee_db": {
    'user': config['user'],
    'password': config['password'],
    'host': config['host'],
    'database': 'employee_db',
    'raise_on_warnings': True
    }
}

def get_employee():
    # Connection parameters
    db_name = 'employee_db'
    config_ = connections[db_name]

    try:
        # Establishing a connection to the database
        cnx = mysql.connector.connect(**config_)
        cursor = cnx.cursor()

        # Example query
        query = ("SELECT id FROM employee_db.employees where location_id={} and department_ids={};".format(int(config['location_id']), int(config['department_ids'])))

        # Executing the query
        cursor.execute(query)
        
        # Fetching all the rows
        rows = cursor.fetchall()

        # Extracting the column values into a list
        column_values = [str(row[0]) for row in rows]

        # Converting the list into a comma-separated string
        csv_data = ','.join(column_values)

        # Writing to a text file
        with open('data/employee.txt', 'w') as file:
            file.write(csv_data)

        print("Employee's datas successfully written to file.")
        cursor.close()
        cnx.close()

    except Exception as e:
        print(e)