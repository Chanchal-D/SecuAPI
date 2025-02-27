# SecuAPI 🛡️

> A powerful API security scanning tool with an intuitive React frontend

SecuAPI helps developers and security teams identify vulnerabilities in their API endpoints through automated security scanning and real-time monitoring.

## ✨ Features

- 🔍 Comprehensive API endpoint security scanning
- 📊 Real-time vulnerability detection and reporting
- 🎯 Configurable security thresholds and rules
- 🖥️ Modern React-based user interface
- 🔄 CI/CD pipeline integration
- 📝 Detailed JSON report generation
- ⚡ Fast and efficient scanning engine

## 🚀 Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/Chanchal-D/SecuAPI.git
cd SecuAPI
```

2. **Set up the backend**
```bash
pip install -r requirements.txt
python -m src.main
```

3. **Launch the frontend**
```bash
cd frontend
npm install
npm start
```

4. Open http://localhost:3000 in your browser

## 📋 Requirements

- Python 3.8+
- Node.js 14+
- npm 6+

## 🛠️ Configuration

Create \`config/ci_config.yml\`:

```yaml
api:
  base_url: \"https://your-api.com\"
  endpoints:
    - \"/users\"
    - \"/products\"
  headers:
    User-Agent: \"API-Security-Scanner/1.0\"
```

## 📊 Example Usage

```bash
# Start a security scan
python -m src.main --config config/ci_config.yml
```

## 🔒 Security Features

- SQL Injection detection
- XSS vulnerability scanning
- Authentication bypass testing
- Rate-limiting analysis
- Security headers verification
- CORS configuration validation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License. For details, see the [LICENSE](LICENSE) file.

## 📬 Contact

Chanchal - chanchalkuntal398@gmail.com

Project Link: [https://github.com/Chanchal-D/SecuAPI](https://github.com/Chanchal-D/SecuAPI)

---
⭐ Star us on GitHub — it motivates us a lot!
