USE `dartsense_test`;
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
DROP TABLE IF EXISTS `permission`;


CREATE TABLE IF NOT EXISTS `competition` (
  `competition_id` int(11) NOT NULL AUTO_INCREMENT,
  `competition_name` varchar(50) NOT NULL,
  `competition_type` enum('league','tournament') NOT NULL DEFAULT 'competition',
  PRIMARY KEY (`competition_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

INSERT INTO `competition` (`competition_id`, `competition_name`) VALUES
    (0, 'none');
UPDATE `competition` set competition_id=0;

CREATE TABLE IF NOT EXISTS `event` (
  `event_id` int(11) NOT NULL AUTO_INCREMENT,
  `competition_id` int(11) NOT NULL DEFAULT '0',
  `event_type` enum('none','league_round','league_adjust','poule','knockout') NOT NULL,
  `event_name` varchar(50) NOT NULL,
  PRIMARY KEY (`event_id`),
  KEY `fk_event_competition_id` (`competition_id`),
  CONSTRAINT `fk_event_competition_id` FOREIGN KEY (`competition_id`) REFERENCES `competition` (`competition_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `event` (`event_id`, `competition_id`, `event_type`, `event_name`) VALUES
    (0, 0, 'none', 'default');
UPDATE `event` set event_id=0;

CREATE TABLE IF NOT EXISTS `group` (
  `group_id` int(11) NOT NULL AUTO_INCREMENT,
  `group_name` varchar(50) NOT NULL,
  PRIMARY KEY (`group_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

INSERT INTO `group` (`group_id`, `group_name`) VALUES
    (0, 'site admins');

CREATE TABLE IF NOT EXISTS `player` (
  `player_id` int(11) NOT NULL AUTO_INCREMENT,
  `player_name` varchar(50) NOT NULL,
  `player_nickname` varchar(50) DEFAULT NULL,
  `player_callsigns` varchar(100) NOT NULL,
  PRIMARY KEY (`player_id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `group_competition` (
  `group_id` int(11) NOT NULL,
  `competition_id` int(11) NOT NULL,
  PRIMARY KEY (`group_id`,`competition_id`),
  KEY `fk_gl_competition_id` (`competition_id`),
  CONSTRAINT `fk_gl_group_id` FOREIGN KEY (`group_id`) REFERENCES `group` (`group_id`),
  CONSTRAINT `fk_gl_competition_id` FOREIGN KEY (`competition_id`) REFERENCES `competition` (`competition_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `permission` (
  `permission_id` int(11) NOT NULL AUTO_INCREMENT,
  `permission_code` char(6) NOT NULL,
  `permission_name` varchar(50) NOT NULL,
  `permission_description` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`permission_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `group_permission` (
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`group_id`,`permission_id`),
  KEY `fk_gp_permission_id` (`permission_id`),
  CONSTRAINT `fk_gp_group_id` FOREIGN KEY (`group_id`) REFERENCES `group` (`group_id`),
  CONSTRAINT `fk_gp_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `permission` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `match` (
  `match_id` int(11) NOT NULL AUTO_INCREMENT,
  `event_id` int(11) NOT NULL DEFAULT '0',
  `match_date` date NOT NULL,
  `match_date_round` varchar(10) DEFAULT NULL,
  `match_type` varchar(10) DEFAULT NULL,
  `player_1_id` int(11) NOT NULL,
  `player_1_score` tinyint(4) NOT NULL,
  `player_1_180s` tinyint(4) DEFAULT '0',
  `player_1_lollies` tinyint(4) DEFAULT '0',
  `player_2_id` int(11) NOT NULL,
  `player_2_score` tinyint(4) NOT NULL,
  `player_2_180s` tinyint(4) DEFAULT '0',
  `player_2_lollies` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`match_id`),
  KEY `fk_match_player_1_id` (`player_1_id`),
  KEY `fk_match_player_2_id` (`player_2_id`),
  KEY `fk_match_event_id` (`event_id`),
  CONSTRAINT `fk_match_event_id` FOREIGN KEY (`event_id`) REFERENCES `event` (`event_id`),
  CONSTRAINT `fk_match_player_1_id` FOREIGN KEY (`player_1_id`) REFERENCES `player` (`player_id`),
  CONSTRAINT `fk_match_player_2_id` FOREIGN KEY (`player_2_id`) REFERENCES `player` (`player_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `permission` (`permission_id`, `permission_code`, `permission_name`, `permission_description`) VALUES
    (1, 'ADDLEA', 'add competition', NULL),
    (2, 'ADDEVE', 'add event', 'add event to competition');

CREATE TABLE IF NOT EXISTS `player_alias` (
  `player_id` int(11) NOT NULL,
  `alias` varchar(50) NOT NULL,
  PRIMARY KEY (`player_id`,`alias`),
  CONSTRAINT `fk_player_alias_player_id` FOREIGN KEY (`player_id`) REFERENCES `player` (`player_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `user` (
  `user_id` int(10) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(255) NOT NULL,
  `user_email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `usercredential` (
  `user_id` int(10) NOT NULL,
  `usercred_provider` enum('google','facebook') NOT NULL,
  `usercred_value` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`,`usercred_provider`),
  KEY `FK_cred_userid` (`user_id`),
  CONSTRAINT `fk_uc_userid` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `user_group` (
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`user_id`,`group_id`),
  KEY `fk_ug_group_id` (`group_id`),
  CONSTRAINT `fk_ug_group_id` FOREIGN KEY (`group_id`) REFERENCES `group` (`group_id`),
  CONSTRAINT `fk_ug_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `finish` (
  `match_id` int(11) NOT NULL,
  `player_id` int(11) NOT NULL,
  `finish_score` smallint(6) NOT NULL,
  KEY `fk_finish_match_id` (`match_id`),
  KEY `fk_finish_player_id` (`player_id`),
  CONSTRAINT `fk_finish_match_id` FOREIGN KEY (`match_id`) REFERENCES `match` (`match_id`),
  CONSTRAINT `fk_finish_player_id` FOREIGN KEY (`player_id`) REFERENCES `player` (`player_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `competition_player` (
  `competition_id` INT(11) NOT NULL,
  `player_id` INT(11) NOT NULL,
  PRIMARY KEY (`competition_id`, `player_id`),
  INDEX `fk_competition_player_player_id` (`player_id`),
  CONSTRAINT `fk_competition_player_competition_id` FOREIGN KEY (`competition_id`) REFERENCES `competition` (`competition_id`),
  CONSTRAINT `fk_competition_player_player_id` FOREIGN KEY (`player_id`) REFERENCES `player` (`player_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;