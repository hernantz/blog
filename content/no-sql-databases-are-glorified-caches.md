Title: No-SQL databases are glorified caches
Date: 2021-04-26
Summary: Thoughts on SQL vs No-SQL databases.
Category: Programming
Tags: database, postgres, sql

![Photo by Jan Antonin Kolar](images/jan-antonin-kolar-lRoX0shwjUQ-unsplash.jpg "Archives - Photo by Jan Antonin Kolar")

In any modern project, the question to SQL or not to SQL will pop up, so it's important to define the fundamentals of each paradigm.


## Flexibility

At some stage in the life of your app, the API versioning will require that you maintain some degree of backwards compatibility in your schema, if your app is built on microservices or you have native clients and cannot guarantee that they will all be updated at the same time.

No-SQL databases are often praised for giving you a lot of flexibility on how to define your schema. But it turns out that schema can be greatly adaptive in SQL databases too. There are schema and data migrations that can be done by background processes. Although one has to [be aware](https://www.craigkerstiens.com/2017/09/10/better-postgres-migrations/) of which schema updates will hold a lock that might require downtime.

Moreover, Postgres has native support for JSON fields in case you need extra flexibility.

Probably something worth noticing is that in schema-less databases it is implied that correctness is checked at code level instead of within the database. Strong consistency and strong types are more reliable in traditional SQL databases.


## Pet vs Cattle

Scalability is an important aspect that distinguish both models. 

It is easier to scale document databases horizontally by adding more servers and sharding data across clusters.

SQL databases require a constant monitoring on how data is being accessed and which tables are growing the most. Query plans might change, queries become slow, new indexes might be needed, etc. 
SQL databases often offer a great deal [of parameters](https://postgresqlco.nf/tuning-guide) that can be tuned to increase the performance too.

It's common to have a master-follower setup, but you can only scale so much. At some point you will need to have a distributed cluster of servers that can scale horizontally.


## Queries 

In the No-SQL realm you don't join data by ids. You will often find that the database engine doesn't support this, and you have to do it in your code, probably resulting in more round trips to the database and reinventing many algorithms, hello bugs! Instead you denormalize heavily.

This limitation is not the only reason you de-normalize. De-normalization is encouraged if data is read more times than it is changed (or deleted).

How often are you retrieving the post author along with the post content? What about the comments? And now think how often authors will change their display name or profile picture.

A good reads vs writes ratio makes the case to optimize for the most common access pattern of your data, and yields better performance. You only pay the cost once an update occurs.

Now, de-normalization can also happen in a SQL world, but it is an optimization, not the first approach to model your data. In a document database, you have to think in advance how your data will be consumed by the client, and pre-format the documents that way, to minimize the number of round trips to get all the data needed to show a screen or render a widget. Almost like a chached REST API response.

[This is were the trade-off is](http://www.sarahmei.com/blog/2013/11/11/why-you-should-never-use-mongodb/), data has to be modeled beforehand. New aggregates, reports, new relationships, etc impose a challenge for document databases.

A document database is a glorified cache, a filterable filesystem that you can grep for some JSON, where files contain all you need (and more). It's performance and scalability comes at the expense of simplicity.

On that note, and to be fair, many document databases offer other interesting features that include: real time reactivity, offline support, streaming/merging changes, direct access to clients to handle thousands of simultaneous connections, where there's no need to convert JSON to SQL back and forth through an HTTP API.

On the other hand, [SQL might be a poor API](https://blog.nelhage.com/post/some-opinionated-sql-takes/), but it is powerful, and along with ACID, strong consistency, transactional updates, are features that are very important when dealing with money for example, not so much in a social network where transactions can be optimistic and consistency can be eventual.


## Conclusion

Nowadays with JSON fields and denormalization we can obtain many of the benefits of a document database, while keeping all the good parts a SQL database has to offer. I would even go as far as to claim that in all applications, you can't get away without a SQL system to run queries and aggregates. That being said, document databases might have a place in your stack, if you use them as a sort of scalable / filterable cache, while keeping a SQL source of truth around.