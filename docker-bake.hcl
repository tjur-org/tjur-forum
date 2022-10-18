variable "IMAGE_TAG" {
  default = "latest"
}

target "python" {
  dockerfile = "images/Dockerfile.python"
}

target "builder" {
  dockerfile = "images/Dockerfile.builder"
  target = "builder"
  contexts = {
    python = "target:python"
  }
}

target "builder-test" {
  inherits = ["builder"]
  target = "builder-test"
}

target "runtime" {
  dockerfile = "images/Dockerfile.runtime"
  contexts = {
    builder = "target:builder"
    python = "target:python"
  }
  tags = ["tjur-forum:${IMAGE_TAG}"]
}

target "runtime-test" {
  dockerfile = "images/Dockerfile.runtime"
  contexts = {
    builder = "target:builder-test"
    python = "target:python"
  }
  tags = ["tjur-forum:${IMAGE_TAG}-test"]
}
