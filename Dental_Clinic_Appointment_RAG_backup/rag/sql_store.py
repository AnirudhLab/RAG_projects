import mysql.connector

def get_db_conn(config):
    return mysql.connector.connect(**config)

def fetch_upcoming_slots(conn):
    """
    Returns a list of dicts with:
      doctor_name, schedule_date, start_time, is_booked
    """
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """
        SELECT
          d.name AS doctor_name,
          s.schedule_date,
          s.start_time,
          s.is_booked
        FROM doctor_schedule s
        JOIN doctors d
          ON s.doctor_id = d.doctor_id
        WHERE s.schedule_date >= CURDATE()
        ORDER BY s.schedule_date, s.start_time
        """
    )
    rows = cur.fetchall()
    cur.close()
    return rows

def book_slot(conn, patient_info, doctor_id: int, date: str, time: str) -> bool:
    cur = conn.cursor()
    q = (
        "UPDATE doctor_schedule "
        "SET is_booked=1, booked_at=NOW(), patient_id=%s "
        "WHERE doctor_id=%s AND schedule_date=%s AND start_time=%s AND is_booked=0"
    )
    params = (patient_info.get('id', None), doctor_id, date, time)
    cur.execute(q, params)
    conn.commit()
    success = cur.rowcount == 1
    cur.close()
    return success
