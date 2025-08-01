#!/bin/bash

# Database Backup Script for Expert Connect
# Usage: ./backup_database.sh

# Set variables
BACKUP_DIR="backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DB_FILE="expert_connect/db.sqlite3"
SQLITE_BACKUP="$BACKUP_DIR/db_backup_$TIMESTAMP.sqlite3"
JSON_BACKUP="$BACKUP_DIR/data_backup_$TIMESTAMP.json"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

echo "Creating database backup..."
echo "Timestamp: $TIMESTAMP"

# Create SQLite backup
if [ -f "$DB_FILE" ]; then
    cp "$DB_FILE" "$SQLITE_BACKUP"
    echo "✅ SQLite backup created: $SQLITE_BACKUP"
else
    echo "❌ Database file not found: $DB_FILE"
    exit 1
fi

# Create JSON data backup
echo "Creating JSON data backup..."
python3 expert_connect/manage.py dumpdata --indent=2 > "$JSON_BACKUP"
if [ $? -eq 0 ]; then
    echo "✅ JSON backup created: $JSON_BACKUP"
else
    echo "❌ Failed to create JSON backup"
fi

# Show backup summary
echo ""
echo "📊 Backup Summary:"
echo "=================="
ls -lh "$BACKUP_DIR"/*"$TIMESTAMP"*
echo ""
echo "🎉 Backup completed successfully!"
echo "📁 Backup location: $BACKUP_DIR/" 