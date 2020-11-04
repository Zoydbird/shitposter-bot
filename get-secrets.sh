#helper script to set secrets from gcloud secrets manager

if [ ! -f ".env" ]; then
    touch .env

    echo -n 'DISCORD_TOKEN=' > .env    
    gcloud secrets versions access latest --secret="discord-bot-token"  >> .env

    #newline
    echo '' >> .env

    echo -n 'DISCORD_USER_ID=' >> .env
    gcloud secrets versions access latest --secret="discord-user-id" >> .env
fi