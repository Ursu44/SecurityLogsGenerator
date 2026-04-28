import random

def random_file_path():
    paths = [
        "/var/log/syslog",
        "/etc/hosts",
        "/usr/bin/python3",
        "/home/user1/.bashrc",
        "/opt/app/config.yaml",
        "/tmp/update.sh",          # fix: era link markdown
        "/tmp/.x",
        "/var/tmp/malware.bin",
        "/dev/shm/payload",
        "/root/.ssh/authorized_keys",
        "C:\\Windows\\System32\\notepad.exe",
        "C:\\Program Files\\App\\app.exe",
        "C:\\Users\\user1\\Documents\\report.docx",
        "C:\\Temp\\payload.exe",
        "C:\\Users\\Public\\svchost.exe",
        "C:\\Windows\\Temp\\dropper.exe",
        "C:\\Windows\\System32\\svchost.exe"
    ]
    return random.choice(paths)


def random_user():
    return random.choice(["root", "admin", "user1", "user2", "guest", "backup"])


def random_ip():
    private_ranges = [
        lambda: f"172.{random.randint(16,27)}.{random.randint(0,255)}.{random.randint(1,254)}",
        lambda: f"192.168.{random.randint(0,255)}.{random.randint(1,254)}"
    ]
    public_ranges = [
        lambda: f"31.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}",
        lambda: f"52.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
    ]
    return random.choice(private_ranges + public_ranges)()

_attack_wave = False
_wave_counter = 0
_WAVE_LENGTH = 8
_CALM_LENGTH = 15

def is_attack_wave():
    global _attack_wave, _wave_counter
    _wave_counter += 1
    if _attack_wave and _wave_counter >= _WAVE_LENGTH:
        _attack_wave = False
        _wave_counter = 0
    elif not _attack_wave and _wave_counter >= _CALM_LENGTH:
        _attack_wave = True
        _wave_counter = 0
    return _attack_wave

def timestamp_syslog():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")