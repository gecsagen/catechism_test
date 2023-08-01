-- Создание таблицы "Users"
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(55),
    email VARCHAR(100),
    email VARCHAR(155),
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    hashed_password VARCHAR(255)
);

-- Создание таблицы "TestCategory"
CREATE TABLE TestCategory (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);

-- Создание таблицы "Question"
CREATE TABLE Question (
    id SERIAL PRIMARY KEY,
    text TEXT,
    difficulty INTEGER CHECK (difficulty >= 1 AND difficulty <= 3),
    comment TEXT,
    test_name INTEGER,
    FOREIGN KEY (test_name) REFERENCES TestCategory(id)
);


-- Создание таблицы "Comment"
CREATE TABLE Comment (
    id SERIAL PRIMARY KEY,
    text TEXT,
    user_id INTEGER,
    question_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (question_id) REFERENCES Question(id)
);

-- Создание таблицы "Answer"
CREATE TABLE Answer (
    id SERIAL PRIMARY KEY,
    text TEXT,
    is_right BOOLEAN,
    question_id INTEGER,
    FOREIGN KEY (question_id) REFERENCES Question(id)
);

-- Создание таблицы "History"
CREATE TABLE History (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    test_name INTEGER,
    created_at TIMESTAMP,
    percentage_correct DOUBLE PRECISION,
    grade INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (test_name) REFERENCES TestCategory(id)
);

-- Создание таблицы "UserAnswer"
CREATE TABLE UserAnswer (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    question_id INTEGER,
    answer_id INTEGER,
    history_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (question_id) REFERENCES Question(id),
    FOREIGN KEY (answer_id) REFERENCES Answer(id),
    FOREIGN KEY (history_id) REFERENCES History(id)
);

-- Создание нового пользователя 'charlie' с паролем '12345'
CREATE USER charlie WITH PASSWORD '12345';

-- Предоставление необходимых привилегий новому пользователю
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO charlie;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO charlie;