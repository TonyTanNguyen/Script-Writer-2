"""Tests for the VPN rotation policy (pure decision logic)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from pathlib import Path

from glabs.rotate import RotatePolicy, should_rotate, _to_argv
from glabs import generate_media as gm
from glabs.manifest import Manifest


def _policy(**kw):
    base = dict(cmd="rotate.ps1", codes={403}, max_rotations=3, cooldown=25, max_item_requeues=2)
    base.update(kw)
    return RotatePolicy(**base)


def test_policy_enabled_when_cmd_and_budget():
    assert _policy().enabled is True


def test_policy_disabled_without_cmd():
    assert _policy(cmd=None).enabled is False
    assert _policy(cmd="").enabled is False


def test_policy_disabled_with_zero_rotations():
    assert _policy(max_rotations=0).enabled is False


def test_should_rotate_true_on_matching_code_within_budget():
    assert should_rotate(_policy(), error_code=403, rotations_used=0, item_requeues=0) is True


def test_should_rotate_false_on_unlisted_code():
    assert should_rotate(_policy(), error_code=429, rotations_used=0, item_requeues=0) is False
    assert should_rotate(_policy(), error_code=500, rotations_used=0, item_requeues=0) is False


def test_should_rotate_false_when_phase_budget_exhausted():
    assert should_rotate(_policy(max_rotations=3), error_code=403,
                         rotations_used=3, item_requeues=0) is False


def test_should_rotate_false_when_item_requeue_cap_hit():
    assert should_rotate(_policy(max_item_requeues=2), error_code=403,
                         rotations_used=0, item_requeues=2) is False


def test_should_rotate_false_when_disabled():
    assert should_rotate(_policy(cmd=None), error_code=403,
                         rotations_used=0, item_requeues=0) is False


def test_codes_configurable():
    p = _policy(codes={403, 500})
    assert should_rotate(p, error_code=500, rotations_used=0, item_requeues=0) is True


# --- run_phase rotation wiring (fake client, no network / no real VPN) -------

_FAILED_403 = {"status": "failed", "error_code": 403, "error": "PERMISSION DENIED",
               "error_detail": "403"}
_DONE = {"status": "completed", "results": ["http://x/api/files/img.png"]}


class FakeClient:
    """Scripts statuses per prompt; attempt counter persists across resubmits."""
    def __init__(self, scripts):
        self.scripts = scripts
        self.attempts = {}
        self.submits = []
        self._n = 0
        self._tid_body = {}

    def submit(self, endpoint, body):
        self._n += 1
        tid = f"t{self._n}"
        self._tid_body[tid] = body
        self.submits.append(body["prompt"])
        return {"task_id": tid}

    def status(self, tid):
        prompt = self._tid_body[tid]["prompt"]
        i = self.attempts.get(prompt, 0)
        self.attempts[prompt] = i + 1
        seq = self.scripts[prompt]
        return seq[min(i, len(seq) - 1)]

    def download(self, url, dest):
        Path(dest).parent.mkdir(parents=True, exist_ok=True)
        Path(dest).write_bytes(b"img")


def _item(tmp_path, prompt="P1"):
    return gm.Item(item_id="scene:001",
                   body={"prompt": prompt, "model": "nano_banana_2", "aspect_ratio": "16:9"},
                   dest_stem=tmp_path / "scenes" / "scene-001")


def _run(tmp_path, client, policy, rotate_calls):
    m = Manifest(tmp_path / "manifest.json")
    gm.run_phase("scenes", [_item(tmp_path)], client, m, tmp_path,
                 poll_interval=0, rotate_policy=policy,
                 rotate_fn=lambda cmd: (rotate_calls.append(cmd) or (True, "switched")),
                 sleep_fn=lambda s: None, log=lambda *a: None)
    return m


def test_rotation_recovers_a_403(tmp_path):
    client = FakeClient({"P1": [_FAILED_403, _DONE]})
    calls = []
    m = _run(tmp_path, client, _policy(cmd="rot", max_rotations=1), calls)
    assert calls == ["rot"]                       # rotated once
    assert client.submits == ["P1", "P1"]         # resubmitted after rotating
    assert m.status_of("scene:001") == "completed"
    assert (tmp_path / "scenes" / "scene-001.png").exists()


def test_no_rotation_when_disabled_marks_failed(tmp_path):
    client = FakeClient({"P1": [_FAILED_403]})
    calls = []
    m = _run(tmp_path, client, RotatePolicy(), calls)   # cmd=None -> disabled
    assert calls == []
    assert client.submits == ["P1"]
    assert m.status_of("scene:001") == "failed"


def test_rotation_budget_exhausted_then_fails(tmp_path):
    client = FakeClient({"P1": [_FAILED_403, _FAILED_403]})  # still fails after rotating
    calls = []
    m = _run(tmp_path, client, _policy(cmd="rot", max_rotations=1), calls)
    assert calls == ["rot"]                       # rotated once, budget then spent
    assert client.submits == ["P1", "P1"]
    assert m.status_of("scene:001") == "failed"


# --- build_rotate_policy (CLI > file > default) -----------------------------

class _Args:
    def __init__(self, **kw):
        for k in ("rotate_cmd", "rotate_on", "max_rotations", "rotate_cooldown"):
            setattr(self, k, kw.get(k))


def test_build_policy_from_file_when_no_cli():
    p = gm.build_rotate_policy(_Args(), {"rotate_cmd": "x.ps1", "rotate_on_codes": [403, 500],
                                         "max_rotations": 5, "rotate_cooldown": 30})
    assert p.cmd == "x.ps1" and p.codes == {403, 500}
    assert p.max_rotations == 5 and p.cooldown == 30


def test_build_policy_cli_overrides_file():
    p = gm.build_rotate_policy(_Args(rotate_cmd="cli.ps1", rotate_on="429", max_rotations=1),
                               {"rotate_cmd": "file.ps1", "rotate_on_codes": [403]})
    assert p.cmd == "cli.ps1" and p.codes == {429} and p.max_rotations == 1


def test_build_policy_defaults_when_nothing_set():
    p = gm.build_rotate_policy(_Args(), {})
    assert p.cmd is None and p.codes == {403} and p.enabled is False


# --- _to_argv: quoted paths with spaces survive (the PathCommand bug) --------

def test_to_argv_preserves_spaced_quoted_path():
    cmd = 'powershell -ExecutionPolicy Bypass -File "D:\\Viet kich ban Ver 2\\tools\\rotate-vpn.ps1"'
    argv = _to_argv(cmd)
    assert argv == ['powershell', '-ExecutionPolicy', 'Bypass', '-File',
                    'D:\\Viet kich ban Ver 2\\tools\\rotate-vpn.ps1']


def test_to_argv_passthrough_list():
    assert _to_argv(['a', 'b c']) == ['a', 'b c']
