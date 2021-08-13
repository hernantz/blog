Title: Reclaiming space from a big table in Postgres
Date: 2021-05-08
Summary: After deleting columns or updating lots of rows.
Category: Programming
Tags: database, postgres

![Reclamed space from Postgres table](/images/Heroku-Postgres-Size.png "Reclamed space from Postgres table")


Shockingly to many, Postgres treats deletes and updates very similarly. Due to
MVCC, tuples are marked and considered dead/obsolete when they are not reachable
by any active transaction, yet they remain physically on disk taking space in
the table. This is called bloat. It is the job of the autovacuum process, which
needs to run periodically, to re-use that space. But it does not reclaim it back
to the system. This might be specially noticeable after a bulk update where a
big portion of a table's rows is affected (by an `UPDATE` or a `DELETE`), disk
space grows, and never shrinks back again.

The same applies when some columns are deleted from a table, autovacuum won't
help us here either. The `DROP COLUMN` does not physically remove the column,
but simply [makes it invisible][0] to SQL queries, in order to make this
operation super fast. New `UPDATE` or `INSERT` queries store a `NULL` value on
that column, but disk space will not be reclaimed or re-used until, over time,
existing rows are updated.

To deal with a huge amount of bloat the solution is to run the `VACUUM FULL`
command which takes an exclusive lock on the table and rewrites it completely.

If you cannot afford some downtime and this table is critical, then you can use
[pg_repack][1], a Postgres extension that will copy the content of the table by
creating a shadow clone of it (which is also hot updated by triggers) and then
performing a table rename swap, which happens very fast.

Usually these solutions should only be considered when a significant amount of
space needs to be reclaimed from within the table, otherwise, autovacuum should
be good enough.


[0]: https://www.postgresql.org/docs/current/sql-altertable.html#SQL-ALTERTABLE-NOTES
[1]: https://medium.com/miro-engineering/postgresql-bloat-pg-repack-and-deferred-constraints-d0ecf33337ec
