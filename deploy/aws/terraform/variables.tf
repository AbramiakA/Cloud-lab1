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
  description = "GitHub repository in OWNER/REPO format"
  default     = "AbramiakA/Cloud-lab1"
}