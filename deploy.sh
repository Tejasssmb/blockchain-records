#!/bin/bash
# Automated Deployment Script for Render.com

echo "=========================================="
echo "Blockchain Academic Record System"
echo "Deployment Preparation"
echo "=========================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    git config user.email "deployment@blockchain.edu"
    git config user.name "Blockchain Deployer"
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "ERROR: requirements.txt not found!"
    exit 1
fi

# Check if Procfile exists
if [ ! -f "Procfile" ]; then
    echo "ERROR: Procfile not found!"
    exit 1
fi

# Add all files
echo "Adding files to git..."
git add .

# Commit
echo "Committing changes..."
git commit -m "Blockchain Academic Record System with Metamask Integration - Ready for Deployment"

echo ""
echo "=========================================="
echo "✅ Repository ready for deployment!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Create a repository on GitHub: https://github.com/new"
echo "2. Add remote: git remote add origin https://github.com/YOUR_USERNAME/blockchain-records.git"
echo "3. Push: git push -u origin main"
echo "4. Go to Render.com and connect your GitHub repo"
echo "5. Render will auto-deploy!"
echo ""
echo "Your deployed link will look like:"
echo "https://blockchain-academic-records.onrender.com"
echo ""
