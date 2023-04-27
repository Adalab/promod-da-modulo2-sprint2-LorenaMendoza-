-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema universidades
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema universidades
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `universidades` ;
USE `universidades` ;

-- -----------------------------------------------------
-- Table `universidades`.`paises`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `universidades`.`paises` (
  `idestado` INT NOT NULL AUTO_INCREMENT,
  `nombre_pais` VARCHAR(45) NULL,
  `nombre_provincia` VARCHAR(45) NULL,
  `latitud` DECIMAL NULL,
  `longitud` DECIMAL NULL,
  PRIMARY KEY (`idestado`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `universidades`.`universidades`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `universidades`.`universidades` (
  `iduniversidades` INT NOT NULL AUTO_INCREMENT,
  `nombre_universidad` VARCHAR(45) NULL,
  `pagina_web` VARCHAR(45) NULL,
  `paises_idestado` INT NOT NULL,
  PRIMARY KEY (`iduniversidades`),
  INDEX `fk_universidades_paises_idx` (`paises_idestado` ASC) VISIBLE,
  CONSTRAINT `fk_universidades_paises`
    FOREIGN KEY (`paises_idestado`)
    REFERENCES `universidades`.`paises` (`idestado`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
