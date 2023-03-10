terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

variable "provider_url" {
  type = string
}
variable "region" {
  type = string
}
variable "role_name" {
  type = string
}
variable "ns_sa" {
  type = list(string)
}
variable "policies" {
  type = list(string)
}
provider "aws" {
  region = var.region
  profile = "default"
}
data "tls_certificate" "cert" {
  url = var.provider_url
}

resource "aws_iam_openid_connect_provider" "oidc_provider" {
  url = var.provider_url
  client_id_list = ["sts.amazonaws.com"]
  thumbprint_list = [data.tls_certificate.cert.certificates.0.sha1_fingerprint]
}

resource "aws_iam_role" "role" {
  name = var.role_name
  assume_role_policy =  jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Federated": aws_iam_openid_connect_provider.oidc_provider.arn
        },
        "Action": "sts:AssumeRoleWithWebIdentity",
        "Condition": {
          "StringEquals": {
            "${replace(var.provider_url, "https://", "")}:sub": var.ns_sa
          }
        }
      }
    ]
  })
depends_on = [aws_iam_openid_connect_provider.oidc_provider]
}

resource "aws_iam_role_policy_attachment" "policy_attachment" {
  for_each = toset(var.policies)
  role       = aws_iam_role.role.name
  policy_arn = each.value
  depends_on = [aws_iam_role.role]
}

output "iam_role_arn" {
  value = aws_iam_role.role.arn
}
output "iam_provider_arn" {
  value = aws_iam_openid_connect_provider.oidc_provider.arn
}

