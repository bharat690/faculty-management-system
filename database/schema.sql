-- =====================================
-- USERS TABLE
-- =====================================

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    employee_id VARCHAR(20) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (
        role IN ('faculty', 'dean', 'admin')
    ),
    department VARCHAR(100),
    skills TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =====================================
-- SEMESTERS TABLE
-- =====================================

CREATE TABLE IF NOT EXISTS semesters (
    id SERIAL PRIMARY KEY,
    semester_name VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =====================================
-- DEPARTMENTS TABLE
-- =====================================

CREATE TABLE IF NOT EXISTS departments (
    id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) UNIQUE NOT NULL,
    department_code VARCHAR(20) UNIQUE NOT NULL
);


-- =====================================
-- ACADEMIC UNITS TABLE
-- (Department + Year + Section)
-- =====================================

CREATE TABLE IF NOT EXISTS academic_units (
    id SERIAL PRIMARY KEY,
    department_id INT REFERENCES departments(id)
        ON DELETE CASCADE,

    year INT NOT NULL CHECK (
        year BETWEEN 1 AND 4
    ),

    section VARCHAR(10) NOT NULL
);


-- =====================================
-- SUBJECTS TABLE
-- =====================================

CREATE TABLE IF NOT EXISTS subjects (
    id SERIAL PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL,
    subject_code VARCHAR(30) UNIQUE NOT NULL,

    department_id INT REFERENCES departments(id)
        ON DELETE CASCADE,

    year INT NOT NULL CHECK (
        year BETWEEN 1 AND 4
    )
);


-- =====================================
-- ATTENDANCE TABLE
-- =====================================

CREATE TABLE IF NOT EXISTS attendance (
    id SERIAL PRIMARY KEY,

    faculty_id INT REFERENCES users(id)
        ON DELETE CASCADE,

    semester_id INT REFERENCES semesters(id)
        ON DELETE CASCADE,

    attendance_date DATE NOT NULL,

    status VARCHAR(20) NOT NULL CHECK (
        status IN ('present', 'absent', 'leave')
    ),

    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(faculty_id, attendance_date)
);


-- =====================================
-- DAILY ACTIVITY LOGS TABLE
-- =====================================

CREATE TABLE IF NOT EXISTS daily_activity_logs (
    id SERIAL PRIMARY KEY,

    faculty_id INT REFERENCES users(id)
        ON DELETE CASCADE,

    semester_id INT REFERENCES semesters(id)
        ON DELETE CASCADE,

    activity_date DATE NOT NULL,

    slot_number INT NOT NULL CHECK (
        slot_number BETWEEN 1 AND 8
    ),

    start_time TIME NOT NULL,
    end_time TIME NOT NULL,

    task_type VARCHAR(50) NOT NULL CHECK (
        task_type IN (
            'Teaching',
            'Office Work',
            'Meeting',
            'Research',
            'Exam Duty',
            'Free',
            'Other'
        )
    ),

    academic_unit_id INT REFERENCES academic_units(id)
        ON DELETE SET NULL,

    subject_id INT REFERENCES subjects(id)
        ON DELETE SET NULL,

    remarks TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(faculty_id, activity_date, slot_number)
);


-- =====================================
-- WEEKLY SCHEDULE TEMPLATE
-- =====================================

CREATE TABLE IF NOT EXISTS weekly_schedule_templates (
    id SERIAL PRIMARY KEY,

    faculty_id INT REFERENCES users(id)
        ON DELETE CASCADE,

    day_of_week VARCHAR(20) NOT NULL CHECK (
        day_of_week IN (
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday'
        )
    ),

    slot_number INT NOT NULL CHECK (
        slot_number BETWEEN 1 AND 8
    ),

    task_type VARCHAR(50),

    academic_unit_id INT REFERENCES academic_units(id)
        ON DELETE SET NULL,

    subject_id INT REFERENCES subjects(id)
        ON DELETE SET NULL,

    remarks TEXT
);