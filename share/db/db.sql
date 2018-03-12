USE `dartsense_test`;

CREATE TABLE IF NOT EXISTS `league` (
  `league_id` int(11) NOT NULL AUTO_INCREMENT,
  `league_name` varchar(50) NOT NULL,
  PRIMARY KEY (`league_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

INSERT INTO `league` (`league_id`, `league_name`) VALUES
    (0, 'none');

CREATE TABLE IF NOT EXISTS `event` (
  `event_id` int(11) NOT NULL AUTO_INCREMENT,
  `league_id` int(11) NOT NULL DEFAULT '0',
  `event_type` enum('tournament','league','none') NOT NULL,
  `event_name` varchar(50) NOT NULL,
  PRIMARY KEY (`event_id`),
  KEY `fk_event_league_id` (`league_id`),
  CONSTRAINT `fk_event_league_id` FOREIGN KEY (`league_id`) REFERENCES `league` (`league_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `event` (`event_id`, `league_id`, `event_type`, `event_name`) VALUES
    (0, 0, 'none', 'default');

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

CREATE TABLE IF NOT EXISTS `group_league` (
  `group_id` int(11) NOT NULL,
  `league_id` int(11) NOT NULL,
  PRIMARY KEY (`group_id`,`league_id`),
  KEY `fk_gl_league_id` (`league_id`),
  CONSTRAINT `fk_gl_group_id` FOREIGN KEY (`group_id`) REFERENCES `group` (`group_id`),
  CONSTRAINT `fk_gl_league_id` FOREIGN KEY (`league_id`) REFERENCES `league` (`league_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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

CREATE TABLE IF NOT EXISTS `permission` (
  `permission_id` int(11) NOT NULL AUTO_INCREMENT,
  `permission_code` char(6) NOT NULL,
  `permission_name` varchar(50) NOT NULL,
  `permission_description` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`permission_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

INSERT INTO `permission` (`permission_id`, `permission_code`, `permission_name`, `permission_description`) VALUES
    (1, 'ADDLEA', 'add league', NULL),
    (2, 'ADDEVE', 'add event', 'add event to league');

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

