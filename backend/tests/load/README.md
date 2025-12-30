# Load Tests

Performance and scalability validation tests for Phase III.

## load_test.py

Validates SC-005: System handles 100 concurrent conversations without degradation.

### Requirements

```bash
pip install httpx
```

### Usage

```bash
# Quick test with 10 users:
python backend/tests/load/load_test.py --users 10 --duration 30

# Production validation (SC-005 - 100 concurrent users):
python backend/tests/load/load_test.py --users 100 --duration 60

# Custom endpoint and token:
python backend/tests/load/load_test.py \
  --url https://api.yourapp.com \
  --token YOUR_JWT_TOKEN \
  --users 100 \
  --duration 120
```

### Options

- `--url URL`: Base URL of the API (default: http://localhost:8000)
- `--users N`: Number of concurrent users (default: 10)
- `--duration SECONDS`: Test duration in seconds (default: 30)
- `--token TOKEN`: JWT token for authentication (default: test-token)

### Success Criteria Validated

- **SC-001**: p95 latency <2s for agent responses
- **SC-005**: 100 concurrent conversations without degradation (<5% failure rate)

### Interpreting Results

**Good Results:**
- Success rate: >95%
- p95 latency: <2000ms
- p99 latency: <3000ms
- Throughput: >10 req/s

**Warning Signs:**
- Success rate: <90% (investigate errors)
- p95 latency: >2000ms (violates SC-001)
- High error rate (>10%)

**Critical Issues:**
- Success rate: <50% (system overloaded)
- Frequent timeouts (database bottleneck)
- Memory errors (resource exhaustion)

### Before Running

1. **Start the backend server:**
   ```bash
   cd backend
   uvicorn src.main:app --reload
   ```

2. **Get a valid JWT token:**
   ```bash
   # Login via Phase II auth to get token
   curl -X POST http://localhost:8000/api/auth/signin \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"password123"}'
   ```

3. **Ensure OpenAI API key is configured:**
   ```bash
   grep OPENAI_API_KEY backend/.env
   ```

4. **Start with small load first:**
   ```bash
   # Start with 10 users
   python backend/tests/load/load_test.py --users 10 --duration 30
   ```

5. **Gradually increase to 100 users:**
   ```bash
   python backend/tests/load/load_test.py --users 50 --duration 30
   python backend/tests/load/load_test.py --users 100 --duration 60
   ```

### Alternative: k6 Load Testing

For more advanced load testing, use k6:

```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 50 },   // Ramp up to 50 users
    { duration: '3m', target: 100 },  // Stay at 100 users
    { duration: '1m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<2000'], // SC-001: p95 <2s
    http_req_failed: ['rate<0.05'],    // SC-005: <5% failures
  },
};

export default function () {
  const url = 'http://localhost:8000/api/1/chat';
  const payload = JSON.stringify({ message: 'Add task: Test task' });
  const params = {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer YOUR_JWT_TOKEN',
    },
  };

  const res = http.post(url, payload, params);

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response has agent reply': (r) => r.json('response') !== undefined,
  });

  sleep(2); // 2 second delay between requests
}
```

Run with k6:
```bash
k6 run load-test.js
```

### Monitoring During Load Test

Monitor these metrics during the test:

1. **Application logs:**
   ```bash
   tail -f backend/logs/app.log | grep -i error
   ```

2. **Database connections:**
   ```sql
   SELECT count(*) FROM pg_stat_activity WHERE datname = 'your_database';
   ```

3. **OpenAI API usage:**
   - Check OpenAI dashboard for rate limits
   - Monitor token usage and costs

4. **System resources:**
   ```bash
   htop  # CPU and memory usage
   ```

### Troubleshooting

**High latency (>2s):**
- Check database query performance
- Review OpenAI API response times
- Check network latency

**High error rate:**
- Check OpenAI API rate limits
- Verify database connection pool size
- Check application logs for errors

**Timeouts:**
- Increase timeout values
- Scale database resources
- Add connection pooling

**Memory errors:**
- Check for memory leaks
- Increase container/server memory
- Review conversation context size

### Cost Considerations

**OpenAI API Costs:**
- 100 users × 60 seconds = ~3000 requests
- Each request: ~$0.01 (GPT-4) or ~$0.001 (GPT-3.5-turbo)
- Total cost: $30 (GPT-4) or $3 (GPT-3.5-turbo)

**Recommendation:**
- Use GPT-3.5-turbo for load testing
- Start with shorter durations (30s)
- Monitor costs in OpenAI dashboard
