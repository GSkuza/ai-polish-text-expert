# Performance Tester Agent

## Description
Agent responsible for testing and monitoring the performance of AI Polish Text Expert.

## Capabilities
- Load testing
- Response time measurement
- Memory and CPU profiling
- Performance regression detection

## Triggers
- On every release
- Scheduled daily at 02:00 UTC

## Configuration
```json
{
  "agent": "performance-tester",
  "thresholds": {
    "responseTime": 200,
    "memoryUsage": 512,
    "cpuUsage": 80
  }
}
```
