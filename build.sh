#!/bin/bash
set -e

echo "Building React frontend..."
cd frontend
npm install
npm run build

echo "Copying build files to Flask static folder..."
mkdir -p ../build
cp -r build/* ../build/

echo "Done! You can now run the app with: python -m src.main"