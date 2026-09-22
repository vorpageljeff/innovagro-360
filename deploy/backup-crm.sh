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
# These snapshots are on the VPS. Maintain external copies separately.
