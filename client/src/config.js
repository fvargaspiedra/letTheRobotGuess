const config = {
  development: {
    apiUrl: 'http://localhost:5000'
  },
  production: {
    apiUrl: 'http://robotguess.akamaiu.com/api'
  }
}

export default config[process.env.NODE_ENV]
