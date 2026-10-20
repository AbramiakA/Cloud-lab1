variable "region" {
  type    = string
  default = "eu-north-1"
}

variable "project" {
  type    = string
  default = "lab1"
}

variable "github_repository" {
  type        = string
  description = "GitHub immutable repository identifier for OIDC"
  default     = "AbramiakA@152866337/Cloud-lab1@1427139567"
}