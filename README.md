# 🎭 `puppet-master`

**Puppet Master** is a high-fidelity persona generator designed for OpSec researchers, social engineers, and digital forensics analysts. It automates the creation of complex "Digital Puppets" identities with visual assets, security credentials, social media biographies, and context-aware content plans.
Unlike standard "fake name" generators, Puppet Master builds a coherent narrative for each persona, including political alignment, age-appropriate social behaviors, and technical forum inquiries.

## ⚠️ Disclaimer

This tool is for **educational, research, and authorized testing purposes only**. The developer is not responsible for any misuse of the generated data. Always adhere to the Terms of Service of any platform where these personas may be utilized.

## 🚀 Features

* **Total Identity Forging**: Generates full name, age, occupation, address, and telephone data using localized providers.
* **Political & Behavioral Logic**: Personas are assigned political leanings which influence their generated content.
* **Visual Asset Generation**: Integrates with DiceBear and static APIs to download and scrub metadata profile avatars.
* **Social & Technical Content**:
  * **Social Bio**: Context-aware bios based on the puppet's job and personality.
  * **Content Plan**: Generates age-stratified social media posts.
  * **Forum Threads**: Generates strictly technical, cybersecurity, and forensics-related questions for forum simulations.

* **OpSec Ready**: Generates high-entropy passwords and security questions for every profile.
* **Metadata Scrubbing**: Automatically processes downloaded JPG avatars to remove EXIF data.

## 🛠️ Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/puppet-master.git
cd puppet-master
# Install dependencies
pip3 install -r requirements.txt
```

## 🕹️ Usage

By default, it generates a core identity. Use flags to enable extended content.

### Basic generation

```bash
python3 puppetmaster.py
```

### Enable social presence

```bash
python3 puppetmaster.py --bio --content
```

### Enable forums presence

```bash
python3 puppetmaster.py --forum-posts
```

### Full persona forge

```bash
python3 puppetmaster.py --bio --content --forum-posts
```

## 📁 Output structure

Every puppet is stored in its own directory within the `puppets/` folder:

```text
puppets/
└── FIRSTNAME_LASTNAME/
    ├── avatar.svg            # Persona profile picture
    ├── puppet_data.json      # Full data dump (Identity, Security, Content)
    └── (metadata scrubbed assets)
```
