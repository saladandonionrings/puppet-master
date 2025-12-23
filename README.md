# 🎭 `puppet-master`

**Puppet Master** is a high-fidelity persona generator designed for OpSec researchers, social engineers, and digital forensics analysts. 
Can be use for creating sock puppets on Instagram, Twitter, Facebook and many forums.

It offers : 
* **Full identity forging**: full name, age, occupation, address, and telephone data
* **Political / behavioral logic**: Personas are assigned political leanings which influence their generated content (*far-left, left, center/liberal, right, far-right*)
* **Visual asset generation**: DiceBear and static APIs for profile avatars
* **Social / Technical content**:
  * **Social bio**: context-aware bios based on the puppet's job and personality
  * **Content plan**: generates age-stratified social media posts
  * **Forum threads**: generates strictly technical, cybersecurity, and forensics-related questions for forum simulations

**Security-related** :
* **OpSec Ready**: create high-entropy passwords and security questions
* **Metadata Scrubbing**: remove EXIF data from avatars

## ⚠️ Disclaimer

This tool is for **educational, research, and authorized testing purposes only**. The developer is not responsible for any misuse of the generated data. Always adhere to the Terms of Service of any platform where these personas may be utilized.

## Installation

```bash
git clone https://github.com/yourusername/puppet-master.git
cd puppet-master
# Install dependencies
pip3 install -r requirements.txt
```

## Usage

```bash
# basic generation
python3 puppetmaster.py

# social presence
python3 puppetmaster.py --bio --content

# forums presence
python3 puppetmaster.py --forum-posts

# full
python3 puppetmaster.py --bio --content --forum-posts

```

>Output will be in `puppets/FIRSTNAME_LASTNAME`
