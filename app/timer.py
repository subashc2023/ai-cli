"""Timer utility module."""

import time
from rich.table import Table
from typing import Dict, Optional, Tuple

class Timer:
    """A simple timer class for measuring operation timings."""

    def __init__(self):
        """Initialize Timer."""
        self.start_time: Optional[float] = None
        self.splits: Dict[str, float] = {}
        self.cumulative_time: float = 0

    def start(self) -> 'Timer':
        """Start the timer."""
        self.start_time = time.time()
        return self

    def split(self, name: str) -> 'Timer':
        """Record a split time."""
        if self.start_time is None:
            raise RuntimeError("Timer not started")
        elapsed_time = time.time() - self.start_time
        self.splits[name] = elapsed_time
        return self

    def get_table(self) -> Table:
        """Get timing data as a rich table."""
        table = Table(title="Operation Timing")
        table.add_column("Operation", style="cyan")
        table.add_column("Duration (seconds)", justify="right", style="green")
        table.add_column("Cumulative (seconds)", justify="right", style="magenta")

        previous_time = 0.0
        cumulative_time = 0.0
        for name, total_time in sorted(self.splits.items(), key=lambda x: x[1]):
            duration = total_time - previous_time
            cumulative_time = total_time
            table.add_row(name, f"{duration:.3f}", f"{cumulative_time:.3f}")
            previous_time = total_time
        return table 