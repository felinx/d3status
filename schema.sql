
create database if not exists `d3status`;

USE `d3status`;

DROP TABLE IF EXISTS `status`;
CREATE TABLE `status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category` varchar(45) NOT NULL,
  `service` varchar(45) NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '1 - up, 0 -down',
  `updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `subscribers`;
CREATE TABLE `subscribers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` varchar(100) NOT NULL,
  `categorys` varchar(45) NOT NULL COMMENT '''Americas,Europe,Asia''',
  `locale` enum('en','zh_CN','zh_TW') NOT NULL DEFAULT 'en',
  `status` enum('on','off') NOT NULL DEFAULT 'on',
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_UNIQUE` (`token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;