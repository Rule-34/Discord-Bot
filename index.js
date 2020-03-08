require('dotenv').config()

const fs = require('fs'),
  // Packages
  Discord = require('discord.js'),
  debug = require('debug')('bot:main'),
  // Own
  { prefix } = require('./config/config.json')

// Init
const client = new Discord.Client()
client.commands = new Discord.Collection()

const commandFiles = fs
  .readdirSync('./commands')
  .filter(file => file.endsWith('.js'))

for (const file of commandFiles) {
  const command = require(`./commands/${file}`)
  client.commands.set(command.name, command)
}

client.once('ready', () => {
  debug('Ready!')
})

client.login(process.env.BOT_DISCORD_TOKEN)
