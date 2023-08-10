-- Создание таблицы "Users"
CREATE TABLE Users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(55),
    surname VARCHAR(100),
    email VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    hashed_password VARCHAR(255)
);

-- Создание таблицы "TestCategory"
CREATE TABLE TestCategory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255)
);

-- Создание таблицы "Question"
CREATE TABLE Question (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    text TEXT,
    difficulty INTEGER CHECK (difficulty >= 1 AND difficulty <= 3),
    comment TEXT,
    test_name UUID,
    FOREIGN KEY (test_name) REFERENCES TestCategory(id)
);


-- Создание таблицы "Comment"
CREATE TABLE Comment (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    text TEXT,
    user_id UUID,
    question_id UUID,
    created_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (question_id) REFERENCES Question(id)
);

-- Создание таблицы "Answer"
CREATE TABLE Answer (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    text TEXT,
    is_right BOOLEAN,
    question_id UUID,
    FOREIGN KEY (question_id) REFERENCES Question(id)
);

-- Создание таблицы "History"
CREATE TABLE History (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID,
    test_name UUID,
    created_at TIMESTAMP,
    percentage_correct DOUBLE PRECISION,
    grade INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (test_name) REFERENCES TestCategory(id)
);

-- Создание таблицы "UserAnswer"
CREATE TABLE UserAnswer (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID,
    question_id UUID,
    answer_id UUID,
    history_id UUID,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (question_id) REFERENCES Question(id),
    FOREIGN KEY (answer_id) REFERENCES Answer(id),
    FOREIGN KEY (history_id) REFERENCES History(id)
);