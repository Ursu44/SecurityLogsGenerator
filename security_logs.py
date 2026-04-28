import random
from utils import random_file_path, random_user, random_ip, is_attack_wave, timestamp_syslog
from datetime import datetime, timezone


def av_log(malicious=False):
    info = [
        f"{timestamp_syslog()} AV INFO Scan completed successfully",
        f"{timestamp_syslog()} AV INFO No threats found",
        f"{timestamp_syslog()} AV INFO Scheduled scan finished",
        f"{timestamp_syslog()} AV INFO Real-time protection active",
        f"{timestamp_syslog()} AV INFO Virus definitions updated",
        f"{timestamp_syslog()} AV INFO Quick scan completed"
    ]
    alerts = [
        f"{timestamp_syslog()} AV ALERT Malware detected file={random_file_path()} action=quarantine",
        f"{timestamp_syslog()} AV ALERT Trojan detected file={random_file_path()} action=blocked",
        f"{timestamp_syslog()} AV ALERT Ransomware behavior detected action=terminated",
        f"{timestamp_syslog()} AV ALERT Spyware detected file={random_file_path()} action=deleted",
        f"{timestamp_syslog()} AV ALERT Worm detected file={random_file_path()} action=isolated"
    ]
    return random.choice(alerts if malicious else info)


def edr_suspicious_process(malicious=False):
    benign_processes = [
        "chrome.exe", "outlook.exe", "teams.exe",
        "explorer.exe", "powershell.exe -NoProfile"
    ]
    suspicious_processes = [
        "powershell.exe", "cmd.exe", "rundll32.exe",
        "mimikatz.exe", "wmic.exe", "certutil.exe", "mshta.exe"
    ]
    level = "WARN" if malicious else "INFO"
    process = random.choice(suspicious_processes if malicious else benign_processes)
    return (
        f"{timestamp_syslog()} EDR {level} Process execution detected "
        f"process={process} user={random_user()} src_ip={random_ip()}"
    )


def edr_credential_dump(malicious=False):
    if not malicious:
        return f"{timestamp_syslog()} EDR INFO LSASS access by trusted process process=lsass.exe user={random_user()}"
    techniques = ["T1003.001", "T1003.002", "T1003.006"]
    return (
        f"{timestamp_syslog()} EDR ALERT Credential access detected "
        f"technique={random.choice(techniques)} process=lsass.exe "
        f"user={random_user()} src_ip={random_ip()}"
    )


def lateral_movement_log(malicious=False):
    src_hosts = ["workstation01", "workstation02", "laptop01"]
    dst_hosts = ["server01", "db01", "fileserver01"]
    if not malicious:
        return (
            f"{timestamp_syslog()} EDR INFO Remote connection established "
            f"src_host={random.choice(src_hosts)} dst_host={random.choice(dst_hosts)} "
            f"user={random_user()}"
        )
    techniques = [
        "SMB remote execution", "WMI lateral movement", "Pass-the-Hash",
        "Remote Service Creation", "PsExec execution", "RDP lateral movement"
    ]
    return (
        f"{timestamp_syslog()} EDR ALERT Lateral movement detected "
        f"technique=\"{random.choice(techniques)}\" "
        f"src_host={random.choice(src_hosts)} dst_host={random.choice(dst_hosts)} "
        f"user={random_user()}"
    )


def siem_correlation_log(malicious=False):
    if not malicious:
        return f"{timestamp_syslog()} SIEM INFO No correlation rules triggered severity=low"
    rules = [
        "Multiple credential access events",
        "Suspicious process followed by lateral movement",
        "Malware detection + data access",
        "Privilege escalation chain detected",
        "EDR alert followed by outbound connection",
        "Multiple failed authentications across hosts"
    ]
    return (
        f"{timestamp_syslog()} SIEM ALERT Correlation rule triggered "
        f"rule=\"{random.choice(rules)}\" severity=high"
    )


def dlp_log(malicious=False):
    channels = [
        "HTTP upload", "FTP transfer", "Cloud storage",
        "Email attachment", "SFTP transfer", "USB removable media"
    ]
    data_types = [
        "PII", "Credentials", "Source code",
        "Financial data", "Customer database", "HR records"
    ]
    if not malicious:
        return (
            f"{timestamp_syslog()} DLP INFO Data transfer allowed "
            f"channel=\"{random.choice(channels)}\" data_type=\"{random.choice(data_types)}\" "
            f"user={random_user()}"
        )
    return (
        f"{timestamp_syslog()} DLP ALERT Data exfiltration blocked "
        f"channel=\"{random.choice(channels)}\" data_type=\"{random.choice(data_types)}\" "
        f"user={random_user()}"
    )


def generate():
    malicious = is_attack_wave()

    generators = [
        lambda: av_log(malicious),
        lambda: edr_suspicious_process(malicious),
        lambda: edr_credential_dump(malicious),
        lambda: lateral_movement_log(malicious),
        lambda: siem_correlation_log(malicious),
        lambda: dlp_log(malicious),
    ]

    return random.choice(generators)()