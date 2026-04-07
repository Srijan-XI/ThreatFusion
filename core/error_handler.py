#!/usr/bin/env python3
"""
ThreatFusion Error Handling and Recovery System
Provides robust error handling with graceful degradation
"""

import functools
import traceback
import sys
from typing import Callable, Any, Optional, Type, Tuple, Dict, List
from pathlib import Path
import json
from datetime import datetime

# Import logger if available
try:
    from core.logger import get_logger
    LOGGER_AVAILABLE = True
except ImportError:
    LOGGER_AVAILABLE = False


class ThreatFusionError(Exception):
    """Base exception for ThreatFusion"""
    pass


class ScannerError(ThreatFusionError):
    """Error during scanning operations"""
    pass


class ParserError(ThreatFusionError):
    """Error during file parsing"""
    pass


class ReportError(ThreatFusionError):
    """Error during report generation"""
    pass


class ConfigurationError(ThreatFusionError):
    """Error in configuration"""
    pass


class NetworkError(ThreatFusionError):
    """Error in network operations"""
    pass


class ErrorHandler:
    """
    Centralized error handling system
    """
    
    def __init__(self, error_log_dir: str = "outputs/logs/errors"):
        self.error_log_dir = Path(error_log_dir)
        self.error_log_dir.mkdir(parents=True, exist_ok=True)
        self.error_count = 0
        self.errors: List[Dict[str, Any]] = []
        
        if LOGGER_AVAILABLE:
            self.logger = get_logger()
        else:
            self.logger = None
    
    def log_error(self, error: Exception, context: Optional[Dict[str, Any]] = None, fatal: bool = False):
        """
        Log an error with context information
        
        Args:
            error: The exception that occurred
            context: Additional context information
            fatal: Whether this is a fatal error
        """
        self.error_count += 1
        
        error_data = {
            'timestamp': datetime.now().isoformat(),
            'error_number': self.error_count,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': ''.join(traceback.format_exception(type(error), error, error.__traceback__)),
            'context': context or {},
            'fatal': fatal
        }
        
        self.errors.append(error_data)
        
        # Log to file
        self._write_error_to_file(error_data)
        
        # Log using logger if available
        if self.logger:
            if fatal:
                self.logger.critical(
                    f"FATAL ERROR: {type(error).__name__}: {str(error)}",
                    exc_info=True,
                    context=context
                )
            else:
                self.logger.error(
                    f"{type(error).__name__}: {str(error)}",
                    exc_info=True,
                    context=context
                )
        else:
            # Fallback to print
            print(f"[ERROR] {type(error).__name__}: {str(error)}", file=sys.stderr)
            if fatal:
                print("[FATAL] Application cannot continue", file=sys.stderr)
    
    def _write_error_to_file(self, error_data: Dict[str, Any]):
        """Write error to JSON file"""
        error_file = self.error_log_dir / f"error_{datetime.now().strftime('%Y%m%d')}.json"
        
        try:
            # Read existing errors
            if error_file.exists():
                with open(error_file, 'r', encoding='utf-8') as f:
                    existing_errors = json.load(f)
            else:
                existing_errors = []
            
            # Append new error
            existing_errors.append(error_data)
            
            # Write back
            with open(error_file, 'w', encoding='utf-8') as f:
                json.dump(existing_errors, f, indent=2)
        
        except Exception as e:
            print(f"[ERROR] Failed to write error log: {e}", file=sys.stderr)
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of errors"""
        error_types = {}
        for error in self.errors:
            error_type = error['error_type']
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        return {
            'total_errors': self.error_count,
            'error_types': error_types,
            'fatal_errors': sum(1 for e in self.errors if e.get('fatal', False))
        }
    
    def clear_errors(self):
        """Clear error history"""
        self.errors.clear()
        self.error_count = 0


# Global error handler instance
_global_error_handler: Optional[ErrorHandler] = None


def get_error_handler() -> ErrorHandler:
    """Get or create global error handler"""
    global _global_error_handler
    if _global_error_handler is None:
        _global_error_handler = ErrorHandler()
    return _global_error_handler


def handle_errors(
    default_return: Any = None,
    raise_on_error: bool = False,
    log_error: bool = True,
    error_types: Tuple[Type[Exception], ...] = (Exception,)
):
    """
    Decorator for handling errors in functions
    
    Args:
        default_return: Value to return on error
        raise_on_error: Whether to re-raise the exception
        log_error: Whether to log the error
        error_types: Tuple of exception types to catch
    
    Example:
        @handle_errors(default_return=[], log_error=True)
        def risky_function():
            # code that might fail
            pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except error_types as e:
                if log_error:
                    error_handler = get_error_handler()
                    context = {
                        'function': func.__name__,
                        'module': func.__module__,
                        'args': str(args)[:100],  # Limit length
                        'kwargs': str(kwargs)[:100]
                    }
                    error_handler.log_error(e, context=context)
                
                if raise_on_error:
                    raise
                
                return default_return
        
        return wrapper
    return decorator


def safe_execute(
    func: Callable,
    *args,
    default_return: Any = None,
    error_message: str = None,
    **kwargs
) -> Any:
    """
    Safely execute a function with error handling
    
    Args:
        func: Function to execute
        *args: Positional arguments for the function
        default_return: Value to return on error
        error_message: Custom error message
        **kwargs: Keyword arguments for the function
    
    Returns:
        Function result or default_return on error
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        error_handler = get_error_handler()
        context = {
            'function': func.__name__,
            'custom_message': error_message
        }
        error_handler.log_error(e, context=context)
        
        if error_message:
            print(f"[ERROR] {error_message}: {str(e)}", file=sys.stderr)
        
        return default_return


class ErrorRecovery:
    """
    Provides error recovery strategies
    """
    
    @staticmethod
    def retry_on_failure(
        func: Callable,
        max_retries: int = 3,
        delay: float = 1.0,
        backoff: float = 2.0,
        exceptions: Tuple[Type[Exception], ...] = (Exception,)
    ) -> Callable:
        """
        Decorator to retry function on failure
        
        Args:
            func: Function to retry
            max_retries: Maximum number of retries
            delay: Initial delay between retries (seconds)
            backoff: Multiplier for delay after each retry
            exceptions: Tuple of exceptions to catch
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import time
            
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt < max_retries:
                        if LOGGER_AVAILABLE:
                            logger = get_logger()
                            logger.warning(
                                f"Attempt {attempt + 1}/{max_retries} failed for {func.__name__}: {str(e)}. "
                                f"Retrying in {current_delay}s..."
                            )
                        else:
                            print(f"[RETRY] Attempt {attempt + 1} failed. Retrying in {current_delay}s...")
                        
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        # Final attempt failed
                        error_handler = get_error_handler()
                        error_handler.log_error(
                            e,
                            context={
                                'function': func.__name__,
                                'attempts': max_retries + 1,
                                'final_failure': True
                            }
                        )
                        raise
            
            # Should never reach here, but just in case
            if last_exception:
                raise last_exception
        
        return wrapper
    
    @staticmethod
    def fallback_on_error(primary_func: Callable, fallback_func: Callable) -> Callable:
        """
        Decorator to use fallback function if primary fails
        
        Args:
            primary_func: Primary function to try
            fallback_func: Fallback function to use on error
        """
        @functools.wraps(primary_func)
        def wrapper(*args, **kwargs):
            try:
                return primary_func(*args, **kwargs)
            except Exception as e:
                if LOGGER_AVAILABLE:
                    logger = get_logger()
                    logger.warning(
                        f"Primary function {primary_func.__name__} failed: {str(e)}. "
                        f"Using fallback {fallback_func.__name__}"
                    )
                else:
                    print(f"[FALLBACK] Using {fallback_func.__name__} due to error in {primary_func.__name__}")
                
                return fallback_func(*args, **kwargs)
        
        return wrapper


class GracefulDegradation:
    """
    Implements graceful degradation strategies
    """
    
    @staticmethod
    def with_feature_flag(feature_name: str, default_value: Any = None):
        """
        Decorator to disable feature if it fails
        
        Args:
            feature_name: Name of the feature
            default_value: Value to return if feature is disabled
        """
        disabled_features = set()
        
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if feature_name in disabled_features:
                    if LOGGER_AVAILABLE:
                        logger = get_logger()
                        logger.debug(f"Feature {feature_name} is disabled, returning default value")
                    return default_value
                
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    disabled_features.add(feature_name)
                    
                    if LOGGER_AVAILABLE:
                        logger = get_logger()
                        logger.error(
                            f"Feature {feature_name} failed and has been disabled: {str(e)}",
                            exc_info=True
                        )
                    else:
                        print(f"[DEGRADED] Feature {feature_name} disabled due to error")
                    
                    error_handler = get_error_handler()
                    error_handler.log_error(
                        e,
                        context={'feature': feature_name, 'degraded': True}
                    )
                    
                    return default_value
            
            return wrapper
        return decorator


# Convenience functions
def log_error(error: Exception, context: dict = None, fatal: bool = False):
    """Log an error using global error handler"""
    get_error_handler().log_error(error, context, fatal)


def get_error_summary() -> dict:
    """Get error summary from global error handler"""
    return get_error_handler().get_error_summary()


if __name__ == "__main__":
    # Test error handling
    print("Testing ThreatFusion Error Handling System\n")
    
    # Test basic error logging
    @handle_errors(default_return="Error occurred", log_error=True)
    def test_function():
        raise ValueError("Test error")
    
    result = test_function()
    print(f"Result: {result}\n")
    
    # Test retry mechanism
    class Counter:
        def __init__(self):
            self.attempt_count = 0
    
    counter = Counter()
    
    @ErrorRecovery.retry_on_failure(max_retries=3, delay=0.1)
    def flaky_function():
        counter.attempt_count += 1
        if counter.attempt_count < 3:
            raise ConnectionError("Temporary failure")
        return "Success!"
    
    try:
        result = flaky_function()
        print(f"Retry test result: {result}\n")
    except Exception as e:
        print(f"Retry test failed: {e}\n")
    
    # Test graceful degradation
    @GracefulDegradation.with_feature_flag("test_feature", default_value="Feature disabled")
    def experimental_feature():
        raise NotImplementedError("Feature not ready")
    
    result1 = experimental_feature()
    result2 = experimental_feature()  # Should return default immediately
    print(f"Degradation test: {result1}, {result2}\n")
    
    # Print error summary
    summary = get_error_summary()
    print(f"Error Summary: {summary}")
    
    print("\n[+] Error handling test completed!")
