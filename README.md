# Discord Onboarding Bypass Tool

Advanced automation tool for managing Discord server onboarding processes at scale.

## Features

- Mass onboarding bypass for Discord servers
- Modern Chrome 133 fingerprint spoofing
- Proxy rotation support (HTTP/S, authenticated proxies)
- Multi-format token support (plain tokens, email:pass:token)
- Threaded execution for high performance
- Detailed logging and error tracking
- Configurable through JSON files

## Requirements

- Python 3.9+
- TLS Client library
- Valid Discord tokens

## Installation

1. Clone repository:
```bash
git clone https://github.com/Nuu-maan/Discord-Onboarding-Bypass.git
cd discord-onboarding-bypass
```

## Install dependencies:

```bash
pip install -r requirements.txt
```

## Set up input files:

```bash
input/
├── tokens.txt      # Your Discord tokens
├── proxies.txt     # Optional proxy list
└── config.json     # Configuration file
```

## Configuration


```bash
{
    "Threads": 50,
    "Proxyless": false,
    "Debug": true,
    "Timeout": 15,
    "Retries": 3,
    "UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "LogFile": "logs/activity.log"
}
```


## Contributing

>We welcome contributions! To contribute:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Commit your changes (git commit -m 'Add new feature').
Push to the branch (git push origin feature-branch).
Open a pull request.

License:
This project is licensed under MIT [License](LICENSE).

> Disclaimer:This tool is for educational purposes only. Use responsibly and in compliance with Discord's Terms of Service.

