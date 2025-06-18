---
layout: post
title: "Primer - SQL common mistakes"
date: 2025-05-12
author: unattributed
categories: [sql]
tags: [secure-coding, sql, code-review]
---

# **SQL Common Coding Mistakes Cheat Sheet**  

## **1. SQL Injection**  
- **Never use raw input in queries**: Use parameterized queries or prepared statements.  
  ```sql
  -- Bad (Vulnerable to SQL injection)
  SELECT * FROM users WHERE username = '" + user_input + "';
  
  -- Good (Parameterized)
  SELECT * FROM users WHERE username = ?;  -- (Prepared statement)
  ```  

## **2. Missing Indexes**  
- **Slow queries?** Check if columns in `WHERE`, `JOIN`, `ORDER BY` are indexed.  
  ```sql
  -- Add an index if frequently queried
  CREATE INDEX idx_username ON users(username);
  ```  
- **Avoid unnecessary indexes** (slows down inserts/updates).  

## **3. Implicit Type Conversion**  
- **Comparing different types** (e.g., string vs number) can cause full table scans.  
  ```sql
  -- Bad (If 'id' is VARCHAR but compared to a number)
  SELECT * FROM users WHERE id = 123;
  
  -- Good (Explicit type matching)
  SELECT * FROM users WHERE id = '123';
  ```  

## **4. Cartesian Products (Cross Joins)**  
- **Missing `JOIN` conditions** lead to unintended huge results.  
  ```sql
  -- Bad (Returns all combinations)
  SELECT * FROM users, orders;
  
  -- Good (Explicit JOIN)
  SELECT * FROM users JOIN orders ON users.id = orders.user_id;
  ```  

## **5. NULL Handling**  
- **`NULL` comparisons require `IS NULL`/`IS NOT NULL`** (not `= NULL`).  
  ```sql
  -- Bad (Doesn't work)
  SELECT * FROM users WHERE deleted_at = NULL;
  
  -- Good
  SELECT * FROM users WHERE deleted_at IS NULL;
  ```  
- **Aggregate functions (`COUNT`, `SUM`) ignore `NULL` values**.  

## **6. GROUP BY Mistakes**  
- **Non-aggregated columns in `SELECT` must be in `GROUP BY`**.  
  ```sql
  -- Bad (May return arbitrary values)
  SELECT user_id, username, COUNT(*) FROM orders;
  
  -- Good
  SELECT user_id, username, COUNT(*) 
  FROM orders 
  GROUP BY user_id, username;
  ```  

## **7. Subquery Performance**  
- **Avoid `NOT IN` with NULLs** (returns no rows if subquery contains `NULL`).  
  ```sql
  -- Bad (Fails silently if subquery has NULL)
  SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM orders);
  
  -- Better (Use NOT EXISTS)
  SELECT * FROM users 
  WHERE NOT EXISTS (SELECT 1 FROM orders WHERE orders.user_id = users.id);
  ```  

## **8. Transaction Errors**  
- **Forgotten `COMMIT`/`ROLLBACK`** leads to locks or partial updates.  
  ```sql
  BEGIN TRANSACTION;
  UPDATE accounts SET balance = balance - 100 WHERE user_id = 1;
  UPDATE accounts SET balance = balance + 100 WHERE user_id = 2;
  COMMIT; -- Or ROLLBACK if error occurs
  ```  

## **9. Over-fetching Data**  
- **Avoid `SELECT *`** (fetch only needed columns).  
  ```sql
  -- Bad (Unnecessary data transfer)
  SELECT * FROM users;
  
  -- Good
  SELECT id, username FROM users;
  ```  

## **10. Date/Time Pitfalls**  
- **Time zones matter!** Store in UTC and convert on display.  
  ```sql
  -- Bad (Timezone-dependent)
  INSERT INTO logs (event_time) VALUES (NOW());
  
  -- Good (Explicit UTC)
  INSERT INTO logs (event_time) VALUES (UTC_TIMESTAMP());
  ```  

## **11. Case Sensitivity & Collation**  
- **`LIKE` vs `=`** (case sensitivity depends on collation).  
  ```sql
  -- May behave differently based on collation
  SELECT * FROM users WHERE username LIKE 'john%';
  SELECT * FROM users WHERE username = 'John';
  ```  

## **12. Deadlocks & Long-running Queries**  
- **Avoid holding locks too long** (optimize transactions).  
- **Use `EXPLAIN` to debug slow queries**.  

---  
**Debug Tools**:  
- `EXPLAIN QUERY PLAN` (SQLite) / `EXPLAIN ANALYZE` (PostgreSQL)  
- Query profiling (`SET profiling = 1;` in MySQL)  

*Keep this handy to avoid costly SQL mistakes!* 🚀