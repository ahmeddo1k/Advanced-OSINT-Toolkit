# Advanced OSINT Toolkit

أداة متقدمة لجمع المعلومات الاستخباراتية مفتوحة المصدر (OSINT) تدعم:

- 📱 البحث عن أرقام الهواتف (الدولة، المشغل، التوقيت)
- 📧 تحليل البريد الإلكتروني (المزود، الأمان)
- 🌐 فحص شامل للنطاقات (WHOIS, DNS, SSL, Subdomains, Shodan, VirusTotal)
- 👤 البحث عن حسابات المستخدمين عبر 20+ منصة تواصل اجتماعي

## المميزات
- واجهة تفاعلية غنية بالألوان
- تقارير بصيغ TXT, JSON, HTML
- دعم APIs (Shodan, VirusTotal)
- معالجة متوازية للفحص
- نظام تسجيل متقدم
- تحقق من صحة المدخلات

## التثبيت
```bash
git clone https://github.com/yourusername/advanced-osint-toolkit.git
cd advanced-osint-toolkit
pip install -r requirements.txt
cp .env.example .env
# قم بتعديل .env وأضف مفاتيح API الخاصة بك

## الأستخدام

# وضع تفاعلي
python main.py

# أو مباشرة
python main.py -p +201234567890
python main.py -e user@example.com
python main.py -d example.com
python main.py -u username
