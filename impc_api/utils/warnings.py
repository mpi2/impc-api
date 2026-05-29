"""Module for warnings and excepton utils"""

import warnings
from typing import Optional, Type, Union


# Custom warnings
class InvalidCoreWarning(Warning):
    """Warning raised when the core is not in the expected core names"""


class InvalidFieldWarning(Warning):
    """Warning raised when the field name is not in the expected fields"""


class RowsParamIgnored(Warning):
    """Warning raised when the row param is ignored"""


class LargeRequestMemoryWarning(Warning):
    """Warning raised when user triggers a large request without downloading in batches"""


# custom exceptions
class UnsupportedDownloadFormatError(Exception):
    """Exception raised when the format is not supported for download"""


# Custom warning function
def warning_config() -> None:
    """Customises formatting and filters for warnings"""

    def custom_warning(
        message: Union[str, Warning],
        category: Type[Warning],
        filename: str,
        lineno: int,
        line: Optional[str] = None,
    ) -> str:
        return f"{category.__name__}: {message}\n"

    warnings.formatwarning = custom_warning
    warnings.simplefilter("always", Warning)
