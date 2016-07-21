-- select * from suppliers;
-- select * from parts;
-- select * from catalog;

-- pnames of parts for which there is some supplier
select pname from parts 
where pid = any (select pid from catalog);

-- snames of suppliers who supply every part

select sname from suppliers S
where not exists 
(select pid from parts
where pid not in (select pid from catalog where sid = S.sid));

-- snames of suppliers who supply every red part

select sname from suppliers S
where not exists
(select pid from (select * from redparts) as r
where pid not in (select pid from catalog where sid = S.sid));


-- pnames of parts supplied by Acme Widget Suppliers and no one else

select pname from parts
where pid = any
(select catalog.pid from catalog 
 group by catalog.pid having every(catalog.sid = (select sid from suppliers where sname = 'Acme Widget Suppliers')));
 

-- sids of suppliers who charge more for some part than the average cost of that part 

select C.sid from catalog C,
(select catalog.pid as pid, avg(catalog.cost::numeric) as cost
from catalog group by catalog.pid) O where C.pid = O.pid and C.cost::numeric > O.cost;


--  sname of the supplier who charges the most for each part.

select sname as supplier, B.pid as part from suppliers S,
(select sid, T.pid from catalog C,
(select pid, max(cost) as c from catalog group by pid) as T
where C.pid = T.pid and C.cost = T.c) as B
where S.sid = B.sid;

--
create view redparts as select pid from parts where color = 'Red';
--
--
create view greenparts as select pid from parts where color = 'Green';
--

-- sids of suppliers who supply only red parts

select sid from catalog group by sid 
having every (pid in 
(select * from redparts));

-- sids of suppliers who supply a red part or a green part

select sid from catalog where pid = any (select * from greenparts) or pid = any (select * from redparts) group by sid;

-- sids of suppliers who supply a red part

select distinct sid from catalog where pid = any (select * from redparts);

-- sids of suppliers who supply a green part

select distinct sid from catalog where pid = any (select * from greenparts);

-- sids of suppliers who supply a red part and a green part

select sid from catalog where pid = any (select * from redparts)
intersect
select sid from catalog where pid = any (select * from greenparts);

-- for every supplier that only supplies green parts, print the name of the supplier and the total number of parts that she supplies

select sid, COUNT(*) from catalog group by sid 
having every (pid in 
(select * from greenparts));

-- for every supplier that supplies a green part and a reel(red?) part, print the name and price of the most expensive part that she supplies

create view redandgreen as 
select sid from catalog where pid = any (select * from redparts)
intersect
select sid from catalog where pid = any (select * from greenparts);

select sname, price
from suppliers S, 
(select sid, MAX(cost) as price from catalog where sid = ANY (select * from redandgreen) group by sid) as T
where S.sid = T.sid;


 