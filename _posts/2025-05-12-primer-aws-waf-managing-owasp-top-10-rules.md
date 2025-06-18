---
layout: post
title: "Primer AWS WAF - Managing OWASP top 10 rules"
date: 2025-05-12
author: unattributed
categories: [webappsec]
tags: [awsconfig, webapp, burp, dvwa, owasp, owasp-wstg, owasp-top-10]
---

# Implementing AWS Config for WAF: A Detailed Guide to Enforce OWASP Top 10 Protections

## Introduction

In today's threat landscape, web applications face constant attacks targeting common vulnerabilities. The Open Web Application Security Project (OWASP) Top 10 outlines the most critical web application security risks. AWS Web Application Firewall (WAF) provides robust protection against these threats, but ensuring continuous compliance with security best practices requires proper monitoring and enforcement.

This comprehensive guide will walk you through implementing AWS Config to monitor and enforce AWS WAF rules that protect against OWASP Top 10 vulnerabilities, using AWS Managed Rule Groups as referenced in the [AWS WAF Developer Guide](https://docs.aws.amazon.com/waf/latest/developerguide/aws-managed-rule-groups-baseline.html).

## Why AWS Config for WAF?

AWS Config provides several key benefits for managing WAF security:

1. **Continuous Monitoring**: Track configuration changes to your WAF rules in real-time
2. **Compliance Assessment**: Evaluate WAF configurations against security best practices
3. **Automated Remediation**: Trigger actions when non-compliant changes are detected
4. **Historical Tracking**: Maintain a complete history of WAF configuration changes

## Prerequisites

Before implementing this solution, ensure you have:

1. An AWS account with appropriate permissions
2. AWS WAF deployed in your preferred regions (CloudFront or Regional)
3. AWS Config service enabled in your account
4. Basic understanding of OWASP Top 10 vulnerabilities

## Step 1: Enable AWS Config

First, we need to set up AWS Config to monitor our WAF resources:

1. Open the AWS Config console
2. Navigate to "Settings" and ensure recording is turned on
3. Specify an S3 bucket for configuration history storage
4. Create an SNS topic for notifications (recommended)
5. Select "Record all resources supported in this region" or specifically select WAF resources

```bash
# AWS CLI command to enable AWS Config
aws configservice subscribe --s3-bucket your-config-bucket \
--sns-topic arn:aws:sns:region:account-id:your-topic \
--iam-role arn:aws:iam::account-id:role/your-config-role
```

## Step 2: Deploy AWS Managed Rules for OWASP Top 10

As referenced in the [AWS documentation](https://docs.aws.amazon.com/waf/latest/developerguide/aws-managed-rule-groups-baseline.html), AWS provides managed rule groups that align with OWASP Top 10 protections:

1. **AWSManagedRulesCommonRuleSet**: Protects against common web exploits (maps to multiple OWASP categories)
2. **AWSManagedRulesSQLiRuleSet**: Specifically targets SQL injection (OWASP A1)
3. **AWSManagedRulesLinuxRuleSet**: Protects against Linux-specific attacks
4. **AWSManagedRulesPHPRuleSet**: Protects against PHP-specific attacks
5. **AWSManagedRulesWordPressRuleSet**: For WordPress protections

### Implementation Steps:

1. Navigate to AWS WAF in the console
2. Create a new Web ACL or select an existing one
3. Under "Add rules", select "Add managed rule groups"
4. Add the relevant rule groups with appropriate actions (Block, Count, etc.)

```bash
# Example AWS CLI command to associate managed rules with a Web ACL
aws wafv2 associate-web-acl \
--web-acl-arn arn:aws:wafv2:region:account-id:global/webacl/your-web-acl/your-acl-id \
--resource-arn arn:aws:cloudfront::account-id:distribution/your-distribution-id
```

## Step 3: Create AWS Config Rules for WAF Compliance

Now we'll create custom AWS Config rules to ensure our WAF implementation remains compliant with OWASP protections.

### Rule 1: Verify OWASP Core Rule Set is Enabled

This rule checks that the AWSManagedRulesCommonRuleSet is enabled in all WAF Web ACLs.

1. Navigate to AWS Config > Rules
2. Click "Add rule"
3. Search for "waf" and select "wafv2-webacl-resource-policy" as the base rule
4. Configure with the following parameters:

```json
{
  "webaclName": "*",
  "managedRuleGroupConfigs": [
    {
      "name": "AWSManagedRulesCommonRuleSet",
      "vendorName": "AWS",
      "enabled": true
    }
  ]
}
```

### Rule 2: Verify SQL Injection Protection is Enabled

Ensure the SQL injection rule set is active:

```json
{
  "webaclName": "*",
  "managedRuleGroupConfigs": [
    {
      "name": "AWSManagedRulesSQLiRuleSet",
      "vendorName": "AWS",
      "enabled": true
    }
  ]
}
```

### Rule 3: Verify WAF is Attached to All Resources

Create a rule to ensure all applicable resources have WAF protection:

```bash
# This requires a custom Lambda function to evaluate
aws configservice put-config-rule \
--config-rule '{
  "ConfigRuleName": "waf-attached-to-resources",
  "Description": "Checks that all applicable resources have WAF protection",
  "Scope": {
    "ComplianceResourceTypes": ["AWS::CloudFront::Distribution", "AWS::ElasticLoadBalancingV2::LoadBalancer"]
  },
  "Source": {
    "Owner": "CUSTOM_LAMBDA",
    "SourceIdentifier": "arn:aws:lambda:region:account-id:function:your-lambda-function",
    "SourceDetails": [
      {
        "EventSource": "aws.config",
        "MessageType": "ConfigurationItemChangeNotification"
      }
    ]
  },
  "InputParameters": "{}"
}'
```

## Step 4: Set Up Automated Remediation

When AWS Config detects non-compliant WAF configurations, we can automate remediation:

1. Create an SNS topic to receive compliance notifications
2. Configure AWS Lambda functions to remediate common issues
3. Set up EventBridge rules to trigger remediation

### Example Remediation for Missing OWASP Rule Set:

```python
import boto3

def lambda_handler(event, context):
    wafv2 = boto3.client('wafv2')
    
    # Get non-compliant Web ACL details from Config event
    webacl_arn = event['detail']['resourceId']
    region = event['detail']['awsRegion']
    
    # Get current Web ACL configuration
    webacl = wafv2.get_web_acl(
        Name=webacl_arn.split('/')[-1],
        Scope='REGIONAL',  # or 'CLOUDFRONT'
        Id=webacl_arn.split('/')[-2]
    )
    
    # Add missing OWASP rule set
    new_rules = webacl['WebACL']['Rules']
    new_rules.append({
        'Name': 'AWS-AWSManagedRulesCommonRuleSet',
        'Priority': 0,
        'Statement': {
            'ManagedRuleGroupStatement': {
                'VendorName': 'AWS',
                'Name': 'AWSManagedRulesCommonRuleSet'
            }
        },
        'OverrideAction': {'None': {}},
        'VisibilityConfig': {
            'SampledRequestsEnabled': True,
            'CloudWatchMetricsEnabled': True,
            'MetricName': 'AWS-AWSManagedRulesCommonRuleSet'
        }
    })
    
    # Update Web ACL
    wafv2.update_web_acl(
        Name=webacl['WebACL']['Name'],
        Scope='REGIONAL',
        Id=webacl['WebACL']['Id'],
        DefaultAction=webacl['WebACL']['DefaultAction'],
        Rules=new_rules,
        VisibilityConfig=webacl['WebACL']['VisibilityConfig']
    )
    
    return {
        'statusCode': 200,
        'body': 'Successfully remediated Web ACL'
    }
```

## Step 5: Configure Notifications and Reporting

Set up alerts and reporting for WAF compliance status:

1. Create an Amazon EventBridge rule for AWS Config compliance changes
2. Set up SNS notifications for critical compliance failures
3. Configure AWS Security Hub for centralized security findings
4. Create Amazon QuickSight dashboards for compliance visualization

```bash
# Create EventBridge rule for WAF compliance events
aws events put-rule \
--name "waf-compliance-events" \
--event-pattern '{
  "source": ["aws.config"],
  "detail-type": ["Config Rules Compliance Change"],
  "detail": {
    "configRuleName": [
      "waf-owasp-core-ruleset-enabled",
      "waf-sqli-protection-enabled"
    ]
  }
}'
```

## Best Practices for Ongoing Management

1. **Regular Rule Review**: Periodically review WAF rules and adjust sensitivity as needed
2. **Log Analysis**: Enable WAF logging to CloudWatch or S3 for attack pattern analysis
3. **Testing**: Regularly test your WAF rules with controlled attack simulations
4. **Update Strategy**: Plan for regular updates to managed rule groups as new threats emerge
5. **Custom Rules**: Supplement managed rules with custom rules for application-specific protections

## Advanced Configuration Options

### Geo-Blocking Implementation

Add geographic restrictions to complement OWASP protections:

```json
{
  "Name": "GeoBlockNonAllowedCountries",
  "Priority": 1,
  "Statement": {
    "NotStatement": {
      "Statement": {
        "GeoMatchStatement": {
          "CountryCodes": ["US", "CA", "GB", "DE"]
        }
      }
    }
  },
  "Action": {
    "Block": {}
  },
  "VisibilityConfig": {
    "SampledRequestsEnabled": true,
    "CloudWatchMetricsEnabled": true,
    "MetricName": "GeoBlock"
  }
}
```

### Rate-Based Rules

Protect against brute force attacks (OWASP A2):

```json
{
  "Name": "RateLimitLoginAttempts",
  "Priority": 2,
  "Statement": {
    "RateBasedStatement": {
      "Limit": 100,
      "AggregateKeyType": "IP",
      "ScopeDownStatement": {
        "ByteMatchStatement": {
          "SearchString": "/login",
          "FieldToMatch": {
            "UriPath": {}
          },
          "TextTransformations": [
            {
              "Priority": 0,
              "Type": "NONE"
            }
          ],
          "PositionalConstraint": "CONTAINS"
        }
      }
    }
  },
  "Action": {
    "Block": {}
  },
  "VisibilityConfig": {
    "SampledRequestsEnabled": true,
    "CloudWatchMetricsEnabled": true,
    "MetricName": "RateLimitLogin"
  }
}
```

## Troubleshooting Common Issues

1. **False Positives**: Adjust rule sensitivity or create allow lists for legitimate traffic
2. **Performance Impact**: Monitor latency and adjust rule priorities as needed
3. **Rule Conflicts**: Ensure proper rule priority ordering to prevent unintended interactions
4. **Logging Issues**: Verify WAF logs are properly configured and delivered

## Conclusion

Implementing AWS Config to monitor and enforce AWS WAF configurations for OWASP Top 10 protections provides a robust security posture for your web applications. By following this guide and referencing the [AWS WAF Developer Guide](https://docs.aws.amazon.com/waf/latest/developerguide/aws-managed-rule-groups-baseline.html), you can establish continuous compliance monitoring, automated remediation, and comprehensive visibility into your web application security controls.

Remember that security is an ongoing process. Regularly review your WAF configurations, analyze traffic patterns, and adjust your rules to maintain optimal protection against evolving threats while minimizing impact on legitimate traffic.

## Additional Resources

1. [AWS WAF Developer Guide](https://docs.aws.amazon.com/waf/latest/developerguide/)
2. [OWASP Top 10 Documentation](https://owasp.org/www-project-top-ten/)
3. [AWS Config Best Practices](https://docs.aws.amazon.com/config/latest/developerguide/best-practices.html)
4. [AWS Security Hub Integration Guide](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-integrations.html)

[🔝 Back to Top](#implementing-aws-config-for-waf-a-detailed-guide-to-enforce-owasp-top-10-protections)