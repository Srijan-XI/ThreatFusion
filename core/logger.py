#!/usr/bin/env python3
"""
ThreatFusion Advanced Logging System
Provides structured logging with multiple levels and outputs
"""

import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import traceback
import sys

class ColoredFormatter(logging.Formatter):
    """Custom formatter with color support for console output"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        # Avoid leaking ANSI-modified level names into other handlers by restoring
        # the original value after console formatting.
        original_levelname = record.levelname
        if original_levelname in self.COLORS:
            record.levelname = f"{self.COLORS[original_levelname]}{original_levelname}{self.COLORS['RESET']}"

        try:
            return super().format(record)
        finally:
            record.levelname = original_levelname


class JSONFormatter(logging.Formatter):
    """Formatter that outputs logs in JSON format"""
    
    def format(self, record):
        log_data = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': traceback.format_exception(*record.exc_info)
            }
        
        # Add extra fields
        if hasattr(record, 'extra_data'):
            log_data['extra'] = record.extra_data
        
        # Ensure logging never fails when extra fields contain non-JSON-native values.
        return json.dumps(log_data, default=str)


class ThreatFusionLogger:
    """
    Advanced logging system for ThreatFusion
    Supports multiple outputs: console, file, JSON
    """
    
    def __init__(self, name: str = "ThreatFusion", log_dir: str = "outputs/logs"):
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        # Keep logs from being duplicated by parent/root handlers.
        self.logger.propagate = False
        
        # Remove existing handlers
        self.logger.handlers.clear()
        
        # Setup handlers
        self._setup_console_handler()
        self._setup_file_handler()
        self._setup_json_handler()
        self._setup_error_handler()
        
    def _setup_console_handler(self):
        """Setup colored console output"""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        formatter = ColoredFormatter(
            '[%(levelname)s] %(asctime)s - %(name)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def _setup_file_handler(self):
        """Setup text file logging"""
        log_file = self.log_dir / f"{self.name.lower()}_{datetime.now().strftime('%Y%m%d')}.log"
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '[%(levelname)s] %(asctime)s - %(name)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def _setup_json_handler(self):
        """Setup JSON structured logging"""
        json_file = self.log_dir / f"{self.name.lower()}_{datetime.now().strftime('%Y%m%d')}.json"
        
        json_handler = logging.FileHandler(json_file, encoding='utf-8')
        json_handler.setLevel(logging.DEBUG)
        json_handler.setFormatter(JSONFormatter())
        self.logger.addHandler(json_handler)
    
    def _setup_error_handler(self):
        """Setup separate error log file"""
        error_file = self.log_dir / f"{self.name.lower()}_errors_{datetime.now().strftime('%Y%m%d')}.log"
        
        error_handler = logging.FileHandler(error_file, encoding='utf-8')
        error_handler.setLevel(logging.ERROR)
        
        formatter = logging.Formatter(
            '[%(levelname)s] %(asctime)s - %(name)s\n'
            'Module: %(module)s | Function: %(funcName)s | Line: %(lineno)d\n'
            'Message: %(message)s\n'
            '%(exc_info)s\n' + '='*80 + '\n',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        error_handler.setFormatter(formatter)
        self.logger.addHandler(error_handler)
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self._log(logging.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        self._log(logging.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self._log(logging.WARNING, message, **kwargs)
    
    def error(self, message: str, exc_info: bool = False, **kwargs):
        """Log error message"""
        self._log(logging.ERROR, message, exc_info=exc_info, **kwargs)
    
    def critical(self, message: str, exc_info: bool = False, **kwargs):
        """Log critical message"""
        self._log(logging.CRITICAL, message, exc_info=exc_info, **kwargs)
    
    def exception(self, message: str, **kwargs):
        """Log exception with traceback"""
        self._log(logging.ERROR, message, exc_info=True, **kwargs)
    
    def _log(self, level: int, message: str, exc_info: bool = False, **kwargs):
        """Internal logging method"""
        extra = {'extra_data': kwargs} if kwargs else {}
        self.logger.log(level, message, exc_info=exc_info, extra=extra)
    
    def log_scan_start(self, scan_type: str, target: str):
        """Log scan start"""
        self.info(f"Starting {scan_type} scan", scan_type=scan_type, target=target)
    
    def log_scan_complete(self, scan_type: str, files_scanned: int, threats_found: int):
        """Log scan completion"""
        self.info(
            f"{scan_type} scan completed",
            scan_type=scan_type,
            files_scanned=files_scanned,
            threats_found=threats_found
        )
    
    def log_threat_detected(self, threat_type: str, file_path: str, severity: str, details: Dict[str, Any]):
        """Log threat detection"""
        self.warning(
            f"Threat detected: {threat_type}",
            threat_type=threat_type,
            file_path=file_path,
            severity=severity,
            details=details
        )
    
    def log_error_with_context(self, operation: str, error: Exception, context: Dict[str, Any]):
        """Log error with context information"""
        self.error(
            f"Error during {operation}: {str(error)}",
            exc_info=True,
            operation=operation,
            error_type=type(error).__name__,
            context=context
        )


# Global logger instance
_global_logger: Optional[ThreatFusionLogger] = None


def get_logger(name: str = "ThreatFusion") -> ThreatFusionLogger:
    """Get or create global logger instance"""
    global _global_logger
    if _global_logger is None:
        _global_logger = ThreatFusionLogger(name)
    return _global_logger


def setup_logging(name: str = "ThreatFusion", log_dir: str = "outputs/logs") -> ThreatFusionLogger:
    """Setup and return logger instance"""
    global _global_logger
    _global_logger = ThreatFusionLogger(name, log_dir)
    return _global_logger


# Convenience functions
def debug(message: str, **kwargs):
    """Log debug message using global logger"""
    get_logger().debug(message, **kwargs)


def info(message: str, **kwargs):
    """Log info message using global logger"""
    get_logger().info(message, **kwargs)


def warning(message: str, **kwargs):
    """Log warning message using global logger"""
    get_logger().warning(message, **kwargs)


def error(message: str, exc_info: bool = False, **kwargs):
    """Log error message using global logger"""
    get_logger().error(message, exc_info=exc_info, **kwargs)


def critical(message: str, exc_info: bool = False, **kwargs):
    """Log critical message using global logger"""
    get_logger().critical(message, exc_info=exc_info, **kwargs)


def exception(message: str, **kwargs):
    """Log exception using global logger"""
    get_logger().exception(message, **kwargs)


if __name__ == "__main__":
    # Test the logger
    logger = setup_logging("ThreatFusion_Test")
    
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    
    # Test exception logging
    try:
        raise ValueError("Test exception")
    except Exception as e:
        logger.exception("An exception occurred")
    
    # Test structured logging
    logger.log_threat_detected(
        threat_type="Malware",
        file_path="/path/to/file.exe",
        severity="HIGH",
        details={"hash": "abc123", "size": 1024}
    )
    
    print("\n[+] Logger test completed. Check outputs/logs/ for log files.")
