CREATE TABLE `team` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(64) NOT NULL,
    `created_at` DATETIME(6) NOT NULL  COMMENT '创建时间',
    `updated_at` DATETIME(6) NOT NULL  COMMENT '修改时间',
    `description` LONGTEXT   COMMENT '描述'
) CHARACTER SET utf8mb4 COMMENT='Team';
CREATE TABLE `tournament` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'id',
    `name` VARCHAR(64) NOT NULL UNIQUE COMMENT '名称',
    `description` LONGTEXT   COMMENT '描述',
    `created_at` DATETIME(6) NOT NULL  COMMENT '创建时间',
    `updated_at` DATETIME(6) NOT NULL  COMMENT '修改时间',
    KEY `idx_tournament_created_450ed3` (`created_at`, `updated_at`)
) CHARACTER SET utf8mb4 COMMENT='Tournament';
CREATE TABLE `event` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(64) NOT NULL,
    `prize` DECIMAL(10,2),
    `created_at` DATETIME(6) NOT NULL  COMMENT '创建时间',
    `updated_at` DATETIME(6) NOT NULL  COMMENT '修改时间',
    `tournament_id` INT NOT NULL,
    CONSTRAINT `fk_event_tourname_c3757249` FOREIGN KEY (`tournament_id`) REFERENCES `tournament` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='Event';
CREATE TABLE `event_team` (
    `event_id` INT NOT NULL,
    `team_id` INT NOT NULL,
    FOREIGN KEY (`event_id`) REFERENCES `event` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`team_id`) REFERENCES `team` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;