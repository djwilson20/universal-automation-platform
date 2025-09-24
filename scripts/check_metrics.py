#!/usr/bin/env python3
"""
Production metrics monitoring script for deployment validation.
"""

import argparse
import boto3
import time
from datetime import datetime, timedelta
import sys


def check_cloudwatch_metrics(environment: str) -> bool:
    """Check CloudWatch metrics for the specified environment."""

    cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=10)

    metrics_to_check = [
        {
            'MetricName': 'CPUUtilization',
            'Namespace': 'AWS/ECS',
            'Dimensions': [
                {'Name': 'ServiceName', 'Value': f'ai-automation-service'},
                {'Name': 'ClusterName', 'Value': f'ai-automation-{environment}'},
            ],
            'threshold': 80.0,
            'comparison': 'less_than'
        },
        {
            'MetricName': 'MemoryUtilization',
            'Namespace': 'AWS/ECS',
            'Dimensions': [
                {'Name': 'ServiceName', 'Value': f'ai-automation-service'},
                {'Name': 'ClusterName', 'Value': f'ai-automation-{environment}'},
            ],
            'threshold': 80.0,
            'comparison': 'less_than'
        },
        {
            'MetricName': 'TargetResponseTime',
            'Namespace': 'AWS/ApplicationELB',
            'Dimensions': [
                {'Name': 'LoadBalancer', 'Value': f'app/ai-automation-{environment}/12345'},
            ],
            'threshold': 2.0,
            'comparison': 'less_than'
        }
    ]

    all_metrics_healthy = True

    for metric in metrics_to_check:
        try:
            response = cloudwatch.get_metric_statistics(
                Namespace=metric['Namespace'],
                MetricName=metric['MetricName'],
                Dimensions=metric['Dimensions'],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Average']
            )

            if response['Datapoints']:
                latest_value = response['Datapoints'][-1]['Average']

                if metric['comparison'] == 'less_than':
                    is_healthy = latest_value < metric['threshold']
                else:
                    is_healthy = latest_value > metric['threshold']

                status = "✅ HEALTHY" if is_healthy else "❌ UNHEALTHY"
                print(f"{metric['MetricName']}: {latest_value:.2f} - {status}")

                if not is_healthy:
                    all_metrics_healthy = False
            else:
                print(f"{metric['MetricName']}: No data available")
                all_metrics_healthy = False

        except Exception as e:
            print(f"Error checking {metric['MetricName']}: {str(e)}")
            all_metrics_healthy = False

    return all_metrics_healthy


def check_application_health(environment: str) -> bool:
    """Check application-specific health endpoints."""

    import requests

    if environment == 'production':
        health_url = 'https://ai-automation-platform.com/health'
    elif environment == 'production-green':
        health_url = 'https://green.ai-automation-platform.com/health'
    else:
        health_url = f'https://{environment}.ai-automation-platform.com/health'

    try:
        response = requests.get(health_url, timeout=10)
        if response.status_code == 200:
            health_data = response.json()

            checks = [
                ('Database', health_data.get('database', False)),
                ('Cache', health_data.get('cache', False)),
                ('Storage', health_data.get('storage', False)),
                ('API', health_data.get('api', False))
            ]

            all_healthy = True
            for check_name, status in checks:
                status_icon = "✅" if status else "❌"
                print(f"{check_name} Health: {status_icon}")
                if not status:
                    all_healthy = False

            return all_healthy
        else:
            print(f"Health check failed with status {response.status_code}")
            return False

    except Exception as e:
        print(f"Health check request failed: {str(e)}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Check production metrics')
    parser.add_argument('--environment', required=True,
                       choices=['staging', 'production', 'production-green'],
                       help='Environment to check')

    args = parser.parse_args()

    print(f"🔍 Checking metrics for {args.environment} environment...")
    print("=" * 50)

    # Check CloudWatch metrics
    print("\n📊 CloudWatch Metrics:")
    cloudwatch_healthy = check_cloudwatch_metrics(args.environment)

    # Check application health
    print("\n🏥 Application Health:")
    app_healthy = check_application_health(args.environment)

    print("\n" + "=" * 50)

    if cloudwatch_healthy and app_healthy:
        print("✅ All metrics are healthy!")
        sys.exit(0)
    else:
        print("❌ Some metrics are unhealthy!")
        sys.exit(1)


if __name__ == '__main__':
    main()