from src.measurer.measurers.cyclomatic_complexity import CyclomaticComplexityMeasurer
from src.measurer.measurers.filesize import FileSizeMeasurer

measurers = [
    FileSizeMeasurer(),
    CyclomaticComplexityMeasurer(),
]
