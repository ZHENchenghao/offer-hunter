"""Tunnel watchdog — keep public URL alive"""
import subprocess
import time
import sys
import os

TUNNELS = [
    {
        "name": "localhost.run",
        "cmd": [
            "ssh", "-o", "StrictHostKeyChecking=no",
            "-o", "ServerAliveInterval=15",
            "-o", "ServerAliveCountMax=3",
            "-o", "ConnectTimeout=10",
            "-R", "80:localhost:8000", "localhost.run"
        ],
        "url_pattern": "lhr.life"
    },
]

def run_tunnel(name, cmd):
    """Run a tunnel and restart if it dies"""
    while True:
        print(f"[{time.strftime('%H:%M:%S')}] Starting {name}...")
        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            for line in proc.stdout:
                line = line.strip()
                if line:
                    print(f"[{name}] {line}")
                    # Extract URL
                    if "lhr.life" in line:
                        import re
                        urls = re.findall(r'https://[a-z0-9]+\.lhr\.life', line)
                        for u in urls:
                            print(f"\n{'='*60}")
                            print(f"PUBLIC URL: {u}")
                            print(f"{'='*60}\n")
                            # Write to file for easy reference
                            with open(os.path.join(os.path.dirname(__file__), 'current_url.txt'), 'w') as f:
                                f.write(u)
            proc.wait()
        except Exception as e:
            print(f"[{name}] Error: {e}")
        print(f"[{time.strftime('%H:%M:%S')}] {name} died, restarting in 3s...")
        time.sleep(3)


if __name__ == "__main__":
    print("Tunnel watchdog starting...")
    # Start localhost.run tunnel
    run_tunnel("localhost.run", TUNNELS[0]["cmd"])
