from flask import Flask, render_template, request, jsonify
import requests
import re
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    cookie = data.get('cookie')
    link = data.get('link')
    limit = int(data.get('limit'))

    success_count = 0

    header = {
        "authority": "graph.facebook.com",
        "cache-control": "max-age=0",
        "sec-ch-ua-mobile": "?0",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.66 Safari/537.36"
    }

    ses = requests.Session()

    try:
        get_tok = ses.get('https://business.facebook.com/business_locations', headers={
            "user-agent": "Mozilla/5.0 (Linux; Android 8.1.0; MI 8 Build/OPM1.171019.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.86 Mobile Safari/537.36",
            "referer": "https://www.facebook.com/",
            "host": "business.facebook.com",
            "origin": "https://business.facebook.com",
            "upgrade-insecure-requests": "1",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "content-type": "text/html; charset=utf-8"
        }, cookies={"cookie": cookie})
        tokenz = re.search("(EAAG\w+)", get_tok.text).group(1)
        coki = {"cookie": cookie}
    except Exception as e:
        return jsonify({'success': False, 'message': 'Invalid cookie'})

    token = tokenz  

    try:
        for x in range(limit):
            x += 1
            response = ses.post(
                f"https://graph.facebook.com/v13.0/me/feed?link={link}&published=0&access_token={token}",
                headers=header, cookies=coki).json()
            if "id" in response:
                success_count += 1
                print("[+] DONE => {}".format(success_count))
                time.sleep(1)  # Add 1 second delay
            else:
                return jsonify({'success': False, 'message': 'Failed, your account might be flagged as spam'})
    except requests.exceptions.ConnectionError:
        return jsonify({'success': False, 'message': 'Unable to connect to the internet!'})

    return jsonify({'success': True, 'success_count': success_count, 'message': f'Successfully sent {success_count} messages.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
