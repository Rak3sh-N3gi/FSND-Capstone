#!/bin/bash
export DATABASE_URL="postgresql://postgres:abc@localhost:5432/postgres"
export EXCITED="true"
export AUTH0_DOMAIN = 'dev-7pu1qwqr0730cbbq.us.auth0.com'
export JWT_SECRET = 'myjwtsecret'
export client_id ='4KV2AMw29J1ebepXTFDlriKNppzZyuI2'
export redirect_uri = 'https://render-cloud-example-ipd7.onrender.com/'
echo "setup.sh script executed successfully!"