alter table quizes drop column is_active;
alter table quizes add status varchar(20);
alter table questions add answer varchar(256);

drop view questions_all;

create or replace view questions_all as
    select q.question_id, q.title, q.question_type, q.picture, q.task, q.answer,
    (case when q.time_limit is null then qz.time_limit else q.time_limit end) as time_limit,
    c.category_id, c.name as category, q.quiz_id
    from questions q
    left join category_question cq on (q.question_id = cq.question_id)
    left join categories c on (cq.category_id = c.category_id)
    left join quizes qz on (q.quiz_id = qz.quiz_id);
