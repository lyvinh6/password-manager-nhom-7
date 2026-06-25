#!/bin/bash
# Chạy script này để đẩy dự án lên GitHub
# Thay YOUR_USERNAME và YOUR_REPO_NAME cho phù hợp

cd /home/claude/password-manager  # hoặc đường dẫn đến thư mục dự án

git init
git add .
git commit -m "feat: khởi tạo cấu trúc dự án Password Manager - Nhóm 7"

# Tạo repo trên GitHub trước, sau đó chạy 2 lệnh này:
git remote add origin https://github.com/YOUR_USERNAME/password-manager.git
git push -u origin main
