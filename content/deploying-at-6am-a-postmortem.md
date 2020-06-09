Title: Deploying at 6am, a postmortem
Date: 2020-06-09
Category: Programming
Tags: devops 
Summary: Another chapter in the IT nightmare stories.

![Graph of number of active users](/images/demand.png "Graph of number of active users")

Our demand is pretty predictable. We thought it would be best to run deployments very early or very late hours. If they require downtime.

This time we needed to delete a lot of tables that were growing too much and adding too little with features that no one uses (think of event logs etc) which we replaced with logs. Making our backups and future db replications take longer.

So anyway at 6 am I started the deploy, once the app builds it runs the migrations, I put the site in maintenance mode, and the Django release command got stuck in running migrations.

I knew that drop table queries shouldn't take too long, they simply remove a directory from the disk. 

After waiting for more than 10 minutes it was time to check what the postgres db was doing.

You can basically check the logs or run queries against the `pg_stats_activity` table to get an idea of what's going on.

```sql
proddb=> SELECT pg_blocking_pids(pid) AS blocked_by
FROM pg_stat_activity
WHERE cardinality(pg_blocking_pids(pid)) > 0;
-[ RECORD 1 ]-------
blocked_by | {24484}
-[ RECORD 2 ]-------
blocked_by | {25741}
```

Let's inspect those pids

```sql
proddb=> select * from pg_stat_activity where pid = 24484;
-[ RECORD 1 ]----
datid            | 16402
datname          | proddb
pid              | 24484
usesysid         | 16384
usename          | produser
application_name | Heroku Postgres Backups
client_addr      | 52.73.131.14
client_hostname  | 
client_port      | 38811
backend_start    | 2020-06-09 09:09:20.920488+00
xact_start       | 2020-06-09 09:09:20.935983+00
query_start      | 2020-06-09 09:09:38.067414+00
state_change     | 2020-06-09 09:09:38.067415+00
wait_event_type  | Client
wait_event       | ClientWrite
state            | active
backend_xid      | 
backend_xmin     | 72354912
query            | COPY "public"."field_history_fieldhistory" ("id", "object_id", "field_name", "serialized_data", "date_created", "content_type_id", "user_id") TO stdout;
backend_type     | client backend
```
There is the culprit. I can see on `query_start` that it started just ten minutes after I began the deploy and the `application_name` is the Heroku automatic backups service. 

Turns out that when the site has low activity it is also a good time to run our db backups.

After checking the timestamps for previous backups I noticed they take two hours to complete. So I couldn't wait that long with the site down.

So I killed the query with:

```sql
proddb=>  SELECT pg_cancel_backend(24484);
 pg_cancel_backend 
-------------------
 t
```

Immediately after, the lock was freed and the release finished successfully.


