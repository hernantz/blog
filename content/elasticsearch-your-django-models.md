Title: Elasticsearch your Django models
Date: 2016-02-07
Category: Programming 
Tags: elasticsearch, python, django, search, celery
Summary: An indexing strategy to make your django models searchable
Status: draft


![Galileo](/images/django-elasticsearch.jpg "19th-century painting depicting Galileo Galilei displaying his telescope to Leonardo Donato in 1609.")

## Indexing strategies

From simplest to more complex:

1. Cron job. If your database is not that big, you could have a cron job to
   wipe the ES instance and re-index everything.
2. Last updated timestamp.
   Needs an index, if the table is updated too often then it may add performance penalty.
3. Indexing queue.
   Put pks in a queue.
   You can have a separate table (this way you avoid touching the source table db) or separate service like redis or a celery queue.
   different parts of the app enqueue the same task (object/id) how to dedupe? If it is a table with an index it is done, redis has sets? celery?
   https://blog.rapid7.com/2016/05/04/queuing-tasks-with-redis/
   https://stackoverflow.com/questions/26831103/avoiding-duplicate-tasks-in-celery-broker
   Deduplication is important because multiple model updates can imply just one document needed to be updated, some throttling is needed.
4. Event stream replication (kafka).

## Don't map your models to indexes
ES is not a relational DB, it works just fine with denormalyzed data.  So it
could well happen that an ES index contains data from two or more models. Ex. A
product document contains all it's sellers.  We will simply need a way to at
some point get back to a django model and for that we should store the `id`
somewhere.


mencionar el poisoned message
los retry

buenas practicas: late ack.

http://www.cogin.com/articles/SurvivingPoisonMessages.php#PoisonMessages
The question you are asking is a general problem of queue systems, sometimes called "poisonous message". You have to handle them in your business logic to be safe.

## Handling deletes
Para el borrado, usar soft deletes, luego se puede poner un proceso que borre definitivamente en batch. O el task que indexa
puede ver si los pks no existen mas y borrar el documento.



## Create and index and load data
What we need:
elasticsearch-py
elasticsearch-dsl-py
Elasticsearch > v2
connection settings and how to obtain a connection (singleton?)
to work with Elasticsearch we need elasticsearch node running
an index and a doctype
Management command
Mappings

## Vista de busqueda con paginacion
ES no es transaccional, devolviendo una vista paginada que se elimino un objeto del medio puede devolver menos resultados.

## Tests

## Document schema migrations
Elasticsearch is additive
you cannot change the same field type, but removing or adding 
fields from your mapping declaration will result in updates to 
the existing mapping always adding new fields.
Sumitting documents with new fields wont fail but succeed, following
the process mentioned above but with the exception that since we 
did not declare explicitly the new fields types, those will be left
for ES to interpret.

## Data migrations
Usar las migraciones de django para realizar cambios



http://bluesock.org/~willkg/blog/dev/elasticsearch_part1_index.html
http://www.opencrowd.com/blog/post/elasticsearch-django-tutorial/
https://github.com/liberation/django-elasticsearch
https://github.com/ChristopherRabotin/bungiesearch/blob/master/bungiesearch/__init__.py
https://github.com/jaddison/django-simple-elasticsearch
http://elasticutils.readthedocs.org/en/latest/django.html
https://www.youtube.com/watch?v=7FLXjgB0PQI&nohtml5=False
