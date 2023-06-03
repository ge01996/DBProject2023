drop database schooldb;
create database schooldb;

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';


CREATE SCHEMA IF NOT EXISTS `schooldb` DEFAULT CHARACTER SET utf8 ;
USE `schooldb` ;



-- -----------------------------------------------------
-- Table `schooldb`.`role`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `schooldb`.`role` ;

CREATE TABLE IF NOT EXISTS `schooldb`.`role` (
  `id` CHAR(1) NOT NULL,
  `role_desc` TEXT(1000) NOT NULL,
  PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `schooldb`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `schooldb`.`users` ;

CREATE TABLE IF NOT EXISTS `schooldb`.`users` (
  `id` INT(10)  AUTO_INCREMENT,
  `username` VARCHAR(15) NOT NULL,
  `password` VARCHAR(20) NOT NULL,
  `first_name` VARCHAR(20) NOT NULL,
  `last_name` VARCHAR(20) NOT NULL,
  `birthdate` DATE NULL DEFAULT NULL,
  `address` VARCHAR(50) NOT NULL,
  `zip_code` CHAR(5) NOT NULL,
  `role_id` CHAR(1) NOT NULL,
  `curr_rnt` INT(1) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX (`role_id` ASC) VISIBLE,
  CONSTRAINT ``
    FOREIGN KEY (`role_id`)
    REFERENCES `mydb`.`role` (`id`)
    ON UPDATE cascade);


-- -----------------------------------------------------
-- Table `schooldb`.`book`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `schooldb`.`book` ;

CREATE TABLE IF NOT EXISTS `schooldb`.`book` (
  `id` INT(10) AUTO_INCREMENT,
  `isbn` CHAR(13) NOT NULL,
  `title` VARCHAR(30) NOT NULL,
  `publisher` VARCHAR(20) NOT NULL,
  `summary` TEXT(1000) NOT NULL,
  `lang` VARCHAR(20) NOT NULL,
  `pages` SMALLINT(5) NOT NULL,
  `coverurl` VARCHAR(100)  DEFAULT 'C:\dbproject-main\images.png',
  PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `schooldb`.`school`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `schooldb`.`school` ;

CREATE TABLE IF NOT EXISTS `schooldb`.`school` (
  `id` INT(10)  AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  `email` VARCHAR(30) NOT NULL,
  `principal` VARCHAR(40) NOT NULL,
  `librarian` VARCHAR(40) NOT NULL,
  `city` VARCHAR(20) NOT NULL,
  `address` VARCHAR(60) NOT NULL,
  `zip_code` CHAR(5) NOT NULL,
  `phone` CHAR(17) NOT NULL,
  PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `schooldb`.`schoolbook`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `schooldb`.`schoolbook` ;

CREATE TABLE IF NOT EXISTS `schooldb`.`schoolbook` (
  `school_id` INT(10) NOT NULL,
  `book_id` INT(10) NOT NULL,
  `curr_copies` INT(3) NOT NULL,
  `tot_copies` INT(3) NOT NULL,
  PRIMARY KEY (`school_id`, `book_id`),
  INDEX (`book_id` ASC) VISIBLE,
  CONSTRAINT ``
    FOREIGN KEY (`school_id`)
    REFERENCES `schooldb`.`school` (`id`)
    ON UPDATE cascade,
  CONSTRAINT ``
    FOREIGN KEY (`book_id`)
    REFERENCES `schooldb`.`book` (`id`)
    ON UPDATE cascade);


-- -----------------------------------------------------
-- Table `schooldb`.`schooluser`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `schooldb`.`schooluser` ;

CREATE TABLE IF NOT EXISTS `schooldb`.`schooluser` (
  `user_id` INT(10) NOT NULL,
  `school_id` INT(10) NOT NULL,
  PRIMARY KEY (`user_id`, `school_id`),
  INDEX (`school_id` ASC) VISIBLE,
  CONSTRAINT ``
    FOREIGN KEY (`user_id`)
    REFERENCES `mydb`.`users` (`id`)
    ON UPDATE cascade,
  CONSTRAINT ``
    FOREIGN KEY (`school_id`)
    REFERENCES `mydb`.`school` (`id`)
    ON UPDATE cascade);


-- -----------------------------------------------------
-- Table `schooldb`.`writer`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `schooldb`.`writer` ;

CREATE TABLE IF NOT EXISTS `schooldb`.`writer` (
  `id` INT(10) NOT NULL,
  `name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`name`),
  CONSTRAINT ``
    FOREIGN KEY ()
    REFERENCES `schooldb`.`book` ()
    ON UPDATE cascade);


-- -----------------------------------------------------
-- Table `schooldb`.`bwriter`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `schooldb`.`bwriter` ;

CREATE TABLE IF NOT EXISTS `schooldb`.`bwriter` (
  `book_id` INT(10) NOT NULL,
  `writer_id` INT(10) NOT NULL,
  PRIMARY KEY (`book_id`, `writer_id`),
  INDEX (`writer_id` ASC) VISIBLE,
  CONSTRAINT ``
    FOREIGN KEY (`book_id`)
    REFERENCES `mydb`.`book` (`id`)
    ON UPDATE cascade,
  CONSTRAINT ``
    FOREIGN KEY (`writer_id`)
    REFERENCES `mydb`.`writer` (`id`)
    ON UPDATE cascade);


-- -----------------------------------------------------
-- Table `schooldb`.`category`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `schooldb`.`category` ;

CREATE TABLE IF NOT EXISTS `schooldb`.`category` (
  `id` INT(10)  AUTO_INCREMENT,
  `name` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `schooldb`.`bookcat`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `schooldb`.`bookcat` ;

CREATE TABLE IF NOT EXISTS `schooldb`.`bookcat` (
  `book_id` INT(10) NOT NULL,
  `cat_id` INT(10) NOT NULL,
  PRIMARY KEY (`book_id`),
  INDEX (`cat_id` ASC) VISIBLE,
  CONSTRAINT ``
    FOREIGN KEY (`book_id`)
    REFERENCES `mydb`.`book` (`id`)
    ON UPDATE cascade,
  CONSTRAINT ``
    FOREIGN KEY (`cat_id`)
    REFERENCES `mydb`.`category` (`id`)
    ON UPDATE cascade);


-- -----------------------------------------------------
-- Table `schooldb`.`keyword`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `schooldb`.`keyword` ;

CREATE TABLE IF NOT EXISTS `schooldb`.`keyword` (
  `book_id` INT(10) NOT NULL,
  `word` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`book_id`),
  CONSTRAINT ``
    FOREIGN KEY (`book_id`)
    REFERENCES `mydb`.`book` (`id`));


-- -----------------------------------------------------
-- Table `schooldb`.`rental`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `schooldb`.`rental` ;

CREATE TABLE IF NOT EXISTS `schooldb`.`rental` (
  `user_id` INT(10) NOT NULL,
  `book_id` INT(10) NOT NULL,
  `trdate` DATE NULL DEFAULT CURRENT_TIMESTAMP,
  `status` CHAR(1) NOT NULL,
  `libr_id` INT(10) NOT NULL,
  PRIMARY KEY (`user_id`, `book_id`, `trdate`),
  INDEX (`book_id` ASC) VISIBLE,
  INDEX (`libr_id` ASC) VISIBLE,
  CONSTRAINT ``
    FOREIGN KEY (`user_id`)
    REFERENCES `mydb`.`users` (`id`)
    ON UPDATE cascade,
  CONSTRAINT ``
    FOREIGN KEY (`book_id`)
    REFERENCES `mydb`.`book` (`id`)
    ON UPDATE cascade,
  CONSTRAINT ``
    FOREIGN KEY (`libr_id`)
    REFERENCES `mydb`.`users` (`id`)
    ON UPDATE cascade);


-- -----------------------------------------------------
-- Table `schooldb`.`reservation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `schooldb`.`reservation` ;

CREATE TABLE IF NOT EXISTS `schooldb`.`reservation` (
  `user_id` INT(10) NOT NULL,
  `book_id` INT(10) NOT NULL,
  `trdate` DATE  DEFAULT CURRENT_TIMESTAMP,
  `status` CHAR(1) NOT NULL,
  PRIMARY KEY (`user_id`, `book_id`, `trdate`),
  INDEX (`book_id` ASC) VISIBLE,
  CONSTRAINT ``
    FOREIGN KEY (`user_id`)
    REFERENCES `mydb`.`users` (`id`)
    ON UPDATE cascade,
  CONSTRAINT ``
    FOREIGN KEY (`book_id`)
    REFERENCES `mydb`.`book` (`id`)
    ON UPDATE cascade);


-- -----------------------------------------------------
-- Table `schooldb`.`rating`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `schooldb`.`rating` ;

CREATE TABLE IF NOT EXISTS `schooldb`.`rating` (
  `user_id` INT(10) NOT NULL,
  `book_id` INT(10) NOT NULL,
  `trdate` DATE  DEFAULT CURRENT_TIMESTAMP,
  `ratetext` TEXT(1000) NULL DEFAULT NULL,
  `likert` TINYINT(1) NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`, `book_id`),
  INDEX (`book_id` ASC) VISIBLE,
  CONSTRAINT ``
    FOREIGN KEY (`user_id`)
    REFERENCES `mydb`.`users` (`id`)
    ON UPDATE cascade,
  CONSTRAINT ``
    FOREIGN KEY (`book_id`)
    REFERENCES `mydb`.`book` (`id`)
    ON UPDATE cascade);


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
