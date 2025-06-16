# 🧹 Directory_Cleaner_Using_Automation

This is an automation script written in Python to detect and delete duplicate files in a given directory. It uses **MD5 checksum hashing** to find duplicates and supports **scheduled cleaning** at regular intervals.

---

## 🚀 Features

- ✅ Detect duplicate files using MD5 checksum
- 🗑️ Automatically delete duplicate files
- 📁 Supports any directory (absolute or relative path)
- 🕒 Schedule duplicate file cleanup at user-defined time intervals
- 📜 Creates a log file with timestamps
- 🧠 Includes Help (`--h`) and Usage (`--u`) command-line options

---

## 📦 Requirements

- Python 3.x
- Modules used:
  - `os`
  - `sys`
  - `hashlib`
  - `schedule`
  - `time`

---

## 🛠️ How to Use
- python DirectoryCleaner.py <DirectoryPath> <TimeInMinutes>
### 💻 Command-Line Usage
- To run the script, use the following syntax in your terminal or command prompt:
