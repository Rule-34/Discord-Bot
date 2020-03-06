require('dotenv').config()
// Defines defaults if they are available from ENV
const generalConfig = {
  env: process.env.NODE_ENV || 'production',
  token: process.env.BOT_DISCORD_TOKEN,
}

module.exports = generalConfig
