Title: Reclaiming space from a big table in Postgres
Date: 2021-05-08
Summary: After deleting columns or updating lots of rows.
Category: Programming
Tags: database, postgres

![Reclamed space from Postgres table](/images/Heroku-Postgres-Size.png "Reclamed space from Postgres table")


Shockingly to many, Postgres treats deletes and updates very similarly. Due to MVCC, tuples are considered dead/obsolete when they are not reachable by any active transaction, yet they remain physically on disk taking space in the table. This is called bloat, and it is the job of the autovacuum process, , which needs to run periodically, to re-use that space, but it does not reclaim it back to the system. This might be specially noticeable after a bulk update where a big portion of a table's rows is affected.

The same applies when some columns are deleted from a table, autovacuum won't help us here either. The `DROP COLUMN` does not physically remove the column, but simply [makes it invisible](https://www.postgresql.org/docs/current/sql-altertable.html#SQL-ALTERTABLE-NOTES) to SQL queries, to make this operation super fast. New update and insert queries store a `NULL` value on that column, but disk space will not be reclaimed until, over time, existing rows are updated.

To deal with this amount of bloat the solution is to run the `VACUUM FULL` command which takes an exclusive lock on the table and rewrites it completely.

If you cannot afford some downtime and this table is critical, then you can use [pg_repack](https://medium.com/miro-engineering/postgresql-bloat-pg-repack-and-deferred-constraints-d0ecf33337ec), a Postgres extension that can copy the content of the table by creating a shadow of it (which is also hot updated by triggers) and then performing a swap, which happens very fast.

Usually these solutions should only be considered when a significant amount of space needs to be reclaimed from within the table, otherwise, autovacuum should be good enough.
