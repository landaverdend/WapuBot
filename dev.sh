#!/bin/bash
set -e

source .venv/bin/activate

# start uvicorn in background
python -m uvicorn app.main:app --reload --port 8080 &
UVICORN_PID=$!

# start ngrok in background
ngrok http 8080 --log=stdout --log-format=json 2>/dev/null &
NGROK_PID=$!

cleanup() {
    kill $UVICORN_PID $NGROK_PID 2>/dev/null
    exit 0
}
trap cleanup SIGINT SIGTERM

# wait for ngrok to come up and grab the public URL
sleep 2
PUBLIC_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | python3 -c "import sys,json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])")

# register webhook with telegram
source .env
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook?url=${PUBLIC_URL}/webhook&secret_token=${WEBHOOK_SECRET}" > /dev/null

echo ""
echo "  bot:    https://t.me/whatsupay_bot"
echo "  server: http://127.0.0.1:8080"
echo "  ngrok:  ${PUBLIC_URL}"
echo "  ctrl+c to stop"
echo ""

wait
