-- MySQL dump 10.13  Distrib 5.7.12, for osx10.11 (x86_64)
--
-- Host: localhost    Database: tops
-- ------------------------------------------------------
-- Server version	5.7.12

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `common_role`
--

DROP TABLE IF EXISTS `common_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `common_role` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `domain_id` int(20) NOT NULL,
  `cluster_id` int(20) NOT NULL,
  `role_id` int(20) NOT NULL,
  `role_seq` int(20) NOT NULL,
  `is_enable` int(1) DEFAULT '1',
  `cpu` int(2) NOT NULL,
  `mem` int(2) NOT NULL,
  `disk` int(4) DEFAULT NULL,
  `port` int(4) NOT NULL,
  `private_ip` varchar(15) NOT NULL,
  `vip_ip` varchar(15) DEFAULT NULL,
  `public_ip` varchar(15) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `db_name` varchar(50) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `domain_id` (`domain_id`,`cluster_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `common_role`
--

LOCK TABLES `common_role` WRITE;
/*!40000 ALTER TABLE `common_role` DISABLE KEYS */;
/*!40000 ALTER TABLE `common_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `domain`
--

DROP TABLE IF EXISTS `domain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `domain` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `detail` varchar(20) NOT NULL,
  `project_id` int(20) NOT NULL,
  `url` varchar(50) NOT NULL,
  `external_lb` varchar(15) DEFAULT NULL,
  `internal_lv` varchar(15) DEFAULT NULL,
  `oss` varchar(50) DEFAULT NULL,
  `dns` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `detail` (`detail`)
) ENGINE=InnoDB AUTO_INCREMENT=200002 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `domain`
--

LOCK TABLES `domain` WRITE;
/*!40000 ALTER TABLE `domain` DISABLE KEYS */;
INSERT INTO `domain` VALUES (200001,'local','liming\'pc',100001,'http://127.0.0.1:9999',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `domain` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `domain_env`
--

DROP TABLE IF EXISTS `domain_env`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `domain_env` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `domain_id` int(20) NOT NULL,
  `key` varchar(50) NOT NULL,
  `value` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `domain_id` (`domain_id`,`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `domain_env`
--

LOCK TABLES `domain_env` WRITE;
/*!40000 ALTER TABLE `domain_env` DISABLE KEYS */;
/*!40000 ALTER TABLE `domain_env` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project`
--

DROP TABLE IF EXISTS `project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `project` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `detail` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `detail` (`detail`)
) ENGINE=InnoDB AUTO_INCREMENT=100002 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project`
--

LOCK TABLES `project` WRITE;
/*!40000 ALTER TABLE `project` DISABLE KEYS */;
INSERT INTO `project` VALUES (100001,'e-invoice','e-invoice project');
/*!40000 ALTER TABLE `project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_role`
--

DROP TABLE IF EXISTS `project_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `project_role` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `project_id` int(20) NOT NULL,
  `role_id` int(20) NOT NULL,
  `cpu` int(2) NOT NULL,
  `mem` int(2) NOT NULL,
  `disk` int(4) DEFAULT NULL,
  `domain_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_id` (`project_id`,`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_role`
--

LOCK TABLES `project_role` WRITE;
/*!40000 ALTER TABLE `project_role` DISABLE KEYS */;
INSERT INTO `project_role` VALUES (1,100001,300001,0,1,10,200001),(2,100001,300002,0,2,10,200001),(3,100001,400001,0,10,40,200001);
/*!40000 ALTER TABLE `project_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resource`
--

DROP TABLE IF EXISTS `resource`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `resource` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `instance_id` varchar(100) NOT NULL,
  `type` varchar(100) NOT NULL,
  `domain_id` int(20) NOT NULL,
  `private_ip` varchar(15) NOT NULL,
  `public_ip` varchar(15) DEFAULT NULL,
  `port` int(4) NOT NULL,
  `status` varchar(10) NOT NULL COMMENT 'used,deleted',
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `domain_id` (`domain_id`,`instance_id`),
  UNIQUE KEY `domain_id_2` (`domain_id`,`private_ip`,`port`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resource`
--

LOCK TABLES `resource` WRITE;
/*!40000 ALTER TABLE `resource` DISABLE KEYS */;
INSERT INTO `resource` VALUES (1,'aaaaaaaa','fs',200001,'172.16.30.180',NULL,5001,'used','2016-01-01 00:00:00'),(2,'aaaaaaab','fs',200001,'172.16.30.180',NULL,5002,'uesd','2016-01-01 00:00:00'),(3,'aaaaaaac','fs',200001,'172.16.30.180',NULL,5003,'used','2016-01-01 00:00:00');
/*!40000 ALTER TABLE `resource` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `detail` varchar(20) NOT NULL,
  `type` varchar(10) NOT NULL DEFAULT 'ts' COMMENT 'ts or common',
  `port` varchar(200) DEFAULT NULL,
  `config_file` varchar(500) DEFAULT NULL COMMENT 'config.js;config/config.js',
  `code_file` varchar(50) DEFAULT NULL,
  `build_type` varchar(10) NOT NULL COMMENT 'file or tar',
  `project_id` int(20) NOT NULL,
  `domain_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_id` (`project_id`,`detail`),
  UNIQUE KEY `name` (`project_id`,`domain_id`,`name`)
) ENGINE=InnoDB AUTO_INCREMENT=400002 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (300001,'my-upload','my-upload','ts','80,8888',NULL,'upload.sh','file',100001,200001),(300002,'my-api','my-api','ts','80,8888',NULL,'api.sh','file',100001,200001),(400001,'document-api','for a test','ts',NULL,NULL,'api.sh','file',100001,200001);
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ts_role`
--

DROP TABLE IF EXISTS `ts_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ts_role` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `project_id` int(20) NOT NULL,
  `domain_id` int(20) NOT NULL,
  `role_id` int(20) NOT NULL,
  `role_seq` int(20) NOT NULL,
  `resource_id` varchar(100) NOT NULL,
  `is_enable` int(1) DEFAULT '1',
  `tag` varchar(50) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `branch` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `domain_id` (`domain_id`,`resource_id`),
  UNIQUE KEY `domain_id_2` (`domain_id`,`project_id`,`role_id`,`role_seq`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ts_role`
--

LOCK TABLES `ts_role` WRITE;
/*!40000 ALTER TABLE `ts_role` DISABLE KEYS */;
INSERT INTO `ts_role` VALUES (2,'document-api01.local.e-invoice.com',100001,200001,400001,1,'ed5df0687c96451fbfbec62820306a0b026aebf310f1010ebb5d59d1fcd8af75',1,'v1.0.2','2016-07-21 10:59:33','master'),(3,'document-api02.local.e-invoice.com',100001,200001,400001,2,'04a4ee40248e157e6fc06af5f3705b579f04c1ab870614314b9b02b4f93e6421',1,'v1.0.3','2016-07-21 10:59:48','master');
/*!40000 ALTER TABLE `ts_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `var_table`
--

DROP TABLE IF EXISTS `var_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `var_table` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `project_id` bigint(20) NOT NULL,
  `domain_id` bigint(20) NOT NULL,
  `role_id` bigint(20) NOT NULL,
  `key_name` varchar(100) DEFAULT NULL,
  `key_value` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `p_d_r_n` (`project_id`,`domain_id`,`role_id`,`key_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `var_table`
--

LOCK TABLES `var_table` WRITE;
/*!40000 ALTER TABLE `var_table` DISABLE KEYS */;
INSERT INTO `var_table` VALUES (1,100001,200001,400001,'name','day9011'),(3,100001,200001,400001,'age','25');
/*!40000 ALTER TABLE `var_table` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-07-21 16:11:52
