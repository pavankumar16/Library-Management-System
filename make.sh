rm -rf ./static/dist
cd static
npm run watch
python server/server.py
