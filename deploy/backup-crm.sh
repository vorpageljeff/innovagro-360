#!/usr/bin/env bash
set -euo pipefail
umask 077
backup_dir=/opt/innovagro/backups/crm360
mkdir -p "$backup_dir"
exec 9>"$backup_dir/.lock"
flock -n 9 || exit 0
stamp=$(date -u +%Y%m%dT%H%M%SZ)
backup_file="$backup_dir/crm-$stamp.dump"
docker exec voragon-crm-db-1 pg_dump -U crm360 -d crm360 -Fc > "$backup_file.partial"
docker exec -i voragon-crm-db-1 pg_restore --list < "$backup_file.partial" > /dev/null
mv "$backup_file.partial" "$backup_file"
echo "Backup completed: $backup_file"
if docker inspect voragon-crm-evolution_db-1 >/dev/null 2>&1; then
  evolution_dump="$backup_dir/evolution-$stamp.dump"
  docker exec voragon-crm-evolution_db-1 sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' > "$evolution_dump.partial"
  docker exec -i voragon-crm-evolution_db-1 pg_restore --list < "$evolution_dump.partial" > /dev/null
  mv "$evolution_dump.partial" "$evolution_dump"
  evolution_instances="$backup_dir/evolution-instances-$stamp.tar.gz"
  docker exec voragon-crm-evolution-1 tar -czf - -C /evolution instances > "$evolution_instances.partial"
  tar -tzf "$evolution_instances.partial" > /dev/null
  mv "$evolution_instances.partial" "$evolution_instances"
  echo "Evolution database and instances backed up."
fi
# These snapshots are on the VPS. Maintain external copies separately.
