from modules.password_analyzer.analyzer import run as password_analyzer
from modules.hash_tool.hasher import run as hash_generator
from modules.system_info.info import run as system_information
from modules.url_analyzer.analyzer import run as url_analyzer
from modules.security_headers.checker import run as security_header_checker
from modules.metadata_analyzer.analyzer import run as metadata_analyzer
from modules.log_analyzer.analyzer import run as log_analyzer
from modules.report_manager.manager import run as reports_manager
from modules.health_check.checker import run as health_check
from modules.settings.manager import run as settings_manager


COMMANDS = {
    "1": ("Password Analyzer", password_analyzer),
    "2": ("Hash Generator", hash_generator),
    "3": ("System Information", system_information),
    "4": ("URL Analyzer", url_analyzer),
    "5": ("Security Header Checker", security_header_checker),
    "6": ("File Metadata Analyzer", metadata_analyzer),
    "7": ("Log Analyzer", log_analyzer),
    "8": ("Reports Manager", reports_manager),
    "9": ("Health Check", health_check),
    "10": ("Settings", settings_manager),
}
