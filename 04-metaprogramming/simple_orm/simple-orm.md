### Defining model

```
    >>> db = SqliteDatabase('people.db')

    >>> class User(Model):
    ...     name = CharField()
    ...     age = IntegerField()
    ...     is_active = BooleanField()
    ...
    ...     class Meta:
    ...         database = db
    
    >>> db.create_tables(User)
```

### Saving/updating instances

```
    >>> user = User(name='Ivan', age=20, is_active=False)
    >>> user.save()

    >>> user.is_active = True
    >>> suer.save()
```


### Fields

Common properties:

 * null
 * default

Filed types:

 - IntegerField(max_length, min_length)
 - CharField
 - Booleanfield


### Retrieving data

```
    >>> User.select().where(User.name == 'Ivan').get()  # returns iterator
    >>> User.select().where(User.name == 'Ivan').one()  # expects only one; raises Exception
    >>> User.select().where(User.name == 'Ivan').first()  # returns one instance or None
```

`whare` calls could be chained

```
    >>> User.select().where(User.name == 'Ivan').where(User.age == 20).get()
```

Query is executed only on call of `get`, `one` or `first`.


1. Supported complaisant operators:

 * `==`
 * `!=`
 * `<`, `<=`, `>`, `>=`
 * `startswith`, `endswith`, `cantains`
 * `in_`

2. Combining clauses:

```
    >>> User.select().where(or_(User.name == 'Ivan', User.age > 10)).get()
    >>> User.select().where(and_(User.name == 'Ivan', User.age == 10)).get()
```

3. Limiting fetched rows:

```
    >>> User.select().where(or_(User.name == 'Ivan', User.age > 10)).limit(10).get()
```

4. Fetching a subset of fields:

```
    >>> User.select(User.name, User.age).where(or_(User.name == 'Ivan', User.age > 10)).get(10)
```

... returns iterator of tuples

5. Calling DB functions:

```
    >>> User.select(User.name, User.age).where(to_lowercase(User.name) == 'ivan').get()
```

### Support multiple DBMS (SQLite and Postgres)
Make it possible to add new DBMS easy.

### Write functional test (that tests how the ORM works with real DBMS)
