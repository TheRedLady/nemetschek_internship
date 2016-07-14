### Exercise 1

Consider the following schema:
```
       Suppliers( sid: integer, sname: string, address: string)
       Parts(pid: integer, pname: string, color: string)
       Catalog( sid: integer, pid: integer, cost: real)
```

The `Catalog` relation lists the prices charged for parts by `Suppliers`.
Write the following queries in SQL:

1. Find the pnames of parts for which there is some supplier.
2. Find the snames of suppliers who supply every part.
3. Find the snames of suppliers who supply every red part.
4. Find the pnames of parts supplied by Acme Widget Suppliers and no one else.
5. Find the sids of suppliers who charge more for some part than the average cost of
that part (averaged over all the suppliers who supply that part).
6. For each part, find the sname of the supplier who charges the most for that part.
7. Find the sids of suppliers who supply only red parts.
8. Find the sids of suppliers who supply a red part anel a green part.
9. Find the sids of suppliers who supply a red part or a green part.
10. For every supplier that only supplies green parts, print the name of the supplier and the
total number of parts that she supplies.
11. For every supplier that supplies a green part and a reel part, print the name and price
of the most expensive part that she supplies.

### Exercise 2

The following relations keep track of airline flight information:

```
     Flights(flno: integer, from: string, to: string, distance: integer,
            departs: time, arrives: time, price: integer)
     Aircraft( aid: integer, aname: string, cruisingrange: integer)
     Certified( eid: integer, aid: integer)
     Employees( eid: integer ename: string, salary: integer)
```

Note that the `Employees` relation describes pilots and other kinds of employees as well; every
pilot is certified for some aircraft, and only pilots are certified to fly. Write each of the
follwing queries in SQL.

1. Find the names of aircraft such that all pilots certified to operate them earn more than
$80,000.
2. For each pilot who is certified for more than three aircraft, find the eid and the maximum
cruisingmnge of the aircraft for which she or he is certified.
3. Find the names of pilots whose salary is less than the price of the cheapest route from
Los Angeles to Honolulu.
4. For all aircraft with cmisingmnge over 1000 miles, find the name of the aircraft and the
average salary of all pilots certified for this aircraft.
5. Find the names of pilots certified for some Boeing aircraft.
6. Find the aids of all aircraft that can be used on routes from Los Angeles to Chicago.
7. Identify the routes that can be piloted by every pilot who makes more than $100,000.
8. Print the enames of pilots who can operate planes with cruisingmnge greater than 3000
miles but are not certified on any Boeing aircraft.
9. A customer wants to travel from Madison to New York with no more than two changes
of flight. List the choice of departure times from Madison if the customer wants to arrive
in New York by 6 p.m.
10. Compute the difference between the average salary of a pilot and the average salary of
all employees (including pilots).
11. Print the name and salary of every nonpilot whose salary is more than the average salary
for pilots.
12. Print the names of employees who are certified only on aircrafts with cruising range
longer than 1000 miles.
13. Print the names of employees who are certified only on aircrafts with cruising range
longer than 1000 miles, but on at least two such aircrafts.
14. Print the names of employees who are certified only on aircrafts with cruising range
longer than 1000 miles and who are certified on some Boeing aircraft.

### Exercise 3

Consider the following relational schema. An employee can work in more than
one department; the `pct_time` field of the `Works` relation shows the percentage of time that a
given employee works in a given department.

```
       Emp(eid: integer, ename: string, age: integer, salary: real)
       Works(eid: integer, did: integer, pct_time: integer)
       Dept(did: integer, budget: real, managerid: integer)
```

Write the following queries in SQL:

1. Print the names and ages of each employee who works in both the Hardware department
and the Software department.
2. For each department with more than 20 full-time-equivalent employees (i.e., where the
part~time and full-time employees add up to at least that many full-time employees),
print the did together with the number of employees that work in that department.
3. Print the name of each employee whose salary exceeds the budget of all of the depart-
ments that he or she works in.
4. Find the managerids of managers who manage only departments with budgets greater
than $1 million.
5. Find the enames of managers who manage the departments with the largest budgets.
6. If a manager manages more than one department, he or she controls the sum of all the
budgets for those departments. Find the managerids of managers who control more than
$5 million.
7. Find the managerids of managers who control the largest amounts.
8. Find the enames of managers who manage only departments with budgets larger than
\$1 million, but at least one department with budget less than $5 million.


### Exercise 4

Consider the instance of the Sailors relation:

| sid | sname | rating | age  |
------|-------|--------|-------
| 18  | jones | 3      | 30.0 |
| 41  | jonah | 6      | 56.0 |
| 22  | ahab  | 7      | 44.0 |
| 63  | moby  | null   | 15.0 |


1. Write SQL queries to compute the average rating, using `AVG` the sum of the ratings,
using `SUM`; and the number of ratings, using `COUNT`.
2. If you divide the sum just computed by the count, would the result be the same as the
average? How would your answer change if these steps were carried out with respect to
the age field instead of rating?
3. Consider the following query: Find the names of sailors with a higher rating than all
sailors with `age < 21`. The following two SQL queries attempt to obtain the answer
to this question. Do they both compute the result? If not, explain why. Under what
conditions would they compute the same result?

```
SELECT S.sname
FROM Sailors S
WHERE NOT EXISTS (
    SELECT * FROM Sailors S2 WHERE S2.age < 21 AND S.rating <= S2.rating
)

SELECT *
FROM Sailors S
WHERE S.rating > ANY (
    SELECT S2.rating FROM Sailors S2 WHERE S2.age < 21
)
```
