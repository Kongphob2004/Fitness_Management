# ============================================================
#  db.py — ชั้นติดต่อฐานข้อมูล
#  เขียน SQL ในไฟล์นี้ — ใช้ %s เป็น placeholder เสมอ
# ============================================================
from datetime import datetime

import mysql.connector
import config


def get_connection():
    return mysql.connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        port=config.DB_PORT
    )


def run_query(sql, params=None):
    """รัน SELECT คืนผลเป็น list ของ dict"""
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(sql, params or ())
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def run_command(sql, params=None):
    """รัน INSERT / UPDATE / DELETE แล้ว commit"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, params or ())
    conn.commit()
    out = {"new_id": cur.lastrowid, "affected": cur.rowcount}
    cur.close()
    conn.close()
    return out


def blank_to_none(value):
    """ช่องที่ไม่ได้กรอกในฟอร์มจะส่งมาเป็น "" — แปลงเป็น None (= NULL ใน SQL)"""
    return None if value in ("", None) else value


# ---------- สมาชิก (member) ----------
def search_members(filters):
    """ค้นหา สมาชิก ตามเงื่อนไข (name, gender, package_type)"""
    sql = "SELECT * FROM member WHERE 1=1"
    params = []

    if filters.get("name"):
        sql += " AND name LIKE %s"
        params.append("%" + filters["name"] + "%")

    if filters.get("gender"):
        sql += " AND gender = %s"
        params.append(filters["gender"])

    if filters.get("package_type"):
        sql += " AND package_type = %s"
        params.append(filters["package_type"])

    sql += " ORDER BY member_id"
    return run_query(sql, params)


def get_member(member_id):
    """ดึง สมาชิก 1 รายการตาม member_id"""
    rows = run_query(
        "SELECT * FROM member WHERE member_id = %s",
        (member_id,)
    )
    return rows[0] if rows else None


def create_member(data):
    """เพิ่ม สมาชิก ใหม่"""
    sql = """
        INSERT INTO member (name, phone, gender, join_date, package_type)
        VALUES (%s, %s, %s, %s, %s)
    """
    params = (
        data["name"],
        data["phone"],
        data["gender"],
        data["join_date"],
        data["package_type"]
    )
    return run_command(sql, params)


def update_member(member_id, data):
    """แก้ไข สมาชิก ตาม member_id"""
    sql = """
        UPDATE member
        SET name = %s,
            phone = %s,
            gender = %s,
            join_date = %s,
            package_type = %s
        WHERE member_id = %s
    """
    params = (
        data["name"],
        data["phone"],
        data["gender"],
        data["join_date"],
        data["package_type"],
        member_id
    )
    return run_command(sql, params)


def delete_member(member_id):
    """ลบ สมาชิก ตาม member_id"""
    return run_command(
        "DELETE FROM member WHERE member_id = %s",
        (member_id,)
    )

# ---------- เทรนเนอร์ (trainer) ----------

def search_trainers(filters):
    """ค้นหา เทรนเนอร์ ตามเงื่อนไข (name, specialty)"""
    sql = "SELECT * FROM trainer WHERE 1=1"
    params = []

    if filters.get("name"):
        sql += " AND name LIKE %s"
        params.append("%" + filters["name"] + "%")

    if filters.get("specialty"):
        sql += " AND specialty LIKE %s"
        params.append("%" + filters["specialty"] + "%")

    sql += " ORDER BY trainer_id"
    return run_query(sql, params)


def get_trainer(trainer_id):
    """ดึง เทรนเนอร์ 1 รายการตาม trainer_id"""
    rows = run_query(
        "SELECT * FROM trainer WHERE trainer_id = %s",
        (trainer_id,)
    )
    return rows[0] if rows else None


def create_trainer(data):
    """เพิ่ม เทรนเนอร์ ใหม่"""
    sql = """
        INSERT INTO trainer
            (name, phone, specialty)
        VALUES
            (%s, %s, %s)
    """

    params = (
        data["name"],
        data["phone"],
        data["specialty"]
    )

    return run_command(sql, params)


def update_trainer(trainer_id, data):
    """แก้ไข เทรนเนอร์ ตาม trainer_id"""
    sql = """
        UPDATE trainer
        SET name = %s,
            phone = %s,
            specialty = %s
        WHERE trainer_id = %s
    """

    params = (
        data["name"],
        data["phone"],
        data["specialty"],
        trainer_id
    )

    return run_command(sql, params)


def delete_trainer(trainer_id):
    """ลบ เทรนเนอร์ ตาม trainer_id"""
    return run_command(
        "DELETE FROM trainer WHERE trainer_id = %s",
        (trainer_id,)
    )

# ---------- อุปกรณ์ (equipment) ----------

def search_equipment(filters):
    """ค้นหา อุปกรณ์ ตามเงื่อนไข (name, zone, status)"""
    sql = "SELECT * FROM equipment WHERE 1=1"
    params = []

    if filters.get("name"):
        sql += " AND name LIKE %s"
        params.append("%" + filters["name"] + "%")

    if filters.get("zone"):
        sql += " AND zone LIKE %s"
        params.append("%" + filters["zone"] + "%")

    if filters.get("status"):
        sql += " AND status = %s"
        params.append(filters["status"])

    sql += " ORDER BY equip_id"
    return run_query(sql, params)


def get_equipment(equip_id):
    """ดึง อุปกรณ์ 1 รายการตาม equip_id"""
    rows = run_query(
        "SELECT * FROM equipment WHERE equip_id = %s",
        (equip_id,)
    )
    return rows[0] if rows else None


def create_equipment(data):
    """เพิ่ม อุปกรณ์ ใหม่"""
    sql = """
        INSERT INTO equipment
            (name, zone, quantity, status)
        VALUES
            (%s, %s, %s, %s)
    """

    params = (
        data["name"],
        data["zone"],
        data["quantity"],
        data["status"]
    )

    return run_command(sql, params)


def update_equipment(equip_id, data):
    """แก้ไข อุปกรณ์ ตาม equip_id"""
    sql = """
        UPDATE equipment
        SET name = %s,
            zone = %s,
            quantity = %s,
            status = %s
        WHERE equip_id = %s
    """

    params = (
        data["name"],
        data["zone"],
        data["quantity"],
        data["status"],
        equip_id
    )

    return run_command(sql, params)


def delete_equipment(equip_id):
    """ลบ อุปกรณ์ ตาม equip_id"""
    return run_command(
        "DELETE FROM equipment WHERE equip_id = %s",
        (equip_id,)
    )

# ---------- คลาสเรียน (gym_class) ----------
def search_classes(filters):
    """ค้นหา คลาสเรียน พร้อมคำนวณจำนวนที่นั่งว่าง"""
    sql = """
        SELECT
            gc.class_id,
            gc.name,
            gc.trainer_id,
            gc.room,
            gc.capacity,
            gc.schedule_time,
            gc.capacity - IFNULL(b.booked_count, 0) AS seats_left
        FROM gym_class gc
        LEFT JOIN (
            SELECT class_id, COUNT(*) AS booked_count
            FROM booking
            WHERE status = 'booked'
            GROUP BY class_id
        ) b ON gc.class_id = b.class_id
        WHERE 1=1
    """
    params = []

    if filters.get("name"):
        sql += " AND gc.name LIKE %s"
        params.append("%" + filters["name"] + "%")

    if filters.get("room"):
        sql += " AND gc.room LIKE %s"
        params.append("%" + filters["room"] + "%")

    sql += " ORDER BY gc.class_id"
    return run_query(sql, params)


def get_class(class_id):
    """ดึง คลาสเรียน 1 รายการตาม class_id"""
    rows = run_query(
        "SELECT * FROM gym_class WHERE class_id = %s",
        (class_id,)
    )
    return rows[0] if rows else None

def get_class_rooms():
    sql = """
        SELECT DISTINCT TRIM(room) AS room
        FROM gym_class
        WHERE room IS NOT NULL
          AND TRIM(room) <> ''
        ORDER BY room
    """
    return run_query(sql)

def create_class(data):
    """เพิ่ม คลาสเรียน ใหม่"""
    sql = """
        INSERT INTO gym_class
            (name, trainer_id, room, capacity, schedule_time)
        VALUES
            (%s, %s, %s, %s, %s)
    """
    params = (
        data["name"],
        data["trainer_id"],
        data["room"],
        data["capacity"],
        data["schedule_time"]
    )
    return run_command(sql, params)


def update_class(class_id, data):
    """แก้ไข คลาสเรียน ตาม class_id"""
    sql = """
        UPDATE gym_class
        SET name = %s,
            trainer_id = %s,
            room = %s,
            capacity = %s,
            schedule_time = %s
        WHERE class_id = %s
    """
    params = (
        data["name"],
        data["trainer_id"],
        data["room"],
        data["capacity"],
        data["schedule_time"],
        class_id
    )
    return run_command(sql, params)


def delete_class(class_id):
    """ลบ คลาสเรียน ตาม class_id"""
    return run_command(
        "DELETE FROM gym_class WHERE class_id = %s",
        (class_id,)
    )


# ---------- การจอง (booking) ----------
def search_bookings(filters):
    """ค้นหา การจอง ตามเงื่อนไข (member_id, class_id, status)"""
    sql = "SELECT * FROM booking WHERE 1=1"
    params = []

    if filters.get("member_id") not in (None, ""):
        sql += " AND member_id = %s"
        params.append(filters["member_id"])

    if filters.get("class_id") not in (None, ""):
        sql += " AND class_id = %s"
        params.append(filters["class_id"])

    if filters.get("status"):
        sql += " AND status = %s"
        params.append(filters["status"])

    sql += " ORDER BY booking_id"
    return run_query(sql, params)


def get_booking(booking_id):
    """ดึง การจอง 1 รายการตาม booking_id"""
    rows = run_query(
        "SELECT * FROM booking WHERE booking_id = %s",
        (booking_id,)
    )
    return rows[0] if rows else None


def check_can_book(member_id, class_id, booking_id=None):
    """
    ตรวจสอบก่อนบันทึกการจอง:
    1. คลาสต้องมีอยู่จริงและยังมีที่นั่ง
    2. สมาชิกห้ามมีการจอง booked ซ้ำในคลาสเดียวกัน
    """
    booking_id = booking_id or 0

    # ตรวจสอบคลาสและจำนวนที่นั่ง
    sql = """
        SELECT
            gc.capacity,
            (
                SELECT COUNT(*)
                FROM booking b
                WHERE b.class_id = gc.class_id
                  AND b.status = 'booked'
                  AND b.booking_id <> %s
            ) AS booked_count
        FROM gym_class gc
        WHERE gc.class_id = %s
    """
    rows = run_query(sql, (booking_id, class_id))

    if not rows:
        raise ValueError("ไม่พบคลาสนี้")

    capacity = rows[0]["capacity"]
    booked_count = rows[0]["booked_count"]

    if capacity - booked_count <= 0:
        raise ValueError("คลาสนี้เต็มแล้ว")

    # ตรวจสอบการจองซ้ำ
    sql = """
        SELECT booking_id
        FROM booking
        WHERE member_id = %s
          AND class_id = %s
          AND status = 'booked'
          AND booking_id <> %s
        LIMIT 1
    """
    duplicate = run_query(sql, (member_id, class_id, booking_id))

    if duplicate:
        raise ValueError("สมาชิกคนนี้จองคลาสนี้แล้ว")


def create_booking(data):
    """เพิ่ม การจอง ใหม่"""
    if data["status"] == "booked":
        check_can_book(
            data["member_id"],
            data["class_id"]
        )

    sql = """
        INSERT INTO booking
            (member_id, class_id, booking_date, status)
        VALUES
            (%s, %s, %s, %s)
    """
    params = (
        data["member_id"],
        data["class_id"],
        data["booking_date"],
        data["status"]
    )
    return run_command(sql, params)


def update_booking(booking_id, data):
    """แก้ไข การจอง ตาม booking_id"""
    old = get_booking(booking_id)

    if not old:
        raise ValueError("ไม่พบรายการจองนี้")

    # ถ้าสถานะใหม่เป็น booked และ
    # เดิม cancelled หรือมีการเปลี่ยนสมาชิก/คลาส ต้องตรวจสอบใหม่
    if data["status"] == "booked":
        if (
            old["status"] != "booked"
            or old["member_id"] != data["member_id"]
            or old["class_id"] != data["class_id"]
        ):
            check_can_book(
                data["member_id"],
                data["class_id"],
                booking_id
            )

    sql = """
        UPDATE booking
        SET member_id = %s,
            class_id = %s,
            booking_date = %s,
            status = %s
        WHERE booking_id = %s
    """
    params = (
        data["member_id"],
        data["class_id"],
        data["booking_date"],
        data["status"],
        booking_id
    )
    return run_command(sql, params)


def delete_booking(booking_id):
    """ลบ การจอง ตาม booking_id"""
    return run_command(
        "DELETE FROM booking WHERE booking_id = %s",
        (booking_id,)
    )

# ---------- MEMBER CHECKIN ----------

def search_member_checkins(filters):
    sql = """
        SELECT
            mc.checkin_id,
            mc.member_id,
            m.name AS member_name,
            mc.checkin_time,
            mc.checkout_time
        FROM member_checkin mc
        INNER JOIN member m
            ON mc.member_id = m.member_id
        WHERE 1=1
    """
    params = []

    if filters.get("member_id"):
        sql += " AND mc.member_id = %s"
        params.append(filters["member_id"])

    if filters.get("member_name"):
        sql += " AND m.name LIKE %s"
        params.append("%" + filters["member_name"].strip() + "%")

    sql += " ORDER BY mc.checkin_time DESC"

    return run_query(sql, params)


def get_member_checkin(checkin_id):
    rows = run_query(
        """
        SELECT checkin_id, member_id,
               checkin_time, checkout_time
        FROM member_checkin
        WHERE checkin_id = %s
        """,
        (checkin_id,)
    )
    return rows[0] if rows else None


def create_member_checkin(data):
    member_id = data.get("member_id")
    checkin_time = blank_to_none(data.get("checkin_time"))
    checkout_time = blank_to_none(data.get("checkout_time"))

    if not member_id:
        raise ValueError("กรุณาเลือกสมาชิก")

    if not checkin_time:
        checkin_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    checkin_time = str(checkin_time).replace("T", " ")

    if checkout_time:
        checkout_time = str(checkout_time).replace("T", " ")
        if checkout_time < checkin_time:
            raise ValueError("เวลาออกต้องไม่ก่อนเวลาเข้า")

    return run_command(
        """
        INSERT INTO member_checkin
            (member_id, checkin_time, checkout_time)
        VALUES (%s, %s, %s)
        """,
        (member_id, checkin_time, checkout_time)
    )


def update_member_checkin(checkin_id, data):
    member_id = data.get("member_id")
    checkin_time = blank_to_none(data.get("checkin_time"))
    checkout_time = blank_to_none(data.get("checkout_time"))

    if not member_id or not checkin_time:
        raise ValueError("กรุณาเลือกสมาชิกและระบุเวลาเข้าใช้")

    checkin_time = str(checkin_time).replace("T", " ")

    if checkout_time:
        checkout_time = str(checkout_time).replace("T", " ")
        if checkout_time < checkin_time:
            raise ValueError("เวลาออกต้องไม่ก่อนเวลาเข้า")

    return run_command(
        """
        UPDATE member_checkin
        SET member_id = %s,
            checkin_time = %s,
            checkout_time = %s
        WHERE checkin_id = %s
        """,
        (member_id, checkin_time, checkout_time, checkin_id)
    )


def delete_member_checkin(checkin_id):
    return run_command(
        "DELETE FROM member_checkin WHERE checkin_id = %s",
        (checkin_id,)
    )

# ============================================================
# REPORT
# ============================================================
def report_summary():
    """ตัวเลขสรุปบน dashboard"""
    sql = """
        SELECT
            (SELECT COUNT(*) FROM member) AS 'สมาชิก',
            (SELECT COUNT(*) FROM gym_class) AS 'คลาส',
            (SELECT COUNT(*) FROM trainer) AS 'เทรนเนอร์',
            (SELECT COUNT(*)
             FROM booking
             WHERE status = 'booked') AS 'การจอง',

            (SELECT COUNT(*)
             FROM equipment
             WHERE status = 'available') AS 'อุปกรณ์พร้อมใช้',

            (SELECT COUNT(*)
             FROM booking
             WHERE status = 'cancelled') AS 'การจองที่ยกเลิก'
    """
    return run_query(sql)[0]


def report_popular_classes():
    """📈 คลาสยอดนิยม (Most Booked)"""
    sql = """
        SELECT
            gc.class_id,
            gc.name AS class_name,
            COUNT(b.booking_id) AS booking_count
        FROM booking b
        INNER JOIN gym_class gc
            ON b.class_id = gc.class_id
        WHERE b.status = 'booked'
        GROUP BY gc.class_id, gc.name
        ORDER BY booking_count DESC
        LIMIT 5
    """
    return run_query(sql)


def report_trainers_above_avg():
    """🏅 เทรนเนอร์ที่มีผู้จองมากกว่าค่าเฉลี่ย"""
    sql = """
        SELECT
            t.trainer_id,
            t.name AS trainer_name,
            COUNT(b.booking_id) AS booking_count
        FROM trainer t
        INNER JOIN gym_class gc
            ON t.trainer_id = gc.trainer_id
        INNER JOIN booking b
            ON gc.class_id = b.class_id
        WHERE b.status = 'booked'
        GROUP BY t.trainer_id, t.name
        HAVING COUNT(b.booking_id) > (
            SELECT AVG(trainer_booking_count)
            FROM (
                SELECT
                    t2.trainer_id,
                    COUNT(b2.booking_id) AS trainer_booking_count
                FROM trainer t2
                LEFT JOIN gym_class gc2
                    ON t2.trainer_id = gc2.trainer_id
                LEFT JOIN booking b2
                    ON gc2.class_id = b2.class_id
                   AND b2.status = 'booked'
                GROUP BY t2.trainer_id
            ) AS trainer_counts
        )
        ORDER BY booking_count DESC
    """
    return run_query(sql)


def report_class_equipment():
    """🧰 อุปกรณ์ที่ใช้ในแต่ละคลาส"""
    sql = """
        SELECT
            gc.class_id,
            gc.name AS class_name,
            e.equip_id,
            e.name AS equipment_name,
            ce.quantity_used
        FROM class_equipment ce
        INNER JOIN gym_class gc
            ON ce.class_id = gc.class_id
        INNER JOIN equipment e
            ON ce.equip_id = e.equip_id
        ORDER BY gc.class_id, e.equip_id
    """
    return run_query(sql)

def report_top_member_checkins():
    """สมาชิกที่เข้าใช้ Fitness บ่อยที่สุด"""
    sql = """
        SELECT
            m.member_id,
            m.name AS member_name,
            COUNT(mc.checkin_id) AS total_checkins
        FROM member_checkin mc
        INNER JOIN member m
            ON mc.member_id = m.member_id
        GROUP BY m.member_id, m.name
        ORDER BY total_checkins DESC, m.member_id ASC
        LIMIT 10
    """
    return run_query(sql)

def get_trainer_specialties():
    sql = """
        SELECT DISTINCT TRIM(specialty) AS specialty
        FROM trainer
        WHERE specialty IS NOT NULL
          AND TRIM(specialty) <> ''
        ORDER BY specialty
    """
    return run_query(sql)

def get_equipment_zones():
    sql = """
        SELECT DISTINCT TRIM(zone) AS zone
        FROM equipment
        WHERE zone IS NOT NULL
          AND TRIM(zone) <> ''
        ORDER BY zone
    """
    return run_query(sql)

# ============================================================
#  รายการรายงานที่แสดงบนหน้า /report
# ============================================================
REPORTS = [
    ("popular-classes", "📈 คลาสยอดนิยม (Most Booked)", report_popular_classes),
    ("top-trainers", "🏅 เทรนเนอร์ที่มีผู้จองมากกว่าค่าเฉลี่ย (Above Average)", report_trainers_above_avg),
    ("class-equipment", "🧰 อุปกรณ์ที่ใช้ในแต่ละคลาส (Join 3 Tables)", report_class_equipment),
    ("top-member-checkins","🏋️ สมาชิกที่เข้าใช้ Fitness บ่อยที่สุด",report_top_member_checkins),
]