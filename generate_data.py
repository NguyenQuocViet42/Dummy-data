from datetime import datetime, timedelta
import random
import csv 
import yaml

with open('config.yaml', 'r', encoding='utf-8') as file:
    try:
        # Load nội dung YAML thành Python data structure
        config = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        print(exc)

with open('data/employee.txt', 'r') as file:
    # Read the entire content of the file
    content = file.read()

    # Split the content by commas to get individual values
    soon_employee_ids = content.split(',')[:int(config['number_soon_employee'])]
    late_employee_ids = content.split(',')[int(config['number_soon_employee']):int(config['number_soon_employee']) + int(config['number_late_employee'])]
    miss_employee_ids = content.split(',')[int(config['number_soon_employee']) + int(config['number_late_employee']):]
    

def generate_data():
    # Khởi tạo ngày bắt đầu và kết thúc
    start_date = datetime.strptime(config['start_date'], "%d/%m/%Y")
    end_date = datetime.strptime(config['end_date'], "%d/%m/%Y")
    start_time = config['start_time']
    end_time =  config['end_time']
    
    # Danh sách để lưu trữ các bản ghi
    records = []

    # Vòng lặp qua từng ngày trong khoảng thời gian đã cho
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() >= 5:
            current_date += timedelta(days=1)
            continue
        # Tạo bản ghi đi sớm
        for id in soon_employee_ids:
            department_id = config['department_ids']
            employee_id = id
            check_in_date = current_date.strftime("%Y-%m-%d")
            
            first_in = datetime.strptime(start_time, '%H:%M:%S')
            first_in = (first_in - timedelta(minutes=5)).strftime('%H:%M:%S')
            last_out = datetime.strptime(end_time, '%H:%M:%S')
            last_out = (last_out + timedelta(minutes=5)).strftime('%H:%M:%S')
            
            first_in = f"{check_in_date} " + first_in
            last_out = f"{check_in_date} " + last_out
            record = {
                "department": department_id,
                "employee": employee_id,
                "check_in_date": check_in_date,
                "first_in": first_in,
                "last_out": last_out,
                "report_type": "0",
                "status":"Đi sớm,Về muộn"
            }
            records.append(record)
            
        # Tạo bản ghi đi muộn
        for id in late_employee_ids:
            department_id = config['department_ids']
            employee_id = id
            check_in_date = current_date.strftime("%Y-%m-%d")
            
            first_in = datetime.strptime(start_time, '%H:%M:%S')
            first_in = (first_in + timedelta(minutes=6)).strftime('%H:%M:%S')
            last_out = datetime.strptime(end_time, '%H:%M:%S')
            last_out = (last_out + timedelta(minutes=5)).strftime('%H:%M:%S')
            
            first_in = f"{check_in_date} " + first_in
            last_out = f"{check_in_date} " + last_out
            record = {
                "department": department_id,
                "employee": employee_id,
                "check_in_date": check_in_date,
                "first_in": first_in,
                "last_out": last_out,
                "report_type": 'Chấm công muộn',
                "status":"Đi muộn,Về muộn"
            }
            records.append(record)
            
        # Tạo bản ghi không đi làm
        for id in miss_employee_ids:
            department_id = config['department_ids']
            employee_id = id
            check_in_date = current_date.strftime("%Y-%m-%d")
            
            first_in = datetime.strptime(start_time, '%H:%M:%S')
            first_in = (first_in + timedelta(minutes=6)).strftime('%H:%M:%S')
            last_out = datetime.strptime(end_time, '%H:%M:%S')
            last_out = (last_out + timedelta(minutes=0)).strftime('%H:%M:%S')
            
            first_in = f"{check_in_date} " + first_in
            last_out = f"{check_in_date} " + last_out
            record = {
                "department": department_id,
                "employee": employee_id,
                "check_in_date": check_in_date,
                "first_in": first_in,
                "last_out": last_out,
                "report_type": 'Chưa chấm công',
                "status":"Không đi"
            }
            records.append(record)
        # Chuyển sang ngày tiếp theo
        current_date += timedelta(days=1)

    # In ra số lượng bản ghi để xác nhận
    print(f"Total records created: {len(records)}")

    # Đường dẫn và tên tệp CSV để lưu các bản ghi
    csv_file_path = 'data/gen_data.csv'

    # Mở tệp CSV để ghi dữ liệu
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        # Khởi tạo DictWriter với các trường tương ứng với keys của bản ghi
        fieldnames = ['department', 'employee', 'check_in_date', 'first_in', 'last_out', 'report_type', 'status']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Ghi hàng tiêu đề
        writer.writeheader()
        
        # Ghi từng bản ghi vào tệp
        for record in records:
            writer.writerow(record)
            
if __name__ == '__main__':
    generate_data()