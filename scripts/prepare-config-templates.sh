#/bin/bash
cp -v cipe/settings.py.sample cipe/settings.py
cp -v .env.prod.db.sample .env.prod.db
cp -v .env.prod.sample .env.prod
echo ""
echo "This is a randomly generated secret key to put in your new .env.prod"
KEY=$(python -c 'import random; print("".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)]))')
echo "SECRET_KEY=$KEY"
echo ""
echo "Remember to customize your passwords and Google Maps API KEY"

