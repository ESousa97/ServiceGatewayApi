module.exports = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: process.env.NODE_ENV === 'production' ? 'https://service-gateway-api.vercel.app/api/:path*' : 'http://localhost:5001/:path*',
      },
      {
        source: '/cluster-tickets',
        destination: process.env.NODE_ENV === 'production' ? 'https://service-gateway-api.vercel.app/cluster-tickets' : 'http://localhost:5001/cluster-tickets',
      }
    ]
  },
};
