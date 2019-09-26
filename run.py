from app import create_app

app = create_app()
if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], threaded=True, ssl_context=('/etc/letsencrypt/live/furan.xyz/fullchain.pem',
'/etc/letsencrypt/live/furan.xyz/privkey.pem'))
