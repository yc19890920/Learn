/*
    sql 版本库维护
*/

USE spike;

-- version: 1.0
-- date 2019-10-18
-- 商品库存
CREATE TABLE IF NOT EXISTS `goods` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `num` int(11) NOT NULL default 0 COMMENT '商品库存',
  `version` int(11) NOT NULL default 0,
  PRIMARY KEY (`id`)
) ENGINE = InnoDB AUTO_INCREMENT=0 CHARSET=utf8 COLLATE utf8_general_ci COMMENT = '商品';

-- CREATE TABLE `poetry`.`aa` (
--     `id` INT(11) NOT NULL AUTO_INCREMENT ,
--     `a` VARCHAR(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'aa' ,
--     `b` INT(11) NOT NULL DEFAULT '0' COMMENT 'b' ,
--      PRIMARY KEY (`id`)
-- ) ENGINE = InnoDB CHARSET=utf8 COLLATE utf8_general_ci COMMENT = '测试';