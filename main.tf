resource "aws_apprunner_service" "staging" {
  service_name = "api-medica-lacrei-staging"

  source_configuration {
    image_repository {
      image_identifier      = "${var.docker_username}/api-medica-lacrei:latest"
      image_repository_type = "PUBLIC" # Ou PRIVATE se usar ECR
    }
    auto_deployments_enabled = true
  }

  instance_configuration {
    cpu    = "1024"
    memory = "2048"
  }
}