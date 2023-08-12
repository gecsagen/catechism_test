-- Создание таблицы "Users"

CREATE TABLE
    Users (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name VARCHAR(55) NOT NULL,
        surname VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        is_active BOOLEAN DEFAULT TRUE,
        is_admin BOOLEAN DEFAULT FALSE,
        hashed_password VARCHAR(255) NOT NULL
    );

CREATE INDEX idx_user_email ON Users(email);

-- Создание таблицы "TestCategory"

CREATE TABLE
    TestCategory (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name VARCHAR(255) NOT NULL
    );

-- Создание таблицы "Question"

CREATE TABLE
    Question (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        text TEXT NOT NULL,
        difficulty INTEGER CHECK (
            difficulty >= 1
            AND difficulty <= 3
        ),
        comment TEXT,
        test_name UUID,
        FOREIGN KEY (test_name) REFERENCES TestCategory(id) ON DELETE RESTRICT ON UPDATE CASCADE
    );

CREATE INDEX idx_question_test_name ON Question(test_name);

-- Создание таблицы "Comment"

CREATE TABLE
    Comment (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        text TEXT NOT NULL,
        user_id UUID,
        question_id UUID,
        created_at TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE
        SET
            NULL ON UPDATE CASCADE,
            FOREIGN KEY (question_id) REFERENCES Question(id) ON DELETE CASCADE ON UPDATE CASCADE
    );
CREATE INDEX idx_comment_question_id ON Comment(question_id);

-- Создание таблицы "Answer"

CREATE TABLE
    Answer (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        text TEXT NOT NULL,
        is_right BOOLEAN NOT NULL,
        question_id UUID,
        FOREIGN KEY (question_id) REFERENCES Question(id) ON DELETE CASCADE ON UPDATE CASCADE
    );
CREATE INDEX idx_answer_is_right ON Answer(is_right);
-- Создание таблицы "History"

CREATE TABLE
    History (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        user_id UUID,
        test_name UUID,
        created_at TIMESTAMP,
        percentage_correct DOUBLE PRECISION,
        grade INTEGER,
        FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (test_name) REFERENCES TestCategory(id) ON DELETE RESTRICT ON UPDATE CASCADE
    );
    
CREATE INDEX idx_history_created_at ON History(created_at);
-- Создание таблицы "UserAnswer"

CREATE TABLE
    UserAnswer (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        user_id UUID,
        question_id UUID,
        answer_id UUID,
        history_id UUID,
        FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (question_id) REFERENCES Question(id) ON DELETE RESTRICT ON UPDATE CASCADE,
        FOREIGN KEY (answer_id) REFERENCES Answer(id) ON DELETE RESTRICT ON UPDATE CASCADE,
        FOREIGN KEY (history_id) REFERENCES History(id) ON DELETE CASCADE ON UPDATE CASCADE,
        CONSTRAINT unique_user_question_answer_history UNIQUE (user_id, question_id, answer_id, history_id)
    );