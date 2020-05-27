-- migrate:up

BEGIN;

SET FOREIGN_KEY_CHECKS = 0;

ALTER TABLE `team` DROP COLUMN `description2`;
ALTER TABLE `team` ADD COLUMN `description3` LONGTEXT COMMENT '描述' AFTER `description`;

SET FOREIGN_KEY_CHECKS = 1;

COMMIT;

-- migrate:down

BEGIN;

SET FOREIGN_KEY_CHECKS = 0;

ALTER TABLE `team` DROP COLUMN `description3`;
ALTER TABLE `team` ADD COLUMN `description2` LONGTEXT COMMENT '描述' AFTER `description`;

SET FOREIGN_KEY_CHECKS = 1;

COMMIT;