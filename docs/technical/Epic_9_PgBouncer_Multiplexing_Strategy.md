### PgBouncer Connection Multiplexing Strategy

#### 1. Why the Async DB Refactor Shifts the Bottleneck
Before Epic 8, the app used synchronous database drivers. When a user requested data, the application thread would block (wait idly) until the database responded. Because app threads were tied up waiting, the application naturally throttled the number of concurrent queries hitting the DB.

By migrating to an **Asynchronous Architecture**, app threads no longer block. While waiting for PostgreSQL, the thread is freed up to handle hundreds of other incoming requests. Because the app can now process an exponentially higher volume of concurrent requests, it will attempt to open an exponentially higher number of concurrent connections to the database. 

PostgreSQL is notoriously bad at handling a high volume of direct connections (each connection forks a new OS process, consuming RAM). If a sudden surge of read-heavy marketplace traffic hits, the async app will effortlessly pass that surge directly to Postgres, causing it to crash due to Out-Of-Memory (OOM) errors. The bottleneck has shifted from **Application Compute** to **Database Connection Exhaustion**.

#### 2. What PgBouncer Connection Multiplexing Does
PgBouncer is a lightweight connection pooler that sits between the app and the database. 
*   **Client-Side Illusion:** PgBouncer allows the async app to open thousands of lightweight connections to PgBouncer. The app thinks it has a direct connection to the database.
*   **Server-Side Reality:** PgBouncer maintains a very small, fixed pool of actual, heavy connections to PostgreSQL (e.g., 50 connections).
*   **Multiplexing:** When the async app executes a query, PgBouncer temporarily "borrows" one of the 50 real database connections, routes the query, receives the result, passes it back to the app, and immediately returns the DB connection to the pool. Instead of 5,000 app connections forcing 5,000 DB processes, PgBouncer multiplexes those 5,000 client requests through the 50 persistent DB connections.

#### 3. Concrete Steps for Epic 9 (Marketplace Launch)
To actively manage this for the read-heavy marketplace, we must:
*   **Enforce Transaction Pooling:** Ensure `pool_mode = transaction` in `pgbouncer.ini` so connections are released back to the pool the millisecond a `SELECT` completes, rather than waiting for the client to disconnect.
*   **Implement Read-Replica Routing:** We cannot route all this through a single pool. We must provision PostgreSQL Read Replicas, deploy a dedicated PgBouncer instance pointing to them, and configure the application to route all `GET` marketplace queries to this read pool.
*   **Tune Timeouts:** Set `query_wait_timeout` to 5-10 seconds. It is better to return a fast 503 error to a user than to let the PgBouncer queue back up and crash the system.
*   **Deploy Alerting:** We must monitor the `cl_waiting` (Client Waiting Queue) metric. A spike here indicates the database is too slow or the pool size is too small, requiring immediate infrastructure scaling.