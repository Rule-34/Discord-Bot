'use strict'

const generalConfig = require('./config/config.js'),
  // Packages
  Discord = require('discord.js'),
  debug = require('debug')('Discord Bot'),
  // Init
  client = new Discord.Client()

client.on('ready', () => {
  debug(`Logged in as ${client.user.tag}!`)
  debug(process.env.DEBUG)
})

client.on('message', msg => {
  if (msg.content === 'ping') {
    msg.reply('pong')
  }
})

// Start bot
client.login(generalConfig.token)
