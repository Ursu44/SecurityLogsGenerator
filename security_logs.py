import random
from utils import random_file_path, random_user, random_ip
from datetime import datetime, timezone

GOOD_RATIO = 0.65


def av_log(malicious=False):
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    info = [
        f"{timestamp} AV INFO Scan completed successfully",
        f"{timestamp} AV INFO No threats found",
        f"{timestamp} AV INFO Scheduled scan finished",
        f"{timestamp} AV INFO Real-time protection active",
        f"{timestamp} AV INFO Virus definitions updated",
        f"{timestamp} AV INFO Quick scan completed"
    ]

    alerts = [
        f"{timestamp} AV ALERT Malware detected file={random_file_path()} action=quarantine",
        f"{timestamp} AV ALERT Trojan detected file={random_file_path()} action=blocked",
        f"{timestamp} AV ALERT Ransomware behavior detected action=terminated",
        f"{timestamp} AV ALERT Spyware detected file={random_file_path()} action=deleted",
        f"{timestamp} AV ALERT Worm detected file={random_file_path()} action=isolated"
    ]

    return random.choice(alerts if malicious else info)


def edr_suspicious_process(malicious=False):
    benign_processes = [
        "chrome.exe",
        "outlook.exe",
        "teams.exe",
        "explorer.exe",
        "powershell.exe -NoProfile"
    ]

    suspicious_processes = [
        "powershell.exe",
        "cmd.exe",
        "rundll32.exe",
        "mimikatz.exe",
        "wmic.exe",
        "certutil.exe",
        "mshta.exe"
    ]

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    level = "WARN" if malicious else "INFO"

    process = random.choice(
        suspicious_processes if malicious else benign_processes
    )

    return (
        f"{timestamp} EDR {level} Process execution detected "
        f"process={process} user={random_user()} "
        f"src_ip={random_ip()}"
    )


def edr_credential_dump():
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    techniques = [
        "T1003.001",
        "T1003.002",
        "T1003.006"
    ]

    return (
        f"{timestamp} EDR ALERT Credential access detected "
        f"technique={random.choice(techniques)} process=lsass.exe "
        f"user={random_user()} src_ip={random_ip()}"
    )


def lateral_movement_log():
    techniques = [
        "SMB remote execution",
        "WMI lateral movement",
        "Pass-the-Hash",
        "Remote Service Creation",
        "PsExec execution",
        "RDP lateral movement"
    ]

    src_hosts = ["workstation01", "workstation02", "laptop01"]
    dst_hosts = ["server01", "db01", "fileserver01"]

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return (
        f"{timestamp} EDR ALERT Lateral movement detected "
        f"technique=\"{random.choice(techniques)}\" "
        f"src_host={random.choice(src_hosts)} "
        f"dst_host={random.choice(dst_hosts)} "
        f"user={random_user()}"
    )


def siem_correlation_log():
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    rules = [
        "Multiple credential access events",
        "Suspicious process followed by lateral movement",
        "Malware detection + data access",
        "Privilege escalation chain detected",
        "EDR alert followed by outbound connection",
        "Multiple failed authentications across hosts"
    ]

    return (
        f"{timestamp} SIEM ALERT Correlation rule triggered "
        f"rule=\"{random.choice(rules)}\" severity=high"
    )


def dlp_log():
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    channels = [
        "HTTP upload",
        "FTP transfer",
        "Cloud storage",
        "Email attachment",
        "SFTP transfer",
        "USB removable media"
    ]

    data_types = [
        "PII",
        "Credentials",
        "Source code",
        "Financial data",
        "Customer database",
        "HR records"
    ]

    return (
        f"{timestamp} DLP ALERT Data exfiltration blocked "
        f"channel=\"{random.choice(channels)}\" "
        f"data_type=\"{random.choice(data_types)}\" "
        f"user={random_user()}"
    )


_generator_index = 0

def generate():
    global _generator_index

    malicious = random.random() > GOOD_RATIO

    benign_generators = [
        ("av_log", lambda: av_log(False)),
        ("edr_suspicious_process", lambda: edr_suspicious_process(False))
    ]

    malicious_generators = [
        ("av_log", lambda: av_log(True)),
        ("edr_suspicious_process", lambda: edr_suspicious_process(True)),
        ("edr_credential_dump", edr_credential_dump),
        ("lateral_movement_log", lateral_movement_log),
        ("siem_correlation_log", siem_correlation_log),
        ("dlp_log", dlp_log)
    ]

    if malicious:
        name, func = malicious_generators[_generator_index % len(malicious_generators)]
    else:
        name, func = benign_generators[_generator_index % len(benign_generators)]

    _generator_index += 1
    return func()
