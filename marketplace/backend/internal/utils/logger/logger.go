package logger

import (
	"context"
	"fmt"
	"log"
	"os"
	"sync"
	"time"

	"github.com/katsimat/backend/internal/configs"
)

type Level int

const (
	LevelDebug Level = iota
	LevelInfo
	LevelWarn
	LevelError
)

const (
	levelDebug = "DEBUG"
	levelInfo  = "INFO"
	levelWarn  = "WARN"
	levelError = "ERROR"

	timestampFormat = "2006-01-02 15:04:05.000"
	TraceIDKey      = "trace_id"
)

var (
	currentLevel = LevelInfo
	logger       = log.New(os.Stdout, "", 0)
	logFile      *os.File
	mu           sync.RWMutex
	configMgr    *configs.ConfigManager
)

func init() {
	configMgr = configs.GetConfigManager()
}

func getCurrentLevel() Level {
	mu.RLock()
	defer mu.RUnlock()
	return currentLevel
}

func updateLevelFromConfig() {
	cfg := configMgr.GetLoggingConfig()
	mu.Lock()
	defer mu.Unlock()

	switch cfg.Level {
	case levelDebug:
		currentLevel = LevelDebug
	case levelInfo:
		currentLevel = LevelInfo
	case levelWarn:
		currentLevel = LevelWarn
	case levelError:
		currentLevel = LevelError
	default:
		currentLevel = LevelInfo
	}
}

func SetLevel(level Level) {
	mu.Lock()
	defer mu.Unlock()
	currentLevel = level
}

func Debug(ctx context.Context, message string) {
	updateLevelFromConfig()
	if getCurrentLevel() <= LevelDebug {
		logMessage(levelDebug, getTraceIDFromContext(ctx), message)
	}
}

func Debugf(ctx context.Context, format string, v ...any) {
	updateLevelFromConfig()
	if getCurrentLevel() <= LevelDebug {
		message := fmt.Sprintf(format, v...)
		logMessage(levelDebug, getTraceIDFromContext(ctx), message)
	}
}

func Info(ctx context.Context, message string) {
	updateLevelFromConfig()
	if getCurrentLevel() <= LevelInfo {
		logMessage(levelInfo, getTraceIDFromContext(ctx), message)
	}
}

func Infof(ctx context.Context, format string, v ...any) {
	updateLevelFromConfig()
	if getCurrentLevel() <= LevelInfo {
		message := fmt.Sprintf(format, v...)
		logMessage(levelInfo, getTraceIDFromContext(ctx), message)
	}
}

func Warn(ctx context.Context, message string) {
	updateLevelFromConfig()
	if getCurrentLevel() <= LevelWarn {
		logMessage(levelWarn, getTraceIDFromContext(ctx), message)
	}
}

func Warnf(ctx context.Context, format string, v ...any) {
	updateLevelFromConfig()
	if getCurrentLevel() <= LevelWarn {
		message := fmt.Sprintf(format, v...)
		logMessage(levelWarn, getTraceIDFromContext(ctx), message)
	}
}

func Error(ctx context.Context, message string) {
	updateLevelFromConfig()
	if getCurrentLevel() <= LevelError {
		logMessage(levelError, getTraceIDFromContext(ctx), message)
	}
}

func Errorf(ctx context.Context, format string, v ...any) {
	updateLevelFromConfig()
	if getCurrentLevel() <= LevelError {
		message := fmt.Sprintf(format, v...)
		logMessage(levelError, getTraceIDFromContext(ctx), message)
	}
}

func getTraceIDFromContext(ctx context.Context) string {
	if ctx == nil {
		return ""
	}
	if traceID, ok := ctx.Value(TraceIDKey).(string); ok {
		return traceID
	}
	return ""
}

func logMessage(level string, traceID string, message string) {
	cfg := configMgr.GetLoggingConfig()

	mu.Lock()
	defer mu.Unlock()

	if cfg.FilePath != "" && (logFile == nil || logFile.Name() != cfg.FilePath) {
		if logFile != nil && logFile != os.Stdout {
			logFile.Close()
		}

		if err := os.MkdirAll("logs", 0755); err == nil {
			if file, err := os.OpenFile(cfg.FilePath, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666); err == nil {
				logFile = file
				logger = log.New(logFile, "", 0)
			} else {
				logFile = os.Stdout
				logger = log.New(os.Stdout, "", 0)
			}
		} else {
			logFile = os.Stdout
			logger = log.New(os.Stdout, "", 0)
		}
	} else if cfg.FilePath == "" && logFile != os.Stdout {
		if logFile != nil {
			logFile.Close()
		}
		logFile = os.Stdout
		logger = log.New(os.Stdout, "", 0)
	}

	timestamp := time.Now().Format(timestampFormat)
	if traceID != "" {
		logger.Printf("[%s] [%s] [%s] %s", timestamp, level, traceID, message)
	} else {
		logger.Printf("[%s] [%s] %s", timestamp, level, message)
	}
}
