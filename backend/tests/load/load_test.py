#!/usr/bin/env python3
"""
Load test for Phase III chat endpoint (T079).

Validates SC-005: System handles 100 concurrent conversations without degradation.

Requirements:
- pip install httpx asyncio

Usage:
    # Test with 10 concurrent users:
    python backend/tests/load/load_test.py --users 10 --duration 30

    # Test with 100 concurrent users (SC-005):
    python backend/tests/load/load_test.py --users 100 --duration 60

    # Test with custom endpoint:
    python backend/tests/load/load_test.py --url http://localhost:8000 --users 100
"""

import argparse
import asyncio
import time
from collections import defaultdict
from datetime import datetime
from typing import Dict, List

import httpx


class LoadTester:
    """
    Load tester for chat endpoint.

    Simulates multiple concurrent users sending chat messages.
    """

    def __init__(
        self,
        base_url: str,
        num_users: int,
        duration_seconds: int,
        jwt_token: str,
    ):
        self.base_url = base_url.rstrip("/")
        self.num_users = num_users
        self.duration_seconds = duration_seconds
        self.jwt_token = jwt_token

        # Metrics
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.latencies: List[float] = []
        self.errors: Dict[str, int] = defaultdict(int)
        self.start_time = None
        self.end_time = None

    async def send_chat_message(
        self, client: httpx.AsyncClient, user_id: int, message: str
    ) -> tuple[bool, float, str]:
        """
        Send a chat message to the API.

        Returns:
            (success, latency_ms, error_message)
        """
        url = f"{self.base_url}/api/{user_id}/chat"
        headers = {
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json",
        }
        data = {"message": message}

        start = time.time()
        try:
            response = await client.post(url, json=data, headers=headers, timeout=10.0)
            latency_ms = (time.time() - start) * 1000

            if response.status_code == 200:
                return True, latency_ms, ""
            else:
                return False, latency_ms, f"HTTP {response.status_code}"

        except Exception as e:
            latency_ms = (time.time() - start) * 1000
            return False, latency_ms, str(type(e).__name__)

    async def user_session(self, user_id: int, client: httpx.AsyncClient):
        """
        Simulate a single user's session.

        Sends messages for the duration of the test.
        """
        messages = [
            "Add task: Buy groceries",
            "What tasks do I have?",
            "Complete the grocery task",
            "Show me my completed tasks",
            "Add task: Call dentist",
        ]
        message_index = 0

        while (time.time() - self.start_time) < self.duration_seconds:
            message = messages[message_index % len(messages)]
            success, latency, error = await self.send_chat_message(
                client, user_id, message
            )

            self.total_requests += 1
            self.latencies.append(latency)

            if success:
                self.successful_requests += 1
            else:
                self.failed_requests += 1
                self.errors[error] += 1

            message_index += 1

            # Wait between messages (simulate human typing)
            await asyncio.sleep(2)

    async def run(self):
        """
        Run the load test.
        """
        print("=" * 60)
        print(f"🔥 Load Test - {self.num_users} Concurrent Users")
        print("=" * 60)
        print(f"Target: {self.base_url}")
        print(f"Duration: {self.duration_seconds}s")
        print(f"Users: {self.num_users}")
        print()
        print("Starting test...")
        print()

        self.start_time = time.time()

        # Create HTTP client with connection pooling
        async with httpx.AsyncClient(
            limits=httpx.Limits(
                max_connections=self.num_users * 2, max_keepalive_connections=self.num_users
            )
        ) as client:
            # Launch user sessions concurrently
            tasks = [
                self.user_session(user_id, client)
                for user_id in range(1, self.num_users + 1)
            ]
            await asyncio.gather(*tasks)

        self.end_time = time.time()

        self._print_results()

    def _print_results(self):
        """
        Print test results and validate success criteria.
        """
        duration = self.end_time - self.start_time

        print()
        print("=" * 60)
        print("📊 Load Test Results")
        print("=" * 60)
        print(f"Duration: {duration:.2f}s")
        print(f"Total requests: {self.total_requests}")
        print(f"Successful: {self.successful_requests}")
        print(f"Failed: {self.failed_requests}")
        print(f"Success rate: {(self.successful_requests / max(self.total_requests, 1)) * 100:.2f}%")
        print()

        if self.latencies:
            self.latencies.sort()
            p50 = self.latencies[len(self.latencies) // 2]
            p95 = self.latencies[int(len(self.latencies) * 0.95)]
            p99 = self.latencies[int(len(self.latencies) * 0.99)]
            avg = sum(self.latencies) / len(self.latencies)

            print("Latency:")
            print(f"  Average: {avg:.2f}ms")
            print(f"  p50: {p50:.2f}ms")
            print(f"  p95: {p95:.2f}ms")
            print(f"  p99: {p99:.2f}ms")
            print()

            # Validate SC-001: p95 <2s
            sc001_pass = p95 < 2000
            print(f"SC-001 (p95 <2s): {p95:.2f}ms - {'✅ PASS' if sc001_pass else '❌ FAIL'}")

        if self.errors:
            print()
            print("Errors:")
            for error, count in sorted(self.errors.items(), key=lambda x: -x[1]):
                print(f"  {error}: {count}")

        print()

        # Validate SC-005: 100 concurrent conversations
        if self.num_users >= 100:
            throughput = self.total_requests / duration
            degradation = self.failed_requests / max(self.total_requests, 1)
            sc005_pass = degradation < 0.05  # Less than 5% failures

            print(
                f"SC-005 (100 concurrent): {self.num_users} users, "
                f"{degradation * 100:.2f}% failures - {'✅ PASS' if sc005_pass else '❌ FAIL'}"
            )
            print(f"  Throughput: {throughput:.2f} req/s")

        print()
        print("=" * 60)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Load test for Phase III chat endpoint",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test with 10 users for 30 seconds:
  python backend/tests/load/load_test.py --users 10 --duration 30

  # Test SC-005 (100 concurrent users):
  python backend/tests/load/load_test.py --users 100 --duration 60

  # Test with custom URL and token:
  python backend/tests/load/load_test.py --url http://localhost:8000 --token YOUR_JWT --users 50
        """,
    )

    parser.add_argument(
        "--url",
        default="http://localhost:8000",
        help="Base URL of the API (default: http://localhost:8000)",
    )

    parser.add_argument(
        "--users",
        type=int,
        default=10,
        help="Number of concurrent users (default: 10)",
    )

    parser.add_argument(
        "--duration",
        type=int,
        default=30,
        help="Test duration in seconds (default: 30)",
    )

    parser.add_argument(
        "--token",
        default="test-token",
        help="JWT token for authentication (default: test-token)",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    tester = LoadTester(
        base_url=args.url,
        num_users=args.users,
        duration_seconds=args.duration,
        jwt_token=args.token,
    )

    asyncio.run(tester.run())
