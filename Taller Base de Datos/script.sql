-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `mydb` ;

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Empleados`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Empleados` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Empleados` (
  `cuil` INT NOT NULL,
  `nombre` VARCHAR(45) NULL,
  `apellido` VARCHAR(45) NULL,
  `edad` VARCHAR(45) NULL,
  PRIMARY KEY (`cuil`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Cliente`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Cliente` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Cliente` (
  `idCLiente` INT NOT NULL AUTO_INCREMENT,
  `cuil` VARCHAR(45) NULL,
  `nombre` VARCHAR(45) NULL,
  `edad` INT NULL,
  `puntos` INT NULL,
  `Empleados_cuil` INT NOT NULL,
  PRIMARY KEY (`idCLiente`),
  INDEX `fk_Cliente_Empleados1_idx` (`Empleados_cuil` ASC) VISIBLE,
  CONSTRAINT `fk_Cliente_Empleados1`
    FOREIGN KEY (`Empleados_cuil`)
    REFERENCES `mydb`.`Empleados` (`cuil`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Proveedores`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Proveedores` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Proveedores` (
  `cuil` INT NOT NULL,
  `nombre` VARCHAR(45) NULL,
  `apellido` VARCHAR(45) NULL,
  `empresas` VARCHAR(45) NULL,
  `provee` VARCHAR(45) NULL,
  `Empleados_cuil` INT NOT NULL,
  PRIMARY KEY (`cuil`),
  INDEX `fk_Proveedores_Empleados1_idx` (`Empleados_cuil` ASC) VISIBLE,
  CONSTRAINT `fk_Proveedores_Empleados1`
    FOREIGN KEY (`Empleados_cuil`)
    REFERENCES `mydb`.`Empleados` (`cuil`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Productos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Productos` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Productos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `marca` VARCHAR(45) NULL,
  `cantidad` INT NULL,
  `precio` FLOAT NULL,
  `Proveedores_cuil` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Productos_Proveedores1_idx` (`Proveedores_cuil` ASC) VISIBLE,
  CONSTRAINT `fk_Productos_Proveedores1`
    FOREIGN KEY (`Proveedores_cuil`)
    REFERENCES `mydb`.`Proveedores` (`cuil`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Facturas`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Facturas` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Facturas` (
  `numero` INT NOT NULL AUTO_INCREMENT,
  `tipo` VARCHAR(45) NULL,
  PRIMARY KEY (`numero`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Facturacion`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Facturacion` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Facturacion` (
  `fecha` DATE NOT NULL,
  `importe` FLOAT NOT NULL,
  `Cliente_idCLiente` INT NOT NULL,
  `Facturas_numero` INT NOT NULL,
  `Productos_id` INT NOT NULL,
  INDEX `fk_Facturacion_Cliente_idx` (`Cliente_idCLiente` ASC) VISIBLE,
  INDEX `fk_Facturacion_Facturas1_idx` (`Facturas_numero` ASC) VISIBLE,
  INDEX `fk_Facturacion_Productos1_idx` (`Productos_id` ASC) VISIBLE,
  CONSTRAINT `fk_Facturacion_Cliente`
    FOREIGN KEY (`Cliente_idCLiente`)
    REFERENCES `mydb`.`Cliente` (`idCLiente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Facturacion_Facturas1`
    FOREIGN KEY (`Facturas_numero`)
    REFERENCES `mydb`.`Facturas` (`numero`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Facturacion_Productos1`
    FOREIGN KEY (`Productos_id`)
    REFERENCES `mydb`.`Productos` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
