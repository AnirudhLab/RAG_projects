import mysql.connector

def fetch_upcoming_slots(conn):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        '''
        SELECT doctor_id, schedule_date, start_time, is_booked
        FROM doctor_schedule
        WHERE schedule_date >= CURDATE()
        ORDER BY schedule_date, start_time
        '''
    )
    rows = cursor.fetchall()
    cursor.close()
    return rows
