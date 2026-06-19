import logging

logger = logging.getLogger(__name__)


def read_credentials(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 2:
                return lines[0].strip(), lines[1].strip()
            else:
                logger.error("File '%s' does not contain enough lines.", file_path)
                return None, None
    except FileNotFoundError:
        logger.error("File '%s' not found.", file_path)
        return None, None
    except Exception as e:
        logger.error("Error reading credentials from %s: %s", file_path, e)
        return None, None


def read_paths_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except Exception as e:
        logger.error("Error reading paths from %s: %s", file_path, e)
        return []
