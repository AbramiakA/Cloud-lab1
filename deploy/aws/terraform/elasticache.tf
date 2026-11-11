resource "aws_elasticache_subnet_group" "redis" { #приватні підмережі для Redis
  name       = "${var.project}-redis-subnets"
  subnet_ids = module.vpc.private_subnets
}

resource "aws_elasticache_replication_group" "redis" { #створ редіс
  replication_group_id = "${var.project}-redis"
  description          = "Redis cache for ${var.project}"

  engine         = "redis"
  engine_version = "7.1"
  node_type      = "cache.t4g.micro"
  port           = 6379

  num_cache_clusters         = 1
  automatic_failover_enabled = false
  multi_az_enabled           = false

  subnet_group_name  = aws_elasticache_subnet_group.redis.name
  security_group_ids = [aws_security_group.redis.id]

  transit_encryption_enabled = true
  at_rest_encryption_enabled = true

  snapshot_retention_limit = 0
}
