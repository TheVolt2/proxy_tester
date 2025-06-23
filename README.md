
# **Proxy Checker**  
### **A High-Performance Proxy Validation Tool with GUI**  

#### **Overview**  
**Proxy Checker** is a Python-based application designed to quickly validate the functionality of proxy servers. Built with simplicity and efficiency in mind, it checks large lists of proxies (HTTP/HTTPS/SOCKS4/SOCKS5) and filters out non-working ones, saving time for developers, security researchers, and network administrators.  

The tool features a **user-friendly Tkinter GUI**, **multi-threaded validation**, and support for **authenticated proxies**, making it ideal for:  
- Verifying free/public proxy lists  
- Cleaning outdated proxies from databases  
- Testing proxy anonymity and response times  
- Preparing reliable proxy pools for web scraping or automation  

---

### **Key Features**  

#### **1. Multi-Threaded Proxy Validation**  
- Checks **50+ proxies simultaneously** (adjustable thread count)  
- Measures **latency** and **success rates** for each proxy  
- Identifies failures with **detailed error logs** (timeouts, auth errors, etc.)  

#### **2. Broad Proxy Support**  
- **Protocols:** HTTP, HTTPS, SOCKS4, SOCKS5  
- **Authentication:** Handles `user:pass@ip:port` formats  
- **Input Flexibility:** Loads proxies from `.txt` files (one proxy per line)  

#### **3. Intuitive GUI**  
- **Real-time progress tracking** (progress bar + live stats)  
- **Color-coded results**:  
  - ✅ **Working proxies** (green)  
  - ❌ **Failed proxies** (red, with error details)  
- **One-click export** – save working proxies to a clean file  

#### **4. Lightweight & Portable**  
- **No external dependencies** (just Python 3.8+ and `requests`)  
- **Cross-platform**: Works on Windows, macOS, and Linux  

---

### **How It Works**  
1. **Input**: Provide a `.txt` file with proxies (e.g., `ip:port` or `user:pass@ip:port`).  
2. **Validation**: The tool sends test requests to `httpbin.org/ip` (or a custom URL) via each proxy.  
3. **Results**:  
   - Working proxies are displayed with latency metrics.  
   - Dead proxies are flagged with failure reasons (e.g., `ConnectionTimeout`, `403 Forbidden`).  
4. **Export**: Save the cleaned list with a single button click.  

---

### **Example Use Cases**  
- **Web Scraping**: Ensure your proxy pool is reliable before running crawlers.  
- **Security Testing**: Check proxy anonymity and IP leakage risks.  
- **Network Maintenance**: Audit corporate or personal proxy servers.  

---

### **Technical Details**  
- **Backend**: Python (`requests`, `concurrent.futures` for threading)  
- **Frontend**: Tkinter (native GUI, no Qt/PyQt required)  
- **Tested With**: Free/public proxy lists, private authenticated proxies  

---

### **Why Choose This Tool?**  
✔ **No bloat** – Unlike heavy GUI frameworks (PyQt), it runs on vanilla Python.  
✔ **Transparent** – Open-source with clear error reporting.  
✔ **Customizable** – Easily modify the test URL or timeout settings in the code.  
