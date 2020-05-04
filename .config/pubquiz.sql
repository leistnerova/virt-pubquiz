create table users (
    user_id serial,
    password varchar(256) NOT NULL,
    name varchar(256) NOT NULL,
    is_active int DEFAULT 1,
    primary key (user_id)
);

insert into users (name, password) values('admin', 'sha256$61y4kwze$29006be6eae188269a27e9eff18f1da7017e5615c590f0ce744f59868bed6ce3'); 

create table quizes (
    quiz_id serial,
    title varchar(256) NOT NULL,
    quiz_type varchar(50) NOT NULL,
    random_order int DEFAULT 0,
    time_limit int,
    is_active int DEFAULT 1,
    from_dir varchar(256),
    primary key (quiz_id)
);

create table categories (
    category_id serial,
    quiz_id int NOT NULL REFERENCES quizes(quiz_id) ON DELETE CASCADE,
    name varchar(256) NOT NULL,
    picture varchar(256),
    primary key (category_id)
);

create table questions (
    question_id serial,
    quiz_id int NOT NULL REFERENCES quizes(quiz_id) ON DELETE CASCADE,
    title varchar(256),
    question_type varchar(50) NOT NULL,
    picture varchar(256),
    task text,
    time_limit int,
    primary key (question_id)
);

create table category_question (
    category_id int REFERENCES categories(category_id) ON DELETE CASCADE,
    question_id int REFERENCES questions(question_id) ON DELETE CASCADE,
    primary key (category_id, question_id)
);

create or replace view questions_all as
    select q.question_id, q.title, q.question_type, q.picture, q.task,
    (case when q.time_limit is null then qz.time_limit else q.time_limit end) as time_limit,
    c.category_id, c.name as category, q.quiz_id
    from questions q
    left join category_question cq on (q.question_id = cq.question_id)
    left join categories c on (cq.category_id = c.category_id)
    left join quizes qz on (q.quiz_id = qz.quiz_id);

create table quiz_run (
    run_id serial,
    question_actual int NOT NULL REFERENCES questions(question_id) ON DELETE CASCADE,
    question_next int REFERENCES questions(question_id) ON DELETE CASCADE,
    question_start timestamp,
    show_category_id int REFERENCES categories(category_id) ON DELETE CASCADE
);

create table teams (
    team_id serial,
    quiz_id int NOT NULL REFERENCES quizes(quiz_id) ON DELETE CASCADE,
    name varchar(256) NOT NULL,
    primary key (team_id)
);

create table team_users (
    team_user_id serial,
    team_id int NOT NULL REFERENCES teams(team_id) ON DELETE CASCADE,
    name varchar(256) NOT NULL,
    editor int default 0,
    primary key (team_user_id)
);

create table team_answers (
    team_id int NOT NULL REFERENCES teams(team_id) ON DELETE CASCADE,
    question_id int NOT NULL REFERENCES questions(question_id) ON DELETE CASCADE,
    answer text,
    points int default 0,
    primary key (team_id, question_id)
);
