-- db/schema.sql : baseline schema (MySQL 8 / MariaDB)
-- Run as root:  mysql -u root -p < db/schema.sql

CREATE DATABASE IF NOT EXISTS productivity
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE productivity;

CREATE TABLE IF NOT EXISTS contacts_contact (
  id          BIGINT       NOT NULL AUTO_INCREMENT,
  first_name  VARCHAR(100) NOT NULL,
  last_name   VARCHAR(100) NOT NULL,
  phone       VARCHAR(30)  NOT NULL,
  email       VARCHAR(254) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS journals_journal (
  id          BIGINT       NOT NULL AUTO_INCREMENT,
  title       VARCHAR(200) NOT NULL,
  content     LONGTEXT     NOT NULL,
  entry_date  DATE         NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS notes_note (
  id       BIGINT       NOT NULL AUTO_INCREMENT,
  title    VARCHAR(200) NOT NULL,
  content  LONGTEXT     NOT NULL,
  date     DATE         NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS tasks_task (
  id           BIGINT       NOT NULL AUTO_INCREMENT,
  name         VARCHAR(200) NOT NULL,
  description  LONGTEXT     NOT NULL,
  due_date     DATE         NULL,
  completed    TINYINT(1)   NOT NULL DEFAULT 0,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;