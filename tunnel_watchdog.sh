#!/bin/bash
# Offer 捕手 — 公网隧道守护脚本
# 功能: 保持 localhost.run SSH 隧道持续在线

SSH_CMD="ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -o ServerAliveCountMax=2 -o ExitOnForwardFailure=yes -R 80:localhost:8000 localhost.run"

while true; do
    echo "[$(date '+%H:%M:%S')] Starting tunnel..."
    $SSH_CMD 2>&1 | while read line; do
        echo "[$(date '+%H:%M:%S')] $line"
        # 提取新URL
        if echo "$line" | grep -q "lhr.life"; then
            echo "=== PUBLIC URL: $(echo $line | grep -oP 'https://[a-z0-9]+\.lhr\.life') ==="
        fi
    done
    echo "[$(date '+%H:%M:%S')] Tunnel dropped. Reconnecting in 5s..."
    sleep 5
done
