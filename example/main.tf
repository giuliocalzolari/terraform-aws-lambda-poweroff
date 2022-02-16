terraform {
  required_version = ">= 1.0"
  backend "local" {}
}


variable "region" {
  default = "eu-west-1"
}

provider "aws" {
  region = var.region
}

module "lambda_poweroff" {
  source = "../"

  extra_tags = {
    CreatedBy = "Terraform"
    App       = "lambda_poweroff"
  }
}

