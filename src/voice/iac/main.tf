terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = "c200eb32-5f5e-4701-b1bc-bfee3ad94d30"
  tenant_id       = "5fb3ddb2-67cf-4c65-bacc-e818fd7722e4"
}

resource "azurerm_resource_group" "rg" {
  name     = var.rg_name
  location = var.location
}

resource "azurerm_cognitive_account" "openai" {
  name                = var.account_name
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  kind                = "OpenAI"
  sku_name            = var.sku
}
