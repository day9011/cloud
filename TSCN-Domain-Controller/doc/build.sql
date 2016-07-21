CREATE TABLE `node` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(10) NOT NULL,
  `description` VARCHAR(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


CREATE TABLE `server` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `node_id` BIGINT(20) NOT NULL,
  `ip` varchar(15) NOT NULL,
  `status` VARCHAR(15) DEFAULT 'unknown',
  `user` VARCHAR(20) NOT NULL,
  `password` VARCHAR(20) NOT NULL ,
  `update_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY (`name`),
  UNIQUE KEY (`ip`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


CREATE TABLE `app` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `app_type_id` BIGINT(20) NOT NULL,
  `node_id` BIGINT(20) NOT NULL,
  `server_id` BIGINT(20) NOT NULL,
  `port` int(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;



CREATE TABLE `app_type` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `code_file` VARCHAR(50) DEFAULT NULL COMMENT 'Code file name, only to jar',
  `build_type` VARCHAR(20) DEFAULT NULL COMMENT 'git, http, local',
  `config_file` VARCHAR(200) DEFAULT NULL COMMENT 'use , for split',
  `update_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


CREATE TABLE `app_env` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `app_id` BIGINT(20) NOT NULL,
  `pkg_id` int(10) NOT NULL,
  `update_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


CREATE TABLE `vcs` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `node_id` BIGINT(20) NOT NULL,
  `app_type_id` BIGINT(20) NOT NULL,
  `branch` VARCHAR (20) NOT NULL,
  `latest_version` VARCHAR (50) NOT NULL,
  `download_url` VARCHAR(200) NOT NULL,
  `exclude` VARCHAR(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY (`node_id`, `app_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


CREATE TABLE `nexus_history` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `app_type_id` BIGINT(20) NOT NULL,
  `branch` VARCHAR(20) NOT NULL,
  `version` VARCHAR(50) DEFAULT NULL,
  `config_changed` INT(1) DEFAULT 0,
  `commit_time` DATETIME,
  `commiter` VARCHAR(30),
  `commit` VARCHAR(500),
  PRIMARY KEY (`id`),
  UNIQUE KEY (`app_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


CREATE TABLE `task_log` (
  `id` VARCHAR(36) NOT NULL,
  `task_name` VARCHAR(20) NOT NULL,
  `retry_from` VARCHAR(36) NOT NULL COMMENT 'retry a failed task',
  `step` INT(2) NOT NULL DEFAULT 0,
  `status` INT(1) NOT NULL COMMENT '0-new, 1-success, 2-failed',
  `comment` VARCHAR(500) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY (`id`, `step`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `task_log` (
  `id` VARCHAR(36) NOT NULL,
  `task_name` VARCHAR(20) NOT NULL,
  `retry_from` VARCHAR(36) NOT NULL COMMENT 'retry a failed task',
  `status` VARCHAR(10) NOT NULL COMMENT 'new, running, success, failed',
  `args` VARCHAR(1000) DEFAULT NULL,
  `apply` varchar(20) NOT NULL DEFAULT 'ops',
  `comment` VARCHAR(500) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `action_log` (
  `id` VARCHAR(40) NOT NULL,
  `task_id` VARCHAR(20) NOT NULL,
  `target` VARCHAR(50) NOT NULL,
  `status` TINYINT(1) NOT NULL COMMENT '0-success',
  `comment` VARCHAR(500) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;