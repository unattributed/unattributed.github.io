---
layout: post
title: "Migrating from iRedAdmin to PostfixAdmin on OpenBSD (MariaDB Repair + Dovecot Integration)"
date: 2025-11-08
author: unattributed
categories: [openbsd, mail, postfix, mariadb]
tags: [postfixadmin, iredmail, dovecot, php, mariadb, openbsd, migration]
---

### Context

OpenBSD 7.7 remains a clean foundation for hardened mail systems. iRedMail provides a fully integrated suite, but its administrative interface, iRedAdmin, is often too opinionated for those who prefer direct control. The goal here was to migrate an existing iRedMail deployment using `iRedAdmin` to the lighter `PostfixAdmin` interface without losing data, while repairing broken MariaDB privileges, resolving PHP-FPM errors, and integrating Dovecot password hashing correctly.

Environment used:
- OS: OpenBSD 7.7  
- Database: MariaDB 11.4.7  
- PHP: 8.3.26  
- Webroot: `/opt/www/postfixadmin/public`  
- PostfixAdmin: 3.3.15  

### Step 1: Preparing the Environment

First confirm `php83_fpm` and `nginx` are running correctly. Restart services to ensure configuration reloads cleanly:

```
# rcctl restart php83_fpm
# rcctl restart nginx
```

All PostfixAdmin templates reside under `/etc/nginx/templates`. The Roundcube and FastCGI templates provide a model for PostfixAdmin.

Create the web directory:

```
# mkdir -p /opt/www/postfixadmin/templates_c
# chown -R www:www /opt/www/postfixadmin
```

### Step 2: Configuring PostfixAdmin

Create `/opt/www/postfixadmin/config.local.php`:

```php
<?php
$CONF['configured'] = true;
$CONF['setup_password'] = '$2y$10$Z/r7RjLQM5gXnniVmlpQ6.M8r5bdpRoMU5Xc.ZxOTwY.7cCxDzo2C';
$CONF['database_type'] = 'mysqli';
$CONF['database_host'] = 'localhost';
$CONF['database_port'] = '3306';
$CONF['database_user'] = 'vmail';
$CONF['database_password'] = '********';
$CONF['database_name'] = 'vmail';
$CONF['database_prefix'] = '';
$CONF['encrypt'] = 'md5crypt';
$CONF['default_language'] = 'en';
$CONF['admin_email'] = 'postmaster@mail.example.net';
$CONF['postfix_admin_url'] = 'https://mail.example.net/postfixadmin';
?>
```

### Step 3: Enabling Required PHP Extensions

PostfixAdmin requires `mysqli` and `sqlite3`. Install the correct versions matching PHP 8.3:

```
# pkg_add php-mysqli-8.3.26 php-sqlite3-8.3.26
# cp /etc/php-8.3.sample/mysqli.ini /etc/php-8.3/
# cp /etc/php-8.3.sample/sqlite3.ini /etc/php-8.3/
# rcctl restart php83_fpm
```

Enable remote URL support for Composer:

```
# sed -i 's/^allow_url_fopen = Off/allow_url_fopen = On/' /etc/php-8.3.ini
```

### Step 4: Installing Dependencies with Composer

Composer isn’t bundled in OpenBSD by default, so fetch it manually:

```
# cd /opt/www/postfixadmin
# ftp https://getcomposer.org/download/latest-stable/composer.phar
# doas -u www php composer.phar install --no-dev --prefer-dist --no-interaction
```

After a long dependency pull, confirm `/opt/www/postfixadmin/vendor/autoload.php` exists and is owned by `www:www`.

### Step 5: Repairing MariaDB Privileges

The vmail user often lacks `CREATE` privileges inherited from iRedMail. Verify permissions with  
`mysql --defaults-file=/root/.my.cnf -e "SHOW GRANTS FOR 'vmail'@'localhost';"`.

If `GRANT ALL PRIVILEGES ON vmail.* TO 'vmail'@'localhost';` is missing, issue:

```
# mysql --defaults-file=/root/.my.cnf
MariaDB [(none)]> GRANT ALL PRIVILEGES ON vmail.* TO 'vmail'@'localhost';
MariaDB [(none)]> FLUSH PRIVILEGES;
MariaDB [(none)]> EXIT;
```

### Step 6: Fixing Dovecot Password Hash Integration

PostfixAdmin initially failed to use Dovecot’s `doveadm pw` due to a permission denial under `/var/run/dovecot/`. On OpenBSD, this socket is restricted. The workaround was to switch encryption from `dovecot:BLF-CRYPT` to `md5crypt` for interface usability, while Dovecot continues verifying existing BLF-CRYPT hashes in mailboxes.

### Step 7: Repairing the Database Schema

The upgrade utility (`public/upgrade.php`) reported missing indexes, duplicate keys, and absent columns. The sequence below resolved the upgrade from schema version 78 to 1851.

1. Back up each table before changes:  
   `mysqldump --defaults-file=/root/.my.cnf vmail admin > vmail_admin_pre79.sql`

2. Add missing indexes:  
   `ALTER TABLE vmail.admin ADD INDEX username (username);`

3. Add missing columns as required by upgrade logs:  
   `ALTER TABLE alias ADD COLUMN goto TEXT NOT NULL DEFAULT '';`

4. Resolve duplicate key conflicts by removing prior indexes:  
   `ALTER TABLE mailbox DROP INDEX domain;`  
   `ALTER TABLE alias DROP INDEX domain;`

5. Bump the version manually in `config`:  
   `UPDATE config SET value='655' WHERE name='version';`

Run the upgrade again until no SQL exceptions appear:  
`doas -u www php public/upgrade.php`

### Step 8: Correcting Postfix Domain Overlap

Postfix logged repetitive warnings:  
`warning: do not list domain mail.example.net in BOTH mydestination and virtual_mailbox_domains`

To eliminate these, edit `/etc/postfix/main.cf` and ensure `mail.example.net` appears **only** in `virtual_mailbox_domains`, not in `mydestination`.

Reload Postfix:

```
# postfix reload
```

### Step 9: Verification

- Access `https://mail.example.net/postfixadmin/`  
- Log in with `postmaster@mail.example.net` and verified credentials.  
- Confirm that listing domains, aliases, and mailboxes succeeds.  
- MariaDB query examples:

  - Show domains: `SELECT domain FROM domain;`
  - Show mailboxes: `SELECT username FROM mailbox;`
  - Show forwarders: `SELECT address, goto FROM alias WHERE goto != '';`

### Step 10: Conclusion

The system now operates with PostfixAdmin managing the same database iRedAdmin once controlled. This migration not only restored visibility into virtual domains and mailboxes but hardened the stack by removing legacy dependencies and reducing PHP exposure. Dovecot continues to authenticate using the existing BLF-CRYPT hashes, while PostfixAdmin safely creates new users using `md5crypt`.

All changes were performed on a live iRedMail system without downtime.  
The key takeaway: OpenBSD’s predictability simplifies recovery—if every SQL change and configuration reload is logged, even complex schema migrations become deterministic and reversible.

---