# 🔐 Password Manager | مدير كلمات المرور

[English](#english) | [العربية](#arabic)

---

<a id="english"></a>

## English

A simple desktop password manager written in Python. It stores website accounts in a local SQLite database, with every field encrypted using **AES-256-GCM** and keys derived from your master password with **Argon2id**. The interface is built with **PySide6 (Qt)**.

### Features

- Add a website account (site name, username, password)
- Show all saved accounts (decrypted with your master password)
- Delete an account by its ID
- Everything is stored locally, with no internet connection or server
- Site name, username, and password are all encrypted, not just the password

### Requirements

- Python **3.12 or newer** (the code uses nested quotes inside f-strings)
- Dependencies:
  - `PySide6`
  - `argon2-cffi`
  - `cryptography`

### Installation

```bash
pip install -r requirements.txt
```

### Usage

```bash
python main.py
```

The database file `database.db` is created automatically in the folder you run the program from.

1. **Add new website**: enter your master password, then the website name, username, and password, and click *Add*.
2. **Show all website**: enter your master password and click *Show all*.
3. **Delete website**: enter the ID shown in the list and click *Delete*.

> ⚠️ Use the **same master password** every time. Entries added with different master passwords cannot be decrypted together, and *Show all* will report a wrong password.

### Project Structure

| File | Description |
|---|---|
| `main.py` | Entry point; wires the modules together |
| `config.py` | Shared objects (database, crypto, manager) |
| `database.py` | SQLite connection and table creation |
| `crypt.py` | Key derivation (Argon2id) and AES-GCM encryption/decryption |
| `password_manager.py` | Add, show, and delete logic |
| `ui.py` | PySide6 graphical interface |

### How Encryption Works

1. A random 16-byte **salt** is generated for each entry.
2. A 32-byte key is derived from the master password and salt using **Argon2id** (`time_cost=5`, `memory_cost=40000`, `parallelism=4`).
3. The name, username, and password are each encrypted with **AES-GCM** using a separate random 12-byte **nonce**.
4. The ciphertexts, salt, and nonces are saved in the `websites` table.

### Security Notes

- If you forget the master password, your data **cannot be recovered**.
- The master password is not stored anywhere; a wrong password is detected when decryption fails.
- Back up `database.db` regularly and keep it somewhere safe.
- This is a learning/personal project and has not been security-audited.

---

<a id="arabic"></a>

<div dir="rtl" align="right">

## العربية

مدير كلمات مرور بسيط لسطح المكتب مكتوب بلغة بايثون. يحفظ حسابات المواقع في قاعدة بيانات **SQLite** محلية، وكل الحقول مشفّرة بخوارزمية **AES-256-GCM**، ويتم اشتقاق المفتاح من كلمة المرور الرئيسية باستخدام **Argon2id**. الواجهة مبنية بمكتبة **PySide6 (Qt)**.

### المميزات

- إضافة حساب موقع (اسم الموقع، اسم المستخدم، كلمة المرور)
- عرض كل الحسابات المحفوظة (يتم فك تشفيرها بكلمة مرورك الرئيسية)
- حذف حساب باستخدام رقمه (ID)
- كل شيء يُخزَّن محليًا بدون إنترنت أو سيرفر
- يتم تشفير اسم الموقع واسم المستخدم وكلمة المرور، وليس كلمة المرور فقط

### المتطلبات

- بايثون **3.12 أو أحدث** (الكود يستخدم علامات اقتباس متداخلة داخل f-strings)
- المكتبات:
  - `PySide6`
  - `argon2-cffi`
  - `cryptography`

### التثبيت

```bash
pip install -r requirements.txt
```

### طريقة الاستخدام

```bash
python main.py
```

يتم إنشاء ملف قاعدة البيانات `database.db` تلقائيًا في نفس المجلد الذي تشغّل منه البرنامج.

1. **Add new website** (إضافة موقع): أدخل كلمة المرور الرئيسية، ثم اسم الموقع واسم المستخدم وكلمة المرور، واضغط *Add*.
2. **Show all website** (عرض الكل): أدخل كلمة المرور الرئيسية واضغط *Show all*.
3. **Delete website** (حذف موقع): أدخل رقم الـ ID الظاهر في القائمة واضغط *Delete*.

> ⚠️ استخدم **نفس كلمة المرور الرئيسية** دائمًا. الحسابات المضافة بكلمات مرور رئيسية مختلفة لا يمكن فك تشفيرها معًا، وسيظهر خطأ كلمة المرور الخاطئة عند العرض.

### هيكل المشروع

| الملف | الوصف |
|---|---|
| `main.py` | نقطة البداية وربط الوحدات ببعضها |
| `config.py` | الكائنات المشتركة (قاعدة البيانات، التشفير، المدير) |
| `database.py` | الاتصال بـ SQLite وإنشاء الجدول |
| `crypt.py` | اشتقاق المفتاح (Argon2id) والتشفير وفك التشفير (AES-GCM) |
| `password_manager.py` | منطق الإضافة والعرض والحذف |
| `ui.py` | الواجهة الرسومية بـ PySide6 |

### كيف يعمل التشفير

1. يتم توليد **salt** عشوائي (16 بايت) لكل حساب.
2. يتم اشتقاق مفتاح (32 بايت) من كلمة المرور الرئيسية والـ salt باستخدام **Argon2id** (`time_cost=5`، `memory_cost=40000`، `parallelism=4`).
3. يتم تشفير الاسم واسم المستخدم وكلمة المرور كل واحد على حدة بـ **AES-GCM** مع **nonce** عشوائي (12 بايت) مختلف لكل حقل.
4. تُحفظ النصوص المشفّرة والـ salt والـ nonces في جدول `websites`.

### ملاحظات أمنية

- إذا نسيت كلمة المرور الرئيسية فلا يمكن استرجاع بياناتك.
- كلمة المرور الرئيسية لا تُخزَّن في أي مكان؛ يتم اكتشاف الخطأ عند فشل فك التشفير.
- خذ نسخة احتياطية من `database.db` بشكل دوري واحفظها في مكان آمن.
- هذا مشروع تعليمي/شخصي ولم تتم مراجعته أمنيًا.

</div>
