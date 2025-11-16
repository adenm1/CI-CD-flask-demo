import http from 'node:http';

const port = Number(process.env.MOCK_API_PORT || 8001);

const sessions = [
  {
    id: 1,
    title: 'Production deploy',
    description: 'Blue/green rollout',
    status: 'completed',
    difficulty: 'senior',
    started_at: new Date(Date.now() - 3600 * 1000 * 2).toISOString(),
    completed_at: new Date(Date.now() - 3600 * 1000 * 1.5).toISOString(),
    created_at: new Date(Date.now() - 3600 * 1000 * 3).toISOString(),
    updated_at: new Date(Date.now() - 3600 * 1000 * 1.5).toISOString()
  },
  {
    id: 2,
    title: 'Staging deploy',
    description: 'QA regression',
    status: 'in_progress',
    difficulty: 'mid',
    started_at: new Date(Date.now() - 3600 * 1000 * 1).toISOString(),
    completed_at: null,
    created_at: new Date(Date.now() - 3600 * 1000 * 1.2).toISOString(),
    updated_at: new Date(Date.now() - 3600 * 1000 * 0.5).toISOString()
  }
];

function send(res: http.ServerResponse, status: number, payload: any) {
  const body = JSON.stringify(payload);
  res.writeHead(status, {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization'
  });
  res.end(body);
}

function handleRequest(req: http.IncomingMessage, res: http.ServerResponse) {
  const method = req.method || 'GET';
  const urlObj = new URL(req.url || '/', `http://${req.headers.host}`);

  if (method === 'OPTIONS') {
    res.writeHead(204, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      'Access-Control-Allow-Methods': 'GET,POST,PATCH,DELETE,OPTIONS'
    });
    return res.end();
  }

  if (method === 'GET' && urlObj.pathname === '/health') {
    return send(res, 200, { status: 'healthy' });
  }

  if (method === 'GET' && urlObj.pathname === '/api/status') {
    return send(res, 200, {
      status: 'operational',
      successful_deployments: sessions.filter((s) => s.status === 'completed').length,
      failed_deployments: sessions.filter((s) => s.status === 'planned').length,
      active_pipelines: sessions.length,
      avg_build_time: 12.4,
      logs: [
        { id: 1, level: 'info', message: 'Mock deploy completed', timestamp: new Date().toISOString() }
      ]
    });
  }

  if (method === 'GET' && (urlObj.pathname === '/api/sessions/' || urlObj.pathname === '/api/sessions')) {
    return send(res, 200, { data: sessions });
  }

  if (method === 'POST' && (urlObj.pathname === '/api/auth/login' || urlObj.pathname === '/api/auth/register')) {
    let body = '';
    req.on('data', (chunk) => (body += chunk));
    req.on('end', () => {
      const payload = body ? JSON.parse(body) : {};
      send(res, 200, {
        token: 'mock-token',
        admin: { id: 1, username: payload.username || 'mock', role: 'owner' }
      });
    });
    return;
  }

  send(res, 404, { error: 'Not found' });
}

const server = http.createServer(handleRequest);
server.listen(port, () => {
  console.log(`Mock API running at http://localhost:${port}`);
});
