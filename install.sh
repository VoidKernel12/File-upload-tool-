#!/bin/bash

# Color Codes for Styling
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
NC='\033[0m' # No Color

clear
echo -e "${RED}==================================================${NC}"
echo -e "${CYAN}    [🔥] HEARTKILLER CLOUD VAULT INSTALLER        ${NC}"
echo -e "${RED}==================================================${NC}"

# Step 1: Update Termux packages
echo -e "\n${YELLOW}[+] Updating & Upgrading Termux Packages...${NC}"
pkg update && pkg upgrade -y

# Step 2: Install Python, Git and Cloudflared
echo -e "\n${YELLOW}[+] Installing Python, Git, and Cloudflare Tunnel...${NC}"
pkg install python git cloudflared -y

# Step 3: Install Flask
echo -e "\n${YELLOW}[+] Installing Python Flask Framework...${NC}"
pip install --upgrade pip
pip install flask

# Completion Banner & Instructions
echo -e "\n${GREEN}==================================================${NC}"
echo -e "${GREEN} [✔] INSTALLATION COMPLETED SUCCESSFULLY!        ${NC}"
echo -e "${GREEN}==================================================${NC}"
echo -e "${CYAN} 🚀 HOW TO RUN YOUR SERVER:${NC}"
echo -e " 1. Start Server : ${YELLOW}python tool.py${NC}"
echo -e " 2. Public Link  : ${YELLOW}cloudflared tunnel --url http://127.0.0.1:5000${NC}"
echo -e "    ${CYAN}(Open a new Termux session to run the public link)${NC}"
echo -e "${GREEN}==================================================${NC}"
