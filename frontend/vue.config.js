module.exports = {
  pages: {
      admin: {
          entry: './src/admin/index.js',
          template: 'src/admin/index.html',
          filename: 'admin/index.html',
          title: 'DB Test Page',
          chunks: ['chunk-vendors', 'chunk-common', 'admin']
      },
      user: {
          entry: './src/user/index.js',
          template: 'src/user/index.html',
          filename: 'index.html',
          title: 'MEDIAI+',
          chunks: ['chunk-vendors', 'chunk-common', 'user']
      }
  },

  transpileDependencies: [
    'vuetify'
  ]
}
