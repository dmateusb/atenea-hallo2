#!/bin/bash
set -e

echo "🚀 Atenea-Hallo2 Setup Script"
echo "=============================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if running from project root
if [ ! -f "package.json" ]; then
    echo -e "${RED}❌ Error: Please run this script from the project root directory${NC}"
    exit 1
fi

# Step 1: Check Node.js version
echo -e "${BLUE}📦 Checking Node.js version...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    echo -e "${YELLOW}Please install Node.js 20+ from: https://nodejs.org/${NC}"
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 20 ]; then
    echo -e "${RED}❌ Node.js version 20+ required (found: $(node -v))${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Node.js $(node -v) detected${NC}"

# Step 2: Install Node.js dependencies
echo ""
echo -e "${BLUE}📦 Installing Node.js dependencies...${NC}"
npm install
echo -e "${GREEN}✅ Node.js dependencies installed${NC}"

# Step 3: Check Python version
echo ""
echo -e "${BLUE}🐍 Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    echo -e "${YELLOW}Please install Python 3.10+ from: https://www.python.org/${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
    echo -e "${RED}❌ Python 3.10+ required (found: $(python3 --version))${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python $(python3 --version) detected${NC}"

# Step 4: Create Python virtual environment
echo ""
echo -e "${BLUE}🐍 Creating Python virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment already exists, skipping creation${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# Step 5: Activate virtual environment and install dependencies
echo ""
echo -e "${BLUE}📦 Installing Python dependencies...${NC}"
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✅ Python dependencies installed${NC}"

# Step 6: Check for ffmpeg
echo ""
echo -e "${BLUE}🎬 Checking for ffmpeg...${NC}"
if ! command -v ffmpeg &> /dev/null; then
    echo -e "${YELLOW}⚠️  ffmpeg not found${NC}"
    echo -e "${YELLOW}Please install ffmpeg:${NC}"
    echo -e "${YELLOW}  macOS: brew install ffmpeg${NC}"
    echo -e "${YELLOW}  Ubuntu: sudo apt-get install ffmpeg${NC}"
    echo ""
else
    echo -e "${GREEN}✅ ffmpeg detected${NC}"
fi

# Step 7: Clone Hallo2 repository
echo ""
echo -e "${BLUE}📥 Checking Hallo2 repository...${NC}"
if [ -d "hallo2" ]; then
    echo -e "${YELLOW}⚠️  hallo2/ directory already exists${NC}"
    read -p "Do you want to re-clone it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf hallo2
        git clone https://github.com/fudan-generative-vision/hallo2.git
        echo -e "${GREEN}✅ Hallo2 repository cloned${NC}"
    fi
else
    git clone https://github.com/fudan-generative-vision/hallo2.git
    echo -e "${GREEN}✅ Hallo2 repository cloned${NC}"
fi

# Step 8: Install Hallo2 dependencies
echo ""
echo -e "${BLUE}📦 Installing Hallo2 dependencies...${NC}"
cd hallo2
pip install -r requirements.txt
cd ..
echo -e "${GREEN}✅ Hallo2 dependencies installed${NC}"

# Step 9: Check for .env file
echo ""
echo -e "${BLUE}🔑 Checking environment configuration...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found${NC}"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${GREEN}✅ Created .env from .env.example${NC}"
        echo -e "${YELLOW}⚠️  Please edit .env and add your OPENAI_API_KEY${NC}"
    else
        echo -e "${RED}❌ No .env.example file found${NC}"
    fi
else
    echo -e "${GREEN}✅ .env file exists${NC}"
fi

# Step 10: Create data directories
echo ""
echo -e "${BLUE}📁 Creating data directories...${NC}"
mkdir -p data/images
mkdir -p data/audio
mkdir -p data/videos
echo -e "${GREEN}✅ Data directories created${NC}"

# Step 11: Download Hallo2 models (optional)
echo ""
echo -e "${BLUE}📥 Hallo2 Model Download${NC}"
echo -e "${YELLOW}Hallo2 requires pretrained models to run.${NC}"
echo -e "${YELLOW}Please follow the instructions in hallo2/README.md to download models.${NC}"
echo -e "${YELLOW}Models are typically downloaded to: hallo2/pretrained_models/${NC}"
echo ""

# Setup complete
echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo -e "  1. Edit .env and add your OPENAI_API_KEY"
echo -e "  2. Download Hallo2 models (see hallo2/README.md)"
echo -e "  3. Add an avatar image to: data/images/avatar.png"
echo -e "  4. Create an input text file: input.txt"
echo -e "  5. Run: npm run generate"
echo ""
echo -e "${BLUE}For more information, see README.md${NC}"
