"""Bounded VPN-rotation policy for recovering from IP/geo failures (e.g. 403).

Kept VPN-agnostic: the runner invokes an arbitrary ``cmd`` (a WireGuard rotation
script, a VPNGate fetcher, anything) when an item fails with a configured error
code, then re-queues that item. Rotation is deliberately *bounded* — a phase-wide
budget plus a per-item cap — because hammering a service through rapid IP hops
tends to make flagging worse, not better.
"""
from dataclasses import dataclass, field
from typing import Optional, Set
import shlex
import subprocess


@dataclass
class RotatePolicy:
    cmd: Optional[str] = None
    codes: Set[int] = field(default_factory=lambda: {403})
    max_rotations: int = 3          # phase-wide budget
    cooldown: float = 25.0          # seconds to wait after rotating, before retry
    max_item_requeues: int = 2      # cap re-tries of any single item

    @property
    def enabled(self):
        return bool(self.cmd) and self.max_rotations > 0


def should_rotate(policy, error_code, rotations_used, item_requeues):
    """Rotate iff enabled, the code is one we rotate on, and both budgets remain."""
    if not policy.enabled:
        return False
    if error_code not in policy.codes:
        return False
    if rotations_used >= policy.max_rotations:
        return False
    if item_requeues >= policy.max_item_requeues:
        return False
    return True


def _to_argv(cmd):
    """Turn a command (string or list) into an argv list, preserving quoted
    paths that contain spaces. shell=True mangled such paths, so we tokenize
    ourselves (Windows-style: keep backslashes literal, strip surrounding quotes)
    and run without a shell."""
    if isinstance(cmd, (list, tuple)):
        return list(cmd)
    return [tok.strip('"') for tok in shlex.split(cmd, posix=False)]


def run_rotate_command(cmd, timeout=120):
    """Run the user's rotation command (no shell) and return (ok, output)."""
    try:
        proc = subprocess.run(_to_argv(cmd), shell=False, capture_output=True,
                              text=True, timeout=timeout)
        out = (proc.stdout or "") + (proc.stderr or "")
        return proc.returncode == 0, out.strip()
    except subprocess.TimeoutExpired:
        return False, f"rotation command timed out after {timeout}s"
    except Exception as e:  # pragma: no cover - defensive
        return False, str(e)
