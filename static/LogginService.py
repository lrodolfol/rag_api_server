import logging
import logging.handlers
import os
from datetime import datetime
from typing import Optional

class LoggerService:
    def __init__(self, name: str, log_level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self._setup_logger(log_level)

    def _setup_logger(self, log_level: str):
        # Definir nível de log
        level = getattr(logging, log_level.upper(), logging.INFO)
        self.logger.setLevel(level)

        # Evitar duplicação de handlers
        if self.logger.handlers:
            return

        # Formato personalizado
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)

        # Handler para arquivo com rotação
        if not os.path.exists('logs'):
            os.makedirs('logs')

        file_handler = logging.handlers.RotatingFileHandler(
            'logs/application.log',
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)

        # Handler para erros críticos
        error_handler = logging.handlers.RotatingFileHandler(
            'logs/errors.log',
            maxBytes=5 * 1024 * 1024,  # 5MB
            backupCount=3
        )
        error_handler.setFormatter(formatter)
        error_handler.setLevel(logging.ERROR)

        # Adicionar handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(error_handler)

    def debug(self, message: str, *args, **kwargs):
        """Log de debug - informações detalhadas"""
        self.logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        """Log informativo - fluxo normal da aplicação"""
        self.logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        """Log de aviso - situações que merecem atenção"""
        self.logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs):
        """Log de erro - erros que não param a aplicação"""
        self.logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs):
        """Log crítico - erros graves que podem parar a aplicação"""
        self.logger.critical(message, *args, **kwargs)

    def exception(self, message: str, *args, **kwargs):
        """Log de exceção - inclui stack trace"""
        self.logger.exception(message, *args, **kwargs)

    def log_execution_time(self, func_name: str, execution_time: float):
        """Log do tempo de execução de uma função"""
        self.info(f"Função '{func_name}' executada em {execution_time:.4f}s")


# Decorator para logging automático
def log_function_calls(logger_service: LoggerService):
    """Decorator para logar entrada e saída de funções"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            logger_service.debug(f"Iniciando execução: {func.__name__}")

            try:
                start_time = datetime.now()
                result = func(*args, **kwargs)
                end_time = datetime.now()

                execution_time = (end_time - start_time).total_seconds()
                logger_service.log_execution_time(func.__name__, execution_time)
                logger_service.debug(f"Finalizada execução: {func.__name__}")

                return result

            except Exception as e:
                logger_service.exception(f"Erro na função {func.__name__}: {e}")
                raise

        return wrapper

    return decorator