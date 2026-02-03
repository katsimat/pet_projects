package configs

import (
	"encoding/json"
	"os"
	"sync"
	"time"
)

type LoggingConfig struct {
	Level    string `json:"level"`
	FilePath string `json:"file_path"`
}

type DatabaseConfig struct {
	Host           string `json:"host"`
	Port           int    `json:"port"`
	DBName         string `json:"dbname"`
	SSLMode        string `json:"sslmode"`
	ConnectTimeout int    `json:"connect_timeout"`
}

type CredsConfig struct {
	Database struct {
		User     string `json:"user"`
		Password string `json:"password"`
	} `json:"database"`
	Auth struct {
		Secret string `json:"secret"`
	} `json:"auth"`
}

type ConfigManager struct {
	loggingConfig  *LoggingConfig
	databaseConfig *DatabaseConfig
	credsConfig    *CredsConfig
	mu             sync.RWMutex
	lastModified   time.Time
	reloadInterval time.Duration
	stopChan       chan struct{}
}

var (
	manager *ConfigManager
	once    sync.Once
)

func GetConfigManager() *ConfigManager {
	once.Do(func() {
		manager = &ConfigManager{
			loggingConfig:  &LoggingConfig{Level: "INFO"},
			databaseConfig: &DatabaseConfig{},
			credsConfig:    &CredsConfig{},
			reloadInterval: 5 * time.Second,
			stopChan:       make(chan struct{}),
		}
		manager.loadConfigs()
		go manager.watchConfigs()
	})
	return manager
}

func (cm *ConfigManager) GetLoggingConfig() LoggingConfig {
	cm.mu.RLock()
	defer cm.mu.RUnlock()
	return *cm.loggingConfig
}

func (cm *ConfigManager) GetDatabaseConfig() DatabaseConfig {
	cm.mu.RLock()
	defer cm.mu.RUnlock()
	return *cm.databaseConfig
}

func (cm *ConfigManager) GetCredsConfig() CredsConfig {
	cm.mu.RLock()
	defer cm.mu.RUnlock()
	return *cm.credsConfig
}

func (cm *ConfigManager) loadConfigs() {
	cm.mu.RLock()
	isFirstLoad := cm.lastModified.IsZero()
	cm.mu.RUnlock()

	var maxModTime time.Time

	modTime1 := cm.loadConfig("configs/logging.json", func(data []byte) error {
		var config LoggingConfig
		if err := json.Unmarshal(data, &config); err != nil {
			return err
		}
		cm.mu.Lock()
		cm.loggingConfig = &config
		cm.mu.Unlock()
		return nil
	})
	if !modTime1.IsZero() && modTime1.After(maxModTime) {
		maxModTime = modTime1
	}

	modTime2 := cm.loadConfig("configs/database.json", func(data []byte) error {
		var config DatabaseConfig
		if err := json.Unmarshal(data, &config); err != nil {
			return err
		}
		cm.mu.Lock()
		cm.databaseConfig = &config
		cm.mu.Unlock()
		return nil
	})
	if !modTime2.IsZero() && modTime2.After(maxModTime) {
		maxModTime = modTime2
	}

	modTime3 := cm.loadConfig("configs/creds.json", func(data []byte) error {
		var config CredsConfig
		if err := json.Unmarshal(data, &config); err != nil {
			return err
		}
		cm.mu.Lock()
		cm.credsConfig = &config
		cm.mu.Unlock()
		return nil
	})
	if !modTime3.IsZero() && modTime3.After(maxModTime) {
		maxModTime = modTime3
	}

	if isFirstLoad && !maxModTime.IsZero() {
		cm.mu.Lock()
		cm.lastModified = maxModTime
		cm.mu.Unlock()
	}
}

func (cm *ConfigManager) loadConfig(configPath string, apply func([]byte) error) time.Time {
	info, err := os.Stat(configPath)
	if err != nil {
		return time.Time{}
	}

	fileModTime := info.ModTime()

	cm.mu.RLock()
	isFirstLoad := cm.lastModified.IsZero()
	shouldLoad := isFirstLoad || fileModTime.After(cm.lastModified)
	cm.mu.RUnlock()

	if !shouldLoad {
		return time.Time{}
	}

	data, err := os.ReadFile(configPath)
	if err != nil {
		return time.Time{}
	}

	if err := apply(data); err != nil {
		return time.Time{}
	}

	if !isFirstLoad {
		cm.mu.Lock()
		if fileModTime.After(cm.lastModified) {
			cm.lastModified = fileModTime
		}
		cm.mu.Unlock()
	}

	return fileModTime
}

func (cm *ConfigManager) watchConfigs() {
	ticker := time.NewTicker(cm.reloadInterval)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			cm.loadConfigs()
		case <-cm.stopChan:
			return
		}
	}
}

func (cm *ConfigManager) Stop() {
	close(cm.stopChan)
}
