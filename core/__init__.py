"""
ThreatFusion Core Module
Provides logging, reporting, and error handling functionality
"""

from .logger import (
    ThreatFusionLogger,
    get_logger,
    setup_logging,
    debug,
    info,
    warning,
    error,
    critical,
    exception
)

from .error_handler import (
    ThreatFusionError,
    ScannerError,
    ParserError,
    ReportError,
    ConfigurationError,
    NetworkError,
    ErrorHandler,
    get_error_handler,
    handle_errors,
    safe_execute,
    ErrorRecovery,
    GracefulDegradation,
    log_error,
    get_error_summary
)

from .reporting import (
    PDFReport,
    HTMLReport,
    ExcelReport,
    CSVReport,
    ReportGenerator
)

__all__ = [
    # Logger
    'ThreatFusionLogger',
    'get_logger',
    'setup_logging',
    'debug',
    'info',
    'warning',
    'error',
    'critical',
    'exception',
    
    # Error Handling
    'ThreatFusionError',
    'ScannerError',
    'ParserError',
    'ReportError',
    'ConfigurationError',
    'NetworkError',
    'ErrorHandler',
    'get_error_handler',
    'handle_errors',
    'safe_execute',
    'ErrorRecovery',
    'GracefulDegradation',
    'log_error',
    'get_error_summary',
    
    # Reporting
    'PDFReport',
    'HTMLReport',
    'ExcelReport',
    'CSVReport',
    'ReportGenerator',
]

__version__ = '2.0.0'
