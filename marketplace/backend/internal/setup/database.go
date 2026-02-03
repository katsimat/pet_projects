package setup

import (
	"fmt"

	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq"

	"github.com/katsimat/backend/internal/configs"
)

func ConnectDatabase() (*sqlx.DB, error) {
	configMgr := configs.GetConfigManager()
	dbConfig := configMgr.GetDatabaseConfig()
	creds := configMgr.GetCredsConfig()

	dsn := fmt.Sprintf(
		"host=%s port=%d dbname=%s user=%s password=%s sslmode=%s connect_timeout=%d",
		dbConfig.Host,
		dbConfig.Port,
		dbConfig.DBName,
		creds.Database.User,
		creds.Database.Password,
		dbConfig.SSLMode,
		dbConfig.ConnectTimeout,
	)

	db, err := sqlx.Connect("postgres", dsn)
	if err != nil {
		return nil, fmt.Errorf("failed to open database: %w", err)
	}

	if err := db.Ping(); err != nil {
		return nil, fmt.Errorf("failed to ping database: %w", err)
	}

	return db, nil
}
