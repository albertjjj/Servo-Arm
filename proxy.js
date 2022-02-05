const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const app = express();

app.use('/', createProxyMiddleware({ target: 'http://localhost:5000/', changeOrigin: true }));
app.use('/index', createProxyMiddleware({ target: 'http://localhost:5000/index', changeOrigin: true }));
app.listen(3000);