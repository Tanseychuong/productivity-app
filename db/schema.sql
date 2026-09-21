]633;E;{ echo "-- Baseline schema generated from Django migrations (MySQL)"\x3b for a in contacts journals notes tasks\x3b do python manage.py sqlmigrate $a 0001\x3b done\x3b } > db/schema.sql;1e7e88f8-72f5-4fc7-adaf-2ea6c0453c35]633;C-- Baseline schema generated from Django migrations (MySQL)
--
-- Create model Contact
--
CREATE TABLE `contacts_contact` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `first_name` varchar(100) NOT NULL, `last_name` varchar(100) NOT NULL, `phone` varchar(30) NOT NULL, `email` varchar(254) NOT NULL);
--
-- Create model Journal
--
CREATE TABLE `journals_journal` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `title` varchar(200) NOT NULL, `content` longtext NOT NULL, `entry_date` date NOT NULL);
--
-- Create model Note
--
CREATE TABLE `notes_note` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `title` varchar(200) NOT NULL, `content` longtext NOT NULL, `date` date NOT NULL);
--
-- Create model Task
--
CREATE TABLE `tasks_task` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(200) NOT NULL, `description` longtext NOT NULL, `due_date` date NULL, `completed` bool NOT NULL);
