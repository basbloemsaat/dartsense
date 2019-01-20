PRAGMA synchronous = OFF;
PRAGMA journal_mode = MEMORY;

DROP TABLE IF EXISTS `group_competition`;
DROP TABLE IF EXISTS `group_permission`;
DROP TABLE IF EXISTS `user_group`;
DROP TABLE IF EXISTS `finish`;
DROP TABLE IF EXISTS `match`;
DROP TABLE IF EXISTS `event`;
DROP TABLE IF EXISTS `group`;
DROP TABLE IF EXISTS `player_alias`;
DROP TABLE IF EXISTS `competition_player`;
DROP TABLE IF EXISTS `player`;
DROP TABLE IF EXISTS `usercredential`;
DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS `competition`;
DROP TABLE IF EXISTS `organisation`;
DROP TABLE IF EXISTS `permission`;

CREATE TABLE IF NOT EXISTS `organisation` (
   `organisation_id` integer NOT NULL PRIMARY KEY AUTOINCREMENT
,  `organisation_name` varchar(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS `competition` (
   `competition_id` integer NOT NULL PRIMARY KEY AUTOINCREMENT
,  `competition_name` varchar(50) NOT NULL
,  `competition_type` varchar(10) NOT NULL
,  `organisation_id` int(11) NOT NULL DEFAULT '0'
);
INSERT INTO `competition` (`competition_id`, `competition_name`, `competition_type`) VALUES
    (0, 'none', '');
CREATE TABLE IF NOT EXISTS `event` (
  `event_id` integer NOT NULL PRIMARY KEY AUTOINCREMENT
,  `competition_id` integer NOT NULL DEFAULT '0'
,  `event_type` varchar(15)  NULL
,  `event_name` varchar(50) NOT NULL
,  CONSTRAINT `fk_event_competition_id` FOREIGN KEY (`competition_id`) REFERENCES `competition` (`competition_id`)
);
INSERT INTO `event` (`event_id`, `competition_id`, `event_type`, `event_name`) VALUES
    (0, 0, 'none', 'default');
CREATE TABLE IF NOT EXISTS `group` (
  `group_id` integer NOT NULL PRIMARY KEY AUTOINCREMENT
,  `group_name` varchar(50) NOT NULL
);
INSERT INTO `group` (`group_id`, `group_name`) VALUES
    (0, 'site admins');
CREATE TABLE IF NOT EXISTS `player` (
  `player_id` integer NOT NULL PRIMARY KEY AUTOINCREMENT
,  `player_name` varchar(50) NOT NULL
,  `player_nickname` varchar(50) DEFAULT NULL
,  `player_callsigns` varchar(100) NOT NULL
,  `player_id_merged` integer NULL DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS `group_competition` (
  `group_id` integer NOT NULL
,  `competition_id` integer NOT NULL
,  PRIMARY KEY (`group_id`,`competition_id`)
,  CONSTRAINT `fk_gl_group_id` FOREIGN KEY (`group_id`) REFERENCES `group` (`group_id`)
,  CONSTRAINT `fk_gl_competition_id` FOREIGN KEY (`competition_id`) REFERENCES `competition` (`competition_id`)
);

CREATE TABLE IF NOT EXISTS `permission` (
  `permission_id` integer NOT NULL PRIMARY KEY AUTOINCREMENT
,  `permission_code` char(6) NOT NULL
,  `permission_name` varchar(50) NOT NULL
,  `permission_description` varchar(500) DEFAULT NULL
);
CREATE TABLE IF NOT EXISTS `group_permission` (
  `group_id` integer NOT NULL
,  `permission_id` integer NOT NULL
,  PRIMARY KEY (`group_id`,`permission_id`)
,  CONSTRAINT `fk_gp_group_id` FOREIGN KEY (`group_id`) REFERENCES `group` (`group_id`)
,  CONSTRAINT `fk_gp_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `permission` (`permission_id`)
);
CREATE TABLE `match` (
  `match_id` integer NOT NULL PRIMARY KEY AUTOINCREMENT
,  `event_id` integer NOT NULL DEFAULT '0'
,  `match_date` DATETIME NOT NULL
,  `match_date_round` VARCHAR(10) NULL DEFAULT NULL
,  `match_type` VARCHAR(10) NULL DEFAULT NULL
,  `player_1_id` integer NOT NULL
,  `player_1_id_orig` integer NOT NULL
,  `player_1_score` integer NOT NULL
,  `player_1_180s` integer NULL DEFAULT '0'
,  `player_1_lollies` integer NULL DEFAULT '0'
,  `player_2_id` integer NOT NULL
,  `player_2_id_orig` integer NOT NULL
,  `player_2_score` integer NOT NULL
,  `player_2_180s` integer NULL DEFAULT '0'
,  `player_2_lollies` integer NULL DEFAULT '0'
,  CONSTRAINT `fk_match_event_id` FOREIGN KEY (`event_id`) REFERENCES `event` (`event_id`)
,  CONSTRAINT `fk_match_player_1_id` FOREIGN KEY (`player_1_id`) REFERENCES `player` (`player_id`)
);
INSERT INTO `permission` (`permission_id`, `permission_code`, `permission_name`, `permission_description`) VALUES
    (1, 'ADDLEA', 'add competition', NULL),
    (2, 'ADDEVE', 'add event', 'add event to competition');
CREATE TABLE IF NOT EXISTS `player_alias` (
  `player_id` integer NOT NULL
,  `alias` varchar(50) NOT NULL
,  PRIMARY KEY (`player_id`,`alias`)
,  CONSTRAINT `fk_player_alias_player_id` FOREIGN KEY (`player_id`) REFERENCES `player` (`player_id`)
);
CREATE TABLE IF NOT EXISTS `user` (
  `user_id` integer NOT NULL PRIMARY KEY AUTOINCREMENT
,  `user_name` varchar(255) NOT NULL
,  `user_email` varchar(255) DEFAULT NULL
);
CREATE TABLE IF NOT EXISTS `usercredential` (
  `user_id` integer NOT NULL
,  `usercred_provider` varchar(10)  NOT NULL
,  `usercred_value` varchar(255) DEFAULT NULL
,  PRIMARY KEY (`user_id`,`usercred_provider`)
,  CONSTRAINT `fk_uc_userid` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
);
CREATE TABLE IF NOT EXISTS `user_group` (
  `user_id` integer NOT NULL
,  `group_id` integer NOT NULL
,  PRIMARY KEY (`user_id`,`group_id`)
,  CONSTRAINT `fk_ug_group_id` FOREIGN KEY (`group_id`) REFERENCES `group` (`group_id`)
,  CONSTRAINT `fk_ug_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
);
CREATE TABLE IF NOT EXISTS `finish` (
  `match_id` integer NOT NULL
,  `player_id` integer NOT NULL
,  `finish_score` integer NOT NULL
,  CONSTRAINT `fk_finish_match_id` FOREIGN KEY (`match_id`) REFERENCES `match` (`match_id`)
,  CONSTRAINT `fk_finish_player_id` FOREIGN KEY (`player_id`) REFERENCES `player` (`player_id`)
);
CREATE TABLE `competition_player` (
  `competition_id` integer NOT NULL
,  `player_id` integer NOT NULL
,  PRIMARY KEY (`competition_id`, `player_id`)
,  CONSTRAINT `fk_competition_player_competition_id` FOREIGN KEY (`competition_id`) REFERENCES `competition` (`competition_id`)
,  CONSTRAINT `fk_competition_player_player_id` FOREIGN KEY (`player_id`) REFERENCES `player` (`player_id`)
);
CREATE INDEX "idx_finish_fk_finish_match_id" ON "finish" (`match_id`);
CREATE INDEX "idx_finish_fk_finish_player_id" ON "finish" (`player_id`);
CREATE INDEX "idx_group_permission_fk_gp_permission_id" ON "group_permission" (`permission_id`);
CREATE INDEX "idx_user_group_fk_ug_group_id" ON "user_group" (`group_id`);
CREATE INDEX "idx_usercredential_FK_cred_userid" ON "usercredential" (`user_id`);
CREATE INDEX "idx_event_fk_event_competition_id" ON "event" (`competition_id`);
CREATE INDEX "idx_group_competition_fk_gl_competition_id" ON "group_competition" (`competition_id`);
