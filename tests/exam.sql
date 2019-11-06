/*
 Navicat Premium Data Transfer

 Source Server         : localhost-mysql
 Source Server Type    : MySQL
 Source Server Version : 50722
 Source Host           : 127.0.0.1:3306
 Source Schema         : exam

 Target Server Type    : MySQL
 Target Server Version : 50722
 File Encoding         : 65001

 Date: 06/11/2019 10:17:10
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for t_course
-- ----------------------------
DROP TABLE IF EXISTS `t_course`;
CREATE TABLE `t_course` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL,
  `no` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_course
-- ----------------------------
BEGIN;
INSERT INTO `t_course` VALUES (1, '高等数学', 1001);
INSERT INTO `t_course` VALUES (2, '马克思', 1001);
INSERT INTO `t_course` VALUES (3, '大学英语', 1002);
INSERT INTO `t_course` VALUES (4, '数据库', 1002);
INSERT INTO `t_course` VALUES (5, '数据结构', 1003);
COMMIT;

-- ----------------------------
-- Table structure for t_sc
-- ----------------------------
DROP TABLE IF EXISTS `t_sc`;
CREATE TABLE `t_sc` (
  `sid` int(11) NOT NULL,
  `cid` int(11) NOT NULL,
  `score` int(11) DEFAULT NULL,
  PRIMARY KEY (`sid`,`cid`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_sc
-- ----------------------------
BEGIN;
INSERT INTO `t_sc` VALUES (1001, 1, 100);
INSERT INTO `t_sc` VALUES (1001, 2, 80);
INSERT INTO `t_sc` VALUES (1001, 3, 70);
INSERT INTO `t_sc` VALUES (1001, 4, 60);
INSERT INTO `t_sc` VALUES (1001, 5, 50);
INSERT INTO `t_sc` VALUES (1002, 1, 60);
INSERT INTO `t_sc` VALUES (1002, 2, 50);
INSERT INTO `t_sc` VALUES (1002, 3, 80);
INSERT INTO `t_sc` VALUES (1002, 4, 30);
INSERT INTO `t_sc` VALUES (1002, 5, 100);
INSERT INTO `t_sc` VALUES (1003, 1, 60);
INSERT INTO `t_sc` VALUES (1003, 2, 80);
INSERT INTO `t_sc` VALUES (1003, 3, 60);
INSERT INTO `t_sc` VALUES (1003, 4, 40);
INSERT INTO `t_sc` VALUES (1004, 1, 20);
INSERT INTO `t_sc` VALUES (1004, 2, 100);
INSERT INTO `t_sc` VALUES (1004, 3, 30);
INSERT INTO `t_sc` VALUES (1004, 5, 40);
INSERT INTO `t_sc` VALUES (1005, 2, 80);
INSERT INTO `t_sc` VALUES (1005, 3, 60);
INSERT INTO `t_sc` VALUES (1005, 4, 50);
INSERT INTO `t_sc` VALUES (1006, 2, 100);
INSERT INTO `t_sc` VALUES (1006, 5, 100);
INSERT INTO `t_sc` VALUES (1007, 1, 50);
INSERT INTO `t_sc` VALUES (1007, 4, 40);
INSERT INTO `t_sc` VALUES (1008, 3, 60);
COMMIT;

-- ----------------------------
-- Table structure for t_student
-- ----------------------------
DROP TABLE IF EXISTS `t_student`;
CREATE TABLE `t_student` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL,
  `sex` varchar(8) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1010 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_student
-- ----------------------------
BEGIN;
INSERT INTO `t_student` VALUES (1001, '牛一', '男');
INSERT INTO `t_student` VALUES (1002, '蔡二', '女');
INSERT INTO `t_student` VALUES (1003, '张三', '男');
INSERT INTO `t_student` VALUES (1004, '李四', '女');
INSERT INTO `t_student` VALUES (1005, '王五', '男');
INSERT INTO `t_student` VALUES (1006, '李志基', '男');
INSERT INTO `t_student` VALUES (1007, '陈李强', '男');
INSERT INTO `t_student` VALUES (1008, '王八', '女');
INSERT INTO `t_student` VALUES (1009, '张仲景', '男');
COMMIT;

-- ----------------------------
-- Table structure for t_teacher
-- ----------------------------
DROP TABLE IF EXISTS `t_teacher`;
CREATE TABLE `t_teacher` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1006 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_teacher
-- ----------------------------
BEGIN;
INSERT INTO `t_teacher` VALUES (1001, '叶平');
INSERT INTO `t_teacher` VALUES (1002, '李金洋');
INSERT INTO `t_teacher` VALUES (1003, '易法令');
INSERT INTO `t_teacher` VALUES (1004, '李闵');
INSERT INTO `t_teacher` VALUES (1005, '陈国华');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
