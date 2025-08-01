# Database Backups

This directory contains database backups for the Expert Connect project.

## Backup Files

### SQLite Database Backup

- **File**: `db_backup_YYYYMMDD_HHMMSS.sqlite3`
- **Description**: Complete SQLite database file backup
- **Size**: ~217KB
- **Usage**: Direct copy replacement for `expert_connect/db.sqlite3`

### JSON Data Backup

- **File**: `data_backup_YYYYMMDD_HHMMSS.json`
- **Description**: Django data dump in JSON format
- **Size**: ~30KB
- **Usage**: Can be loaded using Django's `loaddata` command

## How to Restore

### Method 1: SQLite File Restore (Recommended)

```bash
# Stop the Django server first
# Copy the backup file to replace the current database
cp backups/db_backup_YYYYMMDD_HHMMSS.sqlite3 expert_connect/db.sqlite3
```

### Method 2: JSON Data Restore

```bash
# Make sure you have a fresh database with migrations applied
python3 expert_connect/manage.py migrate

# Load the JSON data
python3 expert_connect/manage.py loaddata backups/data_backup_YYYYMMDD_HHMMSS.json
```

## Backup Contents

The database contains:

- User accounts (experts and podcasters)
- Expert profiles with images
- Podcast profiles with images
- Likes, favorites, and comments
- Messages between users
- Featured profile settings

## Backup Date: August 1, 2025

This backup was created after implementing:

- ✅ Image upload functionality for profiles
- ✅ Search and category filtering
- ✅ Featured profiles system
- ✅ Likes and favorites system
- ✅ Messaging system
- ✅ Sample expert and podcast data

## Notes

- The SQLite backup is the most reliable for complete restoration
- The JSON backup is useful for data migration between different database types
- Always test backups in a development environment before production use
- Keep multiple backup versions for safety
