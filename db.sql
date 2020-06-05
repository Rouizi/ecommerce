-- MySQL dump 10.13  Distrib 5.7.30, for Linux (x86_64)
--
-- Host: localhost    Database: ecommerce
-- ------------------------------------------------------
-- Server version	5.7.30-0ubuntu0.18.04.1

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
-- Table structure for table `account_emailaddress`
--

DROP TABLE IF EXISTS `account_emailaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_emailaddress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(254) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `primary` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `account_emailaddress_user_id_2c513194_fk_users_user_id` (`user_id`),
  CONSTRAINT `account_emailaddress_user_id_2c513194_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_emailaddress`
--

LOCK TABLES `account_emailaddress` WRITE;
/*!40000 ALTER TABLE `account_emailaddress` DISABLE KEYS */;
INSERT INTO `account_emailaddress` VALUES (5,'cinorouizi@sffe.fr',0,0,1),(6,'cinorouizi@gmail.com',0,0,1),(7,'cinorouizi@hotmail.com',0,1,3);
/*!40000 ALTER TABLE `account_emailaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_emailconfirmation`
--

DROP TABLE IF EXISTS `account_emailconfirmation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_emailconfirmation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `sent` datetime(6) DEFAULT NULL,
  `key` varchar(64) NOT NULL,
  `email_address_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`),
  KEY `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` (`email_address_id`),
  CONSTRAINT `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` FOREIGN KEY (`email_address_id`) REFERENCES `account_emailaddress` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_emailconfirmation`
--

LOCK TABLES `account_emailconfirmation` WRITE;
/*!40000 ALTER TABLE `account_emailconfirmation` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_emailconfirmation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add site',6,'add_site'),(22,'Can change site',6,'change_site'),(23,'Can delete site',6,'delete_site'),(24,'Can view site',6,'view_site'),(25,'Can add email address',7,'add_emailaddress'),(26,'Can change email address',7,'change_emailaddress'),(27,'Can delete email address',7,'delete_emailaddress'),(28,'Can view email address',7,'view_emailaddress'),(29,'Can add email confirmation',8,'add_emailconfirmation'),(30,'Can change email confirmation',8,'change_emailconfirmation'),(31,'Can delete email confirmation',8,'delete_emailconfirmation'),(32,'Can view email confirmation',8,'view_emailconfirmation'),(33,'Can add social account',9,'add_socialaccount'),(34,'Can change social account',9,'change_socialaccount'),(35,'Can delete social account',9,'delete_socialaccount'),(36,'Can view social account',9,'view_socialaccount'),(37,'Can add social application',10,'add_socialapp'),(38,'Can change social application',10,'change_socialapp'),(39,'Can delete social application',10,'delete_socialapp'),(40,'Can view social application',10,'view_socialapp'),(41,'Can add social application token',11,'add_socialtoken'),(42,'Can change social application token',11,'change_socialtoken'),(43,'Can delete social application token',11,'delete_socialtoken'),(44,'Can view social application token',11,'view_socialtoken'),(45,'Can add user',12,'add_user'),(46,'Can change user',12,'change_user'),(47,'Can delete user',12,'delete_user'),(48,'Can view user',12,'view_user'),(49,'Can add item',13,'add_item'),(50,'Can change item',13,'change_item'),(51,'Can delete item',13,'delete_item'),(52,'Can view item',13,'view_item'),(53,'Can add order',14,'add_order'),(54,'Can change order',14,'change_order'),(55,'Can delete order',14,'delete_order'),(56,'Can view order',14,'view_order'),(57,'Can add order item',15,'add_orderitem'),(58,'Can change order item',15,'change_orderitem'),(59,'Can delete order item',15,'delete_orderitem'),(60,'Can view order item',15,'view_orderitem'),(61,'Can add size',16,'add_size'),(62,'Can change size',16,'change_size'),(63,'Can delete size',16,'delete_size'),(64,'Can view size',16,'view_size'),(65,'Can add price item',17,'add_priceitem'),(66,'Can change price item',17,'change_priceitem'),(67,'Can delete price item',17,'delete_priceitem'),(68,'Can view price item',17,'view_priceitem'),(69,'Can add stock item',18,'add_stockitem'),(70,'Can change stock item',18,'change_stockitem'),(71,'Can delete stock item',18,'delete_stockitem'),(72,'Can view stock item',18,'view_stockitem'),(73,'Can add address',19,'add_address'),(74,'Can change address',19,'change_address'),(75,'Can delete address',19,'delete_address'),(76,'Can view address',19,'view_address'),(77,'Can add stripe payment',20,'add_stripepayment'),(78,'Can change stripe payment',20,'change_stripepayment'),(79,'Can delete stripe payment',20,'delete_stripepayment'),(80,'Can view stripe payment',20,'view_stripepayment');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_item`
--

DROP TABLE IF EXISTS `core_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `category` varchar(2) NOT NULL,
  `label` varchar(10) DEFAULT NULL,
  `color_label` varchar(15) DEFAULT NULL,
  `price` decimal(6,2) NOT NULL,
  `image1` varchar(100) NOT NULL,
  `image2` varchar(100) DEFAULT NULL,
  `slug` varchar(100) NOT NULL,
  `description` longtext,
  `discount_price` decimal(6,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `core_item_slug_07f502d0` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_item`
--

LOCK TABLES `core_item` WRITE;
/*!40000 ALTER TABLE `core_item` DISABLE KEYS */;
INSERT INTO `core_item` VALUES (6,'Brushed Heather','S','BS','primary-color',99.00,'clothes/jack_heather_grey_001.jpg','clothes/jack_heather_grey_009.jpg','brushed-heather','Lorem ipsum dolor sit amet consectetur adipisicing elit. Numquam, sapiente illo. Sit error voluptas repellat rerum quidem, soluta enim perferendis voluptates laboriosam. Distinctio, officia quis dolore quos sapiente tempore alias.',88.00),(7,'Vintage Navy','S',NULL,NULL,73.50,'clothes/vintage_001.jpg','clothes/vintage_010.jpg','vintage-navy','Lorem ipsum dolor sit amet consectetur adipisicing elit. Numquam, sapiente illo. Sit error voluptas repellat rerum quidem, soluta enim perferendis voluptates laboriosam. Distinctio, officia quis dolore quos sapiente tempore alias.',NULL),(9,'The Jack','S','BS','primary-color',100.00,'clothes/jack_000.jpg','clothes/jack_009.jpg','jack','Lorem ipsum dolor sit amet consectetur adipisicing elit. Numquam, sapiente illo. Sit error voluptas repellat rerum quidem, soluta enim perferendis voluptates laboriosam. Distinctio, officia quis dolore quos sapiente tempore alias.',NULL),(10,'The Long Haul Jacket','D',NULL,NULL,188.00,'clothes/jacket_lifstyle_01.jpg','clothes/jacket_lifstyle_02.jpg','long-haul-jacket','Lorem ipsum dolor sit amet consectetur adipisicing elit. Numquam, sapiente illo. Sit error voluptas repellat rerum quidem, soluta enim perferendis voluptates laboriosam. Distinctio, officia quis dolore quos sapiente tempore alias.',NULL),(11,'Sun Bleached','D',NULL,NULL,68.60,'clothes/sun_bleached_2.jpg','clothes/sun_bleached_1..jpg','sun-bleached','Lorem ipsum dolor sit amet consectetur adipisicing elit. Numquam, sapiente illo. Sit error voluptas repellat rerum quidem, soluta enim perferendis voluptates laboriosam. Distinctio, officia quis dolore quos sapiente tempore alias.',NULL),(14,'Moto Jacket','OW',NULL,NULL,220.00,'clothes/moto_jacket_1.jpg','clothes/moto_jacket_2.jpg','moto-jacket','Lorem ipsum dolor sit amet consectetur adipisicing elit. Numquam, sapiente illo. Sit error voluptas repellat rerum quidem, soluta enim perferendis voluptates laboriosam. Distinctio, officia quis dolore quos sapiente tempore alias.',NULL),(15,'Tobacco','OW',NULL,NULL,150.99,'clothes/tobacco_1.jpg','clothes/tobacco_2.jpg','tobacco','Lorem ipsum dolor sit amet consectetur adipisicing elit. Numquam, sapiente illo. Sit error voluptas repellat rerum quidem, soluta enim perferendis voluptates laboriosam. Distinctio, officia quis dolore quos sapiente tempore alias.',NULL),(16,'Winslow Jacket','OW','N','danger-color',235.49,'clothes/winslow_jacket_1.jpg','clothes/Winslow_jacket_2.jpg','winslow-jacket','Lorem ipsum dolor sit amet consectetur adipisicing elit. Numquam, sapiente illo. Sit error voluptas repellat rerum quidem, soluta enim perferendis voluptates laboriosam. Distinctio, officia quis dolore quos sapiente tempore alias.',NULL),(17,'Port Jacket','OW',NULL,NULL,188.00,'clothes/port_jacket_1.jpg','clothes/port_jacket_2.jpg','port-jacket','Lorem ipsum dolor sit amet consectetur adipisicing elit. Numquam, sapiente illo. Sit error voluptas repellat rerum quidem, soluta enim perferendis voluptates laboriosam. Distinctio, officia quis dolore quos sapiente tempore alias.',NULL),(18,'Hemp Stripe','OW',NULL,NULL,94.40,'clothes/hemp_stripe_1.jpg','clothes/hemp_stripe_2.jpg','hemp-stripe','Lorem ipsum dolor sit amet consectetur adipisicing elit. Numquam, sapiente illo. Sit error voluptas repellat rerum quidem, soluta enim perferendis voluptates laboriosam. Distinctio, officia quis dolore quos sapiente tempore alias.',84.99),(19,'Hemp Donegal','OW','BS','primary-color',118.00,'clothes/hemp_donegal_1.jpg','clothes/hemp_donegal_2.jpg','hemp-donegal','Lorem ipsum dolor sit amet consectetur adipisicing elit. Numquam, sapiente illo. Sit error voluptas repellat rerum quidem, soluta enim perferendis voluptates laboriosam. Distinctio, officia quis dolore quos sapiente tempore alias.',NULL);
/*!40000 ALTER TABLE `core_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_order`
--

DROP TABLE IF EXISTS `core_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ordered_date` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  `ordered` tinyint(1) NOT NULL,
  `address_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `core_order_user_id_b03bbffd_fk_users_user_id` (`user_id`),
  KEY `core_order_address_id_caf8cd86_fk_users_address_id` (`address_id`),
  CONSTRAINT `core_order_address_id_caf8cd86_fk_users_address_id` FOREIGN KEY (`address_id`) REFERENCES `users_address` (`id`),
  CONSTRAINT `core_order_user_id_b03bbffd_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_order`
--

LOCK TABLES `core_order` WRITE;
/*!40000 ALTER TABLE `core_order` DISABLE KEYS */;
INSERT INTO `core_order` VALUES (16,'2020-05-14 00:10:34.227353',2,0,NULL),(24,'2020-05-14 22:51:46.022199',1,0,NULL),(33,'2020-05-24 23:58:35.649511',1,0,NULL);
/*!40000 ALTER TABLE `core_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_orderitem`
--

DROP TABLE IF EXISTS `core_orderitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_orderitem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `quantity` int(10) unsigned NOT NULL,
  `item_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `ordered` tinyint(1) NOT NULL,
  `size_id` int(11) DEFAULT NULL,
  `order_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `core_orderitem_item_id_3b7d0c2e_fk_core_item_id` (`item_id`),
  KEY `core_orderitem_user_id_323fe695_fk_users_user_id` (`user_id`),
  KEY `core_orderitem_size_id_5f905dc8_fk_core_size_id` (`size_id`),
  KEY `core_orderitem_order_id_30929c10_fk_core_order_id` (`order_id`),
  CONSTRAINT `core_orderitem_item_id_3b7d0c2e_fk_core_item_id` FOREIGN KEY (`item_id`) REFERENCES `core_item` (`id`),
  CONSTRAINT `core_orderitem_order_id_30929c10_fk_core_order_id` FOREIGN KEY (`order_id`) REFERENCES `core_order` (`id`),
  CONSTRAINT `core_orderitem_size_id_5f905dc8_fk_core_size_id` FOREIGN KEY (`size_id`) REFERENCES `core_size` (`id`),
  CONSTRAINT `core_orderitem_user_id_323fe695_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_orderitem`
--

LOCK TABLES `core_orderitem` WRITE;
/*!40000 ALTER TABLE `core_orderitem` DISABLE KEYS */;
INSERT INTO `core_orderitem` VALUES (42,1,6,2,0,1,16),(55,5,6,1,0,1,24),(56,1,6,1,0,3,24),(57,1,9,1,0,2,24);
/*!40000 ALTER TABLE `core_orderitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_size`
--

DROP TABLE IF EXISTS `core_size`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_size` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_size`
--

LOCK TABLES `core_size` WRITE;
/*!40000 ALTER TABLE `core_size` DISABLE KEYS */;
INSERT INTO `core_size` VALUES (1,'S'),(2,'M'),(3,'L');
/*!40000 ALTER TABLE `core_size` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_stockitem`
--

DROP TABLE IF EXISTS `core_stockitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_stockitem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stock` int(10) unsigned NOT NULL,
  `item_id` int(11) NOT NULL,
  `size_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `core_stockitem_item_id_aa6e9c62_fk_core_item_id` (`item_id`),
  KEY `core_stockitem_size_id_b4abf702_fk_core_size_id` (`size_id`),
  CONSTRAINT `core_stockitem_item_id_aa6e9c62_fk_core_item_id` FOREIGN KEY (`item_id`) REFERENCES `core_item` (`id`),
  CONSTRAINT `core_stockitem_size_id_b4abf702_fk_core_size_id` FOREIGN KEY (`size_id`) REFERENCES `core_size` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_stockitem`
--

LOCK TABLES `core_stockitem` WRITE;
/*!40000 ALTER TABLE `core_stockitem` DISABLE KEYS */;
INSERT INTO `core_stockitem` VALUES (1,140,6,1),(2,87,6,2),(3,102,6,3),(4,8,7,1),(5,0,7,2),(6,0,7,3),(7,4,9,1),(8,12,9,2),(9,8,9,3),(10,10,10,1),(11,15,10,2),(12,8,10,3),(13,10,11,1),(14,15,11,2),(15,9,11,3),(19,10,14,1),(20,15,14,2),(21,9,14,3),(22,10,15,1),(23,15,15,2),(24,9,15,3),(25,20,16,1),(26,20,16,2),(27,20,16,3),(28,0,17,1),(29,15,17,2),(30,9,17,3),(31,10,18,1),(32,15,18,2),(33,9,18,3),(34,10,19,1),(35,15,19,2),(36,9,19,3);
/*!40000 ALTER TABLE `core_stockitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_users_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2020-04-23 23:01:48.920752','1','Brushed Heather',1,'[{\"added\": {}}]',13,1),(2,'2020-04-25 18:56:06.752271','1','Brushed Heather',2,'[{\"changed\": {\"fields\": [\"Label\"]}}]',13,1),(3,'2020-04-26 13:01:39.941523','1','Brushed Heather',2,'[{\"changed\": {\"fields\": [\"Color\"]}}]',13,1),(4,'2020-04-26 13:05:27.767494','1','Brushed Heather',2,'[{\"changed\": {\"fields\": [\"Color\"]}}]',13,1),(5,'2020-04-26 13:05:43.811443','1','Brushed Heather',2,'[{\"changed\": {\"fields\": [\"Color\"]}}]',13,1),(6,'2020-04-28 12:28:58.265527','6','Brushed Heather',2,'[{\"changed\": {\"fields\": [\"Label\", \"Price\"]}}]',13,1),(7,'2020-04-28 12:29:21.713840','6','Brushed Heather',2,'[{\"changed\": {\"fields\": [\"Color label\"]}}]',13,1),(8,'2020-04-28 12:39:08.009056','7','Vintage Navy',1,'[{\"added\": {}}]',13,1),(9,'2020-04-28 12:54:08.322307','8','The Jack',1,'[{\"added\": {}}]',13,1),(10,'2020-04-28 13:35:03.817212','8','The Jack',3,'',13,1),(11,'2020-04-28 13:36:40.118926','7','Vintage Navy',2,'[{\"changed\": {\"fields\": [\"Image1\", \"Image2\"]}}]',13,1),(12,'2020-04-28 13:36:53.149368','5','Brushed Heather',3,'',13,1),(13,'2020-04-28 13:36:53.280591','4','Brushed Heather',3,'',13,1),(14,'2020-04-28 13:36:53.330322','3','Brushed Heather',3,'',13,1),(15,'2020-04-28 13:36:53.390308','2','Brushed Heather',3,'',13,1),(16,'2020-04-28 13:36:53.538443','1','Brushed Heather',3,'',13,1),(17,'2020-04-28 13:37:08.625384','6','Brushed Heather',2,'[{\"changed\": {\"fields\": [\"Image1\", \"Image2\"]}}]',13,1),(18,'2020-04-28 13:38:29.368162','9','The Jack',1,'[{\"added\": {}}]',13,1),(19,'2020-04-28 13:45:59.037681','10','The Long Haul Jacket',1,'[{\"added\": {}}]',13,1),(20,'2020-04-28 13:48:06.970252','11','Sun Bleached',1,'[{\"added\": {}}]',13,1),(21,'2020-04-28 13:51:28.106444','12','The Cash Shirt',1,'[{\"added\": {}}]',13,1),(22,'2020-04-28 13:51:28.137675','13','The Cash Shirt',1,'[{\"added\": {}}]',13,1),(23,'2020-04-28 13:52:38.512650','13','The Cash Shirt',2,'[{\"changed\": {\"fields\": [\"Category\"]}}]',13,1),(24,'2020-04-28 13:52:55.431733','12','The Cash Shirt',3,'',13,1),(25,'2020-04-28 13:53:34.665434','10','The Long Haul Jacket',2,'[{\"changed\": {\"fields\": [\"Category\"]}}]',13,1),(26,'2020-04-28 13:54:02.926758','11','Sun Bleached',2,'[{\"changed\": {\"fields\": [\"Category\"]}}]',13,1),(27,'2020-04-28 14:16:35.798680','14','Moto Jacket',1,'[{\"added\": {}}]',13,1),(28,'2020-04-28 14:18:57.636221','15','Tobacco',1,'[{\"added\": {}}]',13,1),(29,'2020-04-28 14:21:32.205969','16','Winslow Jacket',1,'[{\"added\": {}}]',13,1),(30,'2020-04-28 14:27:24.016400','17','Port Jacket',1,'[{\"added\": {}}]',13,1),(31,'2020-04-28 14:31:04.546092','18','Hemp Stripe',1,'[{\"added\": {}}]',13,1),(32,'2020-04-28 14:33:17.017469','19','Hemp Donegal',1,'[{\"added\": {}}]',13,1),(33,'2020-04-28 14:33:52.737190','19','Hemp Donegal',2,'[{\"changed\": {\"fields\": [\"Price\", \"Stock\"]}}]',13,1),(34,'2020-04-28 15:02:10.257322','6','Brushed Heather',2,'[{\"changed\": {\"fields\": [\"Discount price\"]}}]',13,1),(35,'2020-04-28 15:09:47.832263','18','Hemp Stripe',2,'[{\"changed\": {\"fields\": [\"Discount price\"]}}]',13,1),(36,'2020-04-29 00:12:36.706008','18','Hemp Stripe',2,'[{\"changed\": {\"fields\": [\"Discount price\"]}}]',13,1),(37,'2020-04-29 21:34:25.809017','6','Brushed Heather',2,'[{\"changed\": {\"fields\": [\"Slug\"]}}]',13,1),(38,'2020-04-29 21:34:35.389205','14','Moto Jacket',2,'[]',13,1),(39,'2020-04-29 21:38:55.850037','6','Brushed Heather',2,'[]',13,1),(40,'2020-04-29 21:39:15.572255','6','Brushed Heather',2,'[{\"changed\": {\"fields\": [\"Slug\"]}}]',13,1),(41,'2020-05-01 14:32:25.349833','6','Brushed Heather',2,'[{\"changed\": {\"fields\": [\"Description\"]}}]',13,1),(42,'2020-05-01 14:32:35.142691','18','Hemp Stripe',2,'[{\"changed\": {\"fields\": [\"Description\"]}}]',13,1),(43,'2020-05-01 14:32:40.419687','13','The Cash Shirt',2,'[{\"changed\": {\"fields\": [\"Description\"]}}]',13,1),(44,'2020-05-01 14:33:01.241977','10','The Long Haul Jacket',2,'[{\"changed\": {\"fields\": [\"Description\"]}}]',13,1),(45,'2020-05-01 14:33:07.063516','16','Winslow Jacket',2,'[{\"changed\": {\"fields\": [\"Description\"]}}]',13,1),(46,'2020-05-01 18:04:14.816709','19','Hemp Donegal',2,'[{\"changed\": {\"fields\": [\"Description\"]}}]',13,1),(47,'2020-05-01 18:04:20.955143','14','Moto Jacket',2,'[{\"changed\": {\"fields\": [\"Description\"]}}]',13,1),(48,'2020-05-01 18:04:27.333591','17','Port Jacket',2,'[{\"changed\": {\"fields\": [\"Description\"]}}]',13,1),(49,'2020-05-01 18:04:35.025618','11','Sun Bleached',2,'[{\"changed\": {\"fields\": [\"Description\"]}}]',13,1),(50,'2020-05-01 18:04:42.319281','9','The Jack',2,'[{\"changed\": {\"fields\": [\"Description\"]}}]',13,1),(51,'2020-05-01 18:04:49.086419','15','Tobacco',2,'[{\"changed\": {\"fields\": [\"Description\"]}}]',13,1),(52,'2020-05-01 18:04:55.584178','7','Vintage Navy',2,'[{\"changed\": {\"fields\": [\"Description\"]}}]',13,1),(53,'2020-05-01 21:23:21.580674','6','Brushed Heather',2,'[{\"changed\": {\"fields\": [\"Size\"]}}]',13,1),(54,'2020-05-01 21:23:42.396241','19','Hemp Donegal',2,'[{\"changed\": {\"fields\": [\"Size\"]}}]',13,1),(55,'2020-05-01 21:23:48.210537','18','Hemp Stripe',2,'[{\"changed\": {\"fields\": [\"Size\"]}}]',13,1),(56,'2020-05-01 21:23:56.292488','18','Hemp Stripe',2,'[]',13,1),(57,'2020-05-01 22:05:50.600837','1','S',1,'[{\"added\": {}}]',16,1),(58,'2020-05-01 22:05:55.731415','2','M',1,'[{\"added\": {}}]',16,1),(59,'2020-05-01 22:06:00.193824','3','L',1,'[{\"added\": {}}]',16,1),(60,'2020-05-01 22:06:52.399342','1','StockItem object (1)',1,'[{\"added\": {}}]',18,1),(61,'2020-05-01 22:09:15.367470','2','Stock of product \"Brushed Heather\" for size \"M\"',1,'[{\"added\": {}}]',18,1),(62,'2020-05-01 22:09:24.788141','3','Stock of product \"Brushed Heather\" for size \"L\"',1,'[{\"added\": {}}]',18,1),(63,'2020-05-06 02:44:35.325247','4','1515651651',1,'[{\"added\": {}}]',16,1),(64,'2020-05-06 02:44:43.971999','4','1515651651',3,'',16,1),(65,'2020-05-06 15:05:42.877408','6','Brushed Heather',2,'[{\"changed\": {\"fields\": [\"Discount price\"]}}]',13,1),(66,'2020-05-06 15:06:14.467464','6','Brushed Heather',2,'[{\"changed\": {\"fields\": [\"Discount price\"]}}]',13,1),(67,'2020-05-13 04:09:58.906949','13','The Cash Shirt',3,'',13,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (7,'account','emailaddress'),(8,'account','emailconfirmation'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(13,'core','item'),(14,'core','order'),(15,'core','orderitem'),(17,'core','priceitem'),(16,'core','size'),(18,'core','stockitem'),(20,'payment','stripepayment'),(5,'sessions','session'),(6,'sites','site'),(9,'socialaccount','socialaccount'),(10,'socialaccount','socialapp'),(11,'socialaccount','socialtoken'),(19,'users','address'),(12,'users','user');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('02pizazyxi4c52263ouycg776ox94tjr','MDljOTgyMjU0NjIyZDk2MjY4MzUwYjkyOTQyNjk0NmQxMjk0ZWZjZTp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJmMzkyMmI1ZGVmODUyMDRiM2U4NjU4MTc4ZGQwMzdiZDNiMDY0ZmQyIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2020-05-28 01:35:32.796590'),('1562u3zxi548a56oyzebdg0mqtyma4lz','MWFiNjVmNmU2MWI5OTY3MTU4N2E0MDViMDA3YjdkM2E5YWI2ZmRlZjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYWxsYXV0aC5hY2NvdW50LmF1dGhfYmFja2VuZHMuQXV0aGVudGljYXRpb25CYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNzUzYzc4ZWYzNjYxOTkzMzQyMjAxNTVmMGQ5YzI1NzFiOTMyYzczYSIsIl9zZXNzaW9uX2V4cGlyeSI6MH0=','2020-06-12 18:40:43.992752'),('1gsej9ismw156ev3qs0dkqw8wsrsc7nz','MzQ3N2U4MDU2NGM0MjAwZGU5OTQ5NGZlMTI5OGM5OGE4MzNhMDA1OTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2020-06-06 18:48:48.877496'),('1hh2iz45bjv53yzi0q0fw8x0x41a8c1a','MzQ3N2U4MDU2NGM0MjAwZGU5OTQ5NGZlMTI5OGM5OGE4MzNhMDA1OTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2020-05-18 17:42:13.648634'),('2ujgfp5he8mjhvwxdtap4rs6l8lb3co6','MzQ3N2U4MDU2NGM0MjAwZGU5OTQ5NGZlMTI5OGM5OGE4MzNhMDA1OTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2020-06-08 23:54:13.617202'),('2zh7vp6vocojs2bgvvgpi7rn5wv77d46','MzQ3N2U4MDU2NGM0MjAwZGU5OTQ5NGZlMTI5OGM5OGE4MzNhMDA1OTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2020-05-30 01:05:43.267877'),('2zy5uu02p3a8rl542umpjiz4d4g39f3z','MzQ3N2U4MDU2NGM0MjAwZGU5OTQ5NGZlMTI5OGM5OGE4MzNhMDA1OTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2020-05-19 15:16:05.364399'),('34khwxf37ndxsxjsp9aoav1h5n3a0r8g','MWFiNjVmNmU2MWI5OTY3MTU4N2E0MDViMDA3YjdkM2E5YWI2ZmRlZjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYWxsYXV0aC5hY2NvdW50LmF1dGhfYmFja2VuZHMuQXV0aGVudGljYXRpb25CYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNzUzYzc4ZWYzNjYxOTkzMzQyMjAxNTVmMGQ5YzI1NzFiOTMyYzczYSIsIl9zZXNzaW9uX2V4cGlyeSI6MH0=','2020-06-12 01:37:34.372292'),('9a72zv53d7ubvo91wx8ehv9nsr3s0oyo','MzQ3N2U4MDU2NGM0MjAwZGU5OTQ5NGZlMTI5OGM5OGE4MzNhMDA1OTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2020-06-05 12:56:26.789450'),('9ozaxui4eqvdpwdxs5804nzmbjp9pp2e','MzQ3N2U4MDU2NGM0MjAwZGU5OTQ5NGZlMTI5OGM5OGE4MzNhMDA1OTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2020-05-28 17:50:45.226427'),('agyvb8svh6lxgqhxv5wl368168z7qhar','NjY4OWJlMDM1YmFmYWEwZTk3MWQwZDQyNTBhN2NjMTYwMTYzNzQwODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIn0=','2020-05-13 21:33:58.471193'),('b05g5bu2mtft31ci177li9vy498b7ipb','MWFiNjVmNmU2MWI5OTY3MTU4N2E0MDViMDA3YjdkM2E5YWI2ZmRlZjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYWxsYXV0aC5hY2NvdW50LmF1dGhfYmFja2VuZHMuQXV0aGVudGljYXRpb25CYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNzUzYzc4ZWYzNjYxOTkzMzQyMjAxNTVmMGQ5YzI1NzFiOTMyYzczYSIsIl9zZXNzaW9uX2V4cGlyeSI6MH0=','2020-06-15 14:17:40.538572'),('b6xi1wpd7kbg0c7s5u69tayzeqilfqnt','MzQ3N2U4MDU2NGM0MjAwZGU5OTQ5NGZlMTI5OGM5OGE4MzNhMDA1OTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2020-06-06 01:00:27.322918'),('cby4och7j4up098nso2j53nnw247hk86','Mjk0NDdmYTcxZTE3YTA0ZTJmNzRmZTdmYTA5YThlNjk1YmJmMDcxMzp7Il9hdXRoX3VzZXJfaWQiOiIzIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1OTZiOWJmN2UzZDg3OTU3NTMzNzM4N2JhYjlmZWM0MDExMjc3OGY0IiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2020-06-09 17:46:20.603779'),('cbyrat800yl7wmq5gw9xdutanxwo3z4x','MzQ3N2U4MDU2NGM0MjAwZGU5OTQ5NGZlMTI5OGM5OGE4MzNhMDA1OTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2020-05-28 17:14:47.035868'),('dmvmrp7r9o1tln33hdkbnv16t7ezxp0t','MzQ3N2U4MDU2NGM0MjAwZGU5OTQ5NGZlMTI5OGM5OGE4MzNhMDA1OTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2020-05-28 23:52:09.232019'),('e7rpwh6am3w9c0yhfqcjmscgcbtq9lzv','MzQ3N2U4MDU2NGM0MjAwZGU5OTQ5NGZlMTI5OGM5OGE4MzNhMDA1OTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2020-05-28 20:45:05.273063'),('ey38q15rpkzfywzz0wd6fem082tmh1sb','MzQ3N2U4MDU2NGM0MjAwZGU5OTQ5NGZlMTI5OGM5OGE4MzNhMDA1OTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2020-05-28 17:26:28.219454'),('eyyfp9o8evtxqg9uf2e8kzm64zmo4klc','MzQ3N2U4MDU2NGM0MjAwZGU5OTQ5NGZlMTI5OGM5OGE4MzNhMDA1OTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2020-06-07 15:28:22.917323'),('fsd8uregws5kcotn1j6si3hdxgasee5d','MzQ3N2U4MDU2NGM0MjAwZGU5OTQ5NGZlMTI5OGM5OGE4MzNhMDA1OTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2020-05-25 20:58:37.704588'),('g3y9web6bevi3py59rpht75a2vunb0t3','NjY4OWJlMDM1YmFmYWEwZTk3MWQwZDQyNTBhN2NjMTYwMTYzNzQwODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIn0=','2020-05-12 15:01:51.266204'),('hzrvyp2bdk8cy01oi4705dzgyjgy8k3g','MzQ3N2U4MDU2NGM0MjAwZGU5OTQ5NGZlMTI5OGM5OGE4MzNhMDA1OTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2020-05-26 13:16:15.862327'),('jhq9szri5jccchnae0j25451gbpy9tgy','MzQ3N2U4MDU2NGM0MjAwZGU5OTQ5NGZlMTI5OGM5OGE4MzNhMDA1OTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2020-05-25 18:45:04.907297'),('kbgf9czcvudw99pg50rbdems3haeqks8','NjY4OWJlMDM1YmFmYWEwZTk3MWQwZDQyNTBhN2NjMTYwMTYzNzQwODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIn0=','2020-05-27 21:36:06.418765'),('kqs496r7xqhc95k15uh73mztp11tsvny','MDljOTgyMjU0NjIyZDk2MjY4MzUwYjkyOTQyNjk0NmQxMjk0ZWZjZTp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJmMzkyMmI1ZGVmODUyMDRiM2U4NjU4MTc4ZGQwMzdiZDNiMDY0ZmQyIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2020-05-28 00:10:20.661501'),('krd85oe2b5ifyd54qcn7e3yvjztjyx8d','NjY4OWJlMDM1YmFmYWEwZTk3MWQwZDQyNTBhN2NjMTYwMTYzNzQwODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIn0=','2020-05-07 22:30:55.916717'),('lbvu99t4ch1p0e5srdsqpm464g8q39dm','MzQ3N2U4MDU2NGM0MjAwZGU5OTQ5NGZlMTI5OGM5OGE4MzNhMDA1OTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2020-05-17 19:55:57.110205'),('mj27isvtyjw9zex9wq370vzmv66vr9ps','MzQ3N2U4MDU2NGM0MjAwZGU5OTQ5NGZlMTI5OGM5OGE4MzNhMDA1OTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2020-05-16 17:49:47.092631'),('olkzl5penw1yiajt9wenq1oyl3gl5lmb','MzQ3N2U4MDU2NGM0MjAwZGU5OTQ5NGZlMTI5OGM5OGE4MzNhMDA1OTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2020-05-18 17:10:08.025873'),('qcwvyt6b7lhc2vs9adlbnx3n1oekvjzd','MzQ3N2U4MDU2NGM0MjAwZGU5OTQ5NGZlMTI5OGM5OGE4MzNhMDA1OTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2020-06-07 23:33:44.328423'),('rn74s2jawxk6q9i9112lqjxwsgze9yjk','MzQ3N2U4MDU2NGM0MjAwZGU5OTQ5NGZlMTI5OGM5OGE4MzNhMDA1OTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2020-06-05 05:34:28.283249'),('tabdvj9e7qv8ri4tlzfwjiiunkc6khep','MzQ3N2U4MDU2NGM0MjAwZGU5OTQ5NGZlMTI5OGM5OGE4MzNhMDA1OTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2020-06-10 15:36:42.437910'),('twgp0rnzx7nx6andrpx4rhxf3kci2tze','MzQ3N2U4MDU2NGM0MjAwZGU5OTQ5NGZlMTI5OGM5OGE4MzNhMDA1OTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2020-05-17 04:12:31.945841'),('u0iambtx5vp7rj57fsqrx17hhx1d7m0g','NjY4OWJlMDM1YmFmYWEwZTk3MWQwZDQyNTBhN2NjMTYwMTYzNzQwODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIn0=','2020-05-07 22:53:35.683091'),('xkuc76z4msztqyu1suxhmhjfdzjitlx2','MzQ3N2U4MDU2NGM0MjAwZGU5OTQ5NGZlMTI5OGM5OGE4MzNhMDA1OTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2020-06-08 17:56:51.107833'),('yukq47pmkeike7mtfbdqmqt7mzblkzog','ZTZjYjUyYWMwNDE0MGZhODliY2M3MzlmM2ZkNGY2MTNiMTk1OGI3Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0YmNmY2YyNjM1YWUxNDUzZmNmOWQzYzZiMWE3OThmODBjZDY4ZTY1IiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2020-05-04 13:48:04.688425'),('zh8bplxi00pmium8xx5kqikkci86m325','NjY4OWJlMDM1YmFmYWEwZTk3MWQwZDQyNTBhN2NjMTYwMTYzNzQwODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIn0=','2020-05-10 13:01:18.753072'),('zu547etmmllm54ompdwr2a2w8j3e9q8d','MzQ3N2U4MDU2NGM0MjAwZGU5OTQ5NGZlMTI5OGM5OGE4MzNhMDA1OTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NTNjNzhlZjM2NjE5OTMzNDIyMDE1NWYwZDljMjU3MWI5MzJjNzNhIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2020-05-29 16:59:32.009353');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_site_domain_a2e37b91_uniq` (`domain`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_stripepayment`
--

DROP TABLE IF EXISTS `payment_stripepayment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payment_stripepayment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `payment_intent_id` varchar(50) DEFAULT NULL,
  `order_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_id` (`order_id`),
  KEY `payment_stripepayment_user_id_bddf4fe2_fk_users_user_id` (`user_id`),
  CONSTRAINT `payment_stripepayment_order_id_aa8c570a_fk_core_order_id` FOREIGN KEY (`order_id`) REFERENCES `core_order` (`id`),
  CONSTRAINT `payment_stripepayment_user_id_bddf4fe2_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_stripepayment`
--

LOCK TABLES `payment_stripepayment` WRITE;
/*!40000 ALTER TABLE `payment_stripepayment` DISABLE KEYS */;
/*!40000 ALTER TABLE `payment_stripepayment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialaccount`
--

DROP TABLE IF EXISTS `socialaccount_socialaccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `socialaccount_socialaccount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provider` varchar(30) NOT NULL,
  `uid` varchar(191) NOT NULL,
  `last_login` datetime(6) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `extra_data` longtext NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialaccount_provider_uid_fc810c6e_uniq` (`provider`,`uid`),
  KEY `socialaccount_socialaccount_user_id_8146e70c_fk_users_user_id` (`user_id`),
  CONSTRAINT `socialaccount_socialaccount_user_id_8146e70c_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialaccount`
--

LOCK TABLES `socialaccount_socialaccount` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialaccount` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialaccount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialapp`
--

DROP TABLE IF EXISTS `socialaccount_socialapp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `socialaccount_socialapp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provider` varchar(30) NOT NULL,
  `name` varchar(40) NOT NULL,
  `client_id` varchar(191) NOT NULL,
  `secret` varchar(191) NOT NULL,
  `key` varchar(191) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialapp`
--

LOCK TABLES `socialaccount_socialapp` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialapp` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialapp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialapp_sites`
--

DROP TABLE IF EXISTS `socialaccount_socialapp_sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `socialaccount_socialapp_sites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `socialapp_id` int(11) NOT NULL,
  `site_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialapp_sites_socialapp_id_site_id_71a9a768_uniq` (`socialapp_id`,`site_id`),
  KEY `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` (`site_id`),
  CONSTRAINT `socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc` FOREIGN KEY (`socialapp_id`) REFERENCES `socialaccount_socialapp` (`id`),
  CONSTRAINT `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialapp_sites`
--

LOCK TABLES `socialaccount_socialapp_sites` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialapp_sites` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialapp_sites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialtoken`
--

DROP TABLE IF EXISTS `socialaccount_socialtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `socialaccount_socialtoken` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` longtext NOT NULL,
  `token_secret` longtext NOT NULL,
  `expires_at` datetime(6) DEFAULT NULL,
  `account_id` int(11) NOT NULL,
  `app_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq` (`app_id`,`account_id`),
  KEY `socialaccount_social_account_id_951f210e_fk_socialacc` (`account_id`),
  CONSTRAINT `socialaccount_social_account_id_951f210e_fk_socialacc` FOREIGN KEY (`account_id`) REFERENCES `socialaccount_socialaccount` (`id`),
  CONSTRAINT `socialaccount_social_app_id_636a42d7_fk_socialacc` FOREIGN KEY (`app_id`) REFERENCES `socialaccount_socialapp` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialtoken`
--

LOCK TABLES `socialaccount_socialtoken` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_address`
--

DROP TABLE IF EXISTS `users_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_address` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `billing_address` varchar(255) DEFAULT NULL,
  `billing_zip` varchar(50) DEFAULT NULL,
  `default_billing_address` tinyint(1) NOT NULL,
  `default_shipping_address` tinyint(1) NOT NULL,
  `shipping_address` varchar(255) DEFAULT NULL,
  `shipping_zip` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `users_address_user_id_4c106ba4_fk_users_user_id` (`user_id`),
  CONSTRAINT `users_address_user_id_4c106ba4_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_address`
--

LOCK TABLES `users_address` WRITE;
/*!40000 ALTER TABLE `users_address` DISABLE KEYS */;
INSERT INTO `users_address` VALUES (7,1,'45 Rue du Président François Mitterrand','91160',0,1,'45 Rue du Président François Mitterrand','91160');
/*!40000 ALTER TABLE `users_address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user`
--

DROP TABLE IF EXISTS `users_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `stripe_customer_id` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user`
--

LOCK TABLES `users_user` WRITE;
/*!40000 ALTER TABLE `users_user` DISABLE KEYS */;
INSERT INTO `users_user` VALUES (1,'pbkdf2_sha256$180000$88QgOwC2Cxf6$489yfB13X3joLbd170IpRBq6rdqsEeHNfhW5JOV7tSE=','2020-06-01 14:17:40.480572',1,'rouizi','','','cinorouizi@gmail.com',1,1,'2020-04-20 13:47:49.629779',NULL),(2,'pbkdf2_sha256$180000$Qdx9GWZulZfQ$yLRkv2iX0XV5WhY8mWOZ01fFgLNt996BuICxR8igJDM=','2020-05-14 01:37:02.256942',0,'alfa','','','',0,1,'2020-05-04 16:49:32.574666',NULL),(3,'pbkdf2_sha256$180000$MS7ftLWVtqp7$YUIEh+Tr497C4kWm0HnOHQt2ACGlNXY52Ob1Qs1VWlg=','2020-05-29 01:37:06.460285',0,'beta','','','cinorouizi@hotmail.com',0,1,'2020-05-04 17:07:38.784003',NULL);
/*!40000 ALTER TABLE `users_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user_groups`
--

DROP TABLE IF EXISTS `users_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_user_groups_user_id_group_id_b88eab82_uniq` (`user_id`,`group_id`),
  KEY `users_user_groups_group_id_9afc8d0e_fk_auth_group_id` (`group_id`),
  CONSTRAINT `users_user_groups_group_id_9afc8d0e_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `users_user_groups_user_id_5f6f5a90_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user_groups`
--

LOCK TABLES `users_user_groups` WRITE;
/*!40000 ALTER TABLE `users_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user_user_permissions`
--

DROP TABLE IF EXISTS `users_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_user_user_permissions_user_id_permission_id_43338c45_uniq` (`user_id`,`permission_id`),
  KEY `users_user_user_perm_permission_id_0b93982e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `users_user_user_perm_permission_id_0b93982e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `users_user_user_permissions_user_id_20aca447_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user_user_permissions`
--

LOCK TABLES `users_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `users_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-06-05 16:49:18
