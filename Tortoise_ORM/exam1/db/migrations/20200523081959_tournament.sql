-- migrate:up

BEGIN;

SET FOREIGN_KEY_CHECKS = 0;

ALTER TABLE `tournament` ADD INDEX `idx_tournament_created_450ed3` (`created_at`, `updated_at`);
ALTER TABLE `team` ADD COLUMN `description` LONGTEXT COMMENT '描述' AFTER `updated_at`;

SET FOREIGN_KEY_CHECKS = 1;

COMMIT;

-- migrate:down

BEGIN;

SET FOREIGN_KEY_CHECKS = 0;

ALTER TABLE `team` DROP COLUMN `description`;
ALTER TABLE `tournament` DROP INDEX `idx_tournament_created_450ed3`;

SET FOREIGN_KEY_CHECKS = 1;

COMMIT;