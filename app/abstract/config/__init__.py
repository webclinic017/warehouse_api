"""Global configuration"""
import os


def get_app_settings() -> str:
    """Returns the app setting environment"""
    return os.environ.get('APP_SETTINGS', 'development')


def is_testing() -> bool:
    """Returns boolean to check if this is testing environment"""
    return get_app_settings().strip().lower() == 'testing'


def is_production() -> bool:
    """Returns boolean to check if this is production environment"""
    return get_app_settings().strip().lower() == 'production'
