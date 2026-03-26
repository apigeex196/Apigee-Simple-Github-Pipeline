#!/usr/bin/env python3
"""
ESP API client for fetching proxy details from mediatedResource endpoint.

INVENTORY LAYER - NON-AUTHORITATIVE
This module provides HEURISTIC inventory data from ESP API.
NOT FOR migration truth - use verification layer for authoritative data.

This module handles all HTTP communication with the ESP API,
including authentication and error handling.
"""

import os
import sys
from datetime import datetime
from typing import Dict, Any, List, Optional

import requests

# Import models
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from models import InventoryProxyRecord, SourceType, EvidenceLevel


class ESPClient:
    """Client for interacting with ESP mediatedResource API."""
    
    def __init__(
        self,
        base_url: str,
        appkey: Optional[str] = None,
        cert_file: Optional[str] = None,
        insecure: bool = False
    ):
        """
        Initialize ESP client.
        
        Args:
            base_url: Base URL for ESP API (e.g., https://api.corp.intranet)
            appkey: Application key for authentication (or set ESP_APPKEY env var)
            cert_file: Path to SSL certificate chain file
            insecure: Disable SSL verification (dev only)
        """
        self.base_url = base_url.rstrip("/")
        self.appkey = appkey or os.environ.get("ESP_APPKEY")
        self.cert_file = cert_file
        self.insecure = insecure
        
        if not self.appkey:
            print("ERROR: ESP_APPKEY is required. Set via --appkey or ESP_APPKEY environment variable.", file=sys.stderr)
            print("\nTo obtain an appkey:", file=sys.stderr)
            print("  1. Contact ESP team for read-only access", file=sys.stderr)
            print("  2. Request access to mediatedResource endpoint", file=sys.stderr)
            print("  3. Set: export ESP_APPKEY='your-key-here'", file=sys.stderr)
            sys.exit(1)
    
    def _get_headers(self) -> Dict[str, str]:
        """Build request headers with authentication."""
        return {
            "X-Application-Key": self.appkey,
            "Accept": "application/json",
            "x-username": "apienablement"
        }
    
    def _get_verify(self) -> bool:
        """Determine SSL verification setting."""
        if self.insecure:
            return False
        if self.cert_file and os.path.exists(self.cert_file):
            return self.cert_file
        return True

    def _debug_enabled(self) -> bool:
        """Return True when lightweight ESP debug logging is enabled."""
        val = os.environ.get("ESP_DEBUG", "")
        return val.lower() in {"1", "true", "yes", "on"}

    def _debug(self, message: str) -> None:
        """Print debug message only when ESP_DEBUG is enabled."""
        if self._debug_enabled():
            print(f"[esp-debug] {message}", file=sys.stderr)
    
    def fetch_proxies(self, environment: str) -> List[Dict[str, Any]]:
        """
        Fetch all proxies for a given environment.
        
        Args:
            environment: Environment name (test1, sandbox, mock, prod)
        
        Returns:
            List of proxy dictionaries
        
        Raises:
            SystemExit: On API error or invalid response
        """
        # Match legacy behavior: test1 uses dedicated host with no environment query param.
        if environment == "test1":
            actual_base_url = "https://api-test1.test.intranet"
            params: Dict[str, str] = {}
        else:
            actual_base_url = self.base_url
            params = {"environment": environment}

        endpoint = f"{actual_base_url}/Enterprise/v1/Routing/mediatedResource"
        
        headers = self._get_headers()
        verify = self._get_verify()
        
        if not verify:
            print("⚠️  WARNING: SSL verification disabled (--insecure)", file=sys.stderr)
        
        try:
            response = requests.get(
                endpoint,
                headers=headers,
                params=params,
                verify=verify,
                timeout=30
            )
            
            print(f"ESP API: {response.url}")
            print(f"Status: {response.status_code}")
            
            if response.status_code == 401:
                print("\nERROR: Authentication failed (401 Unauthorized)", file=sys.stderr)
                print("Check your ESP_APPKEY is valid and has access to mediatedResource endpoint.", file=sys.stderr)
                sys.exit(2)
            
            if response.status_code == 403:
                print("\nERROR: Access forbidden (403 Forbidden)", file=sys.stderr)
                print("Your appkey may not have access to this environment.", file=sys.stderr)
                sys.exit(2)
            
            if response.status_code != 200:
                print(f"\nERROR: API returned status {response.status_code}", file=sys.stderr)
                print(f"Response: {response.text[:500]}", file=sys.stderr)
                sys.exit(3)
            
            # Parse JSON response
            try:
                data = response.json()
            except ValueError as e:
                print(f"\nERROR: Invalid JSON response: {e}", file=sys.stderr)
                print(f"Response text: {response.text[:500]}", file=sys.stderr)
                sys.exit(4)
            
            # Extract items from response by shape priority.
            shape = "unknown"
            if isinstance(data, list):
                items = data
                shape = "list"
            elif isinstance(data, dict):
                top_keys = list(data.keys())
                self._debug(f"response top-level keys: {top_keys[:15]}")

                if isinstance(data.get("mediatedResource"), list):
                    items = data["mediatedResource"]
                    shape = "dict.mediatedResource"
                elif isinstance(data.get("items"), list):
                    items = data["items"]
                    shape = "dict.items"
                elif isinstance(data.get("proxies"), list):
                    items = data["proxies"]
                    shape = "dict.proxies"
                elif any(key in data for key in ["resourceName", "mediatedResourceId", "name", "proxyName"]):
                    items = [data]
                    shape = "dict.single_proxy"
                else:
                    # Unknown wrapper/object: do NOT treat as proxy payload.
                    items = []
                    shape = "dict.unknown"
                    print("WARNING: ESP response shape was not recognized; returning 0 proxies.", file=sys.stderr)
            else:
                print(f"\nERROR: Unexpected response format: {type(data)}", file=sys.stderr)
                sys.exit(5)

            self._debug(f"detected response shape: {shape}")
            self._debug(f"extracted proxy count: {len(items)}")
            
            print(f"✓ Found {len(items)} proxy/proxies in environment '{environment}'")
            return items
            
        except requests.exceptions.SSLError as e:
            print(f"\nERROR: SSL verification failed: {e}", file=sys.stderr)
            print("\nOptions:", file=sys.stderr)
            print("  1. Set --ca-bundle /path/to/cert-chain.pem", file=sys.stderr)
            print("  2. Use --insecure (dev only, not recommended)", file=sys.stderr)
            sys.exit(6)
        
        except requests.exceptions.ConnectionError as e:
            print(f"\nERROR: Connection failed: {e}", file=sys.stderr)
            print(f"Check that base URL is correct: {self.base_url}", file=sys.stderr)
            sys.exit(7)
        
        except requests.exceptions.Timeout:
            print(f"\nERROR: Request timed out after 30 seconds", file=sys.stderr)
            sys.exit(8)
        
        except requests.exceptions.RequestException as e:
            print(f"\nERROR: Request failed: {e}", file=sys.stderr)
            sys.exit(9)
    
    def find_proxy(self, environment: str, proxy_name: str) -> Optional[Dict[str, Any]]:
        """
        Find a specific proxy by name in the given environment.
        
        Args:
            environment: Environment name
            proxy_name: Proxy name to find (case-insensitive)
        
        Returns:
            Proxy dictionary if found, None otherwise
        """
        proxies = self.fetch_proxies(environment)
        
        proxy_name_lower = proxy_name.lower().strip()
        
        for proxy in proxies:
            # Try multiple fields to match proxy name
            candidates = [
                proxy.get("name"),
                proxy.get("proxyName"),
                proxy.get("apiName"),
                proxy.get("id"),
            ]
            
            for candidate in candidates:
                if isinstance(candidate, str) and candidate.lower().strip() == proxy_name_lower:
                    return proxy
        
        # Not found - show close matches
        print(f"\n⚠️  Proxy '{proxy_name}' not found in environment '{environment}'", file=sys.stderr)
        print(f"\nAvailable proxies ({len(proxies)}):", file=sys.stderr)
        
        for i, proxy in enumerate(proxies[:10], 1):  # Show first 10
            name = proxy.get("name") or proxy.get("proxyName") or proxy.get("id") or "unknown"
            print(f"  {i}. {name}", file=sys.stderr)
        
        if len(proxies) > 10:
            print(f"  ... and {len(proxies) - 10} more", file=sys.stderr)
        
        return None
    
    def fetch_inventory_records(
        self,
        environment: str
    ) -> List[InventoryProxyRecord]:
        """
        Fetch inventory records (NON-AUTHORITATIVE).
        
        Returns InventoryProxyRecord objects clearly marked as heuristic.
        NOT FOR final migration truth.
        
        Args:
            environment: Environment name (test1, sandbox, mock, prod)
        
        Returns:
            List of InventoryProxyRecord objects
        """
        raw_proxies = self.fetch_proxies(environment)
        
        inventory_records = []
        for raw_proxy in raw_proxies:
            record = self._raw_to_inventory_record(raw_proxy, environment)
            inventory_records.append(record)
        
        return inventory_records
    
    def find_proxy_inventory(
        self,
        environment: str,
        proxy_name: str
    ) -> Optional[InventoryProxyRecord]:
        """
        Find proxy and return inventory record (NON-AUTHORITATIVE).
        
        Args:
            environment: Environment name
            proxy_name: Proxy name to find
        
        Returns:
            InventoryProxyRecord if found, None otherwise
        """
        raw_proxy = self.find_proxy(environment, proxy_name)
        if not raw_proxy:
            return None
        
        return self._raw_to_inventory_record(raw_proxy, environment)
    
    def _raw_to_inventory_record(
        self,
        raw_proxy: Dict[str, Any],
        environment: str
    ) -> InventoryProxyRecord:
        """
        Convert raw ESP response to InventoryProxyRecord.
        
        Clearly marks data as heuristic and non-authoritative.
        """
        # Extract name (try multiple fields)
        name = (
            raw_proxy.get("name") or
            raw_proxy.get("proxyName") or
            raw_proxy.get("apiName") or
            raw_proxy.get("id") or
            "unknown"
        )
        
        # Extract optional fields
        base_path = raw_proxy.get("basePath")
        target_endpoint = raw_proxy.get("targetEndpoint") or raw_proxy.get("target")
        virtual_host = raw_proxy.get("virtualHost")
        description = raw_proxy.get("description")
        
        # Extract policy info if available
        detected_policies = []
        policies_raw = raw_proxy.get("policies", [])
        if isinstance(policies_raw, list):
            for policy in policies_raw:
                if isinstance(policy, dict):
                    policy_type = policy.get("type") or policy.get("policyType")
                    if policy_type:
                        detected_policies.append(policy_type)
                elif isinstance(policy, str):
                    detected_policies.append(policy)
        
        # Heuristic auth detection (may not be accurate)
        frontend_auth = self._guess_frontend_auth(raw_proxy)
        backend_auth = self._guess_backend_auth(raw_proxy)
        mtls_level = self._guess_mtls_evidence_level(raw_proxy)
        
        notes = [
            "⚠️  INVENTORY DATA - HEURISTIC AND NON-AUTHORITATIVE",
            "Source: ESP mediatedResource API",
            "Fields may be incomplete, inaccurate, or outdated",
            "Run 'verify' command for authoritative data from OPDK Management API"
        ]
        
        return InventoryProxyRecord(
            name=name,
            environment=environment,
            source_type=SourceType.ESP,
            evidence_level=EvidenceLevel.HEURISTIC,
            authoritative=False,
            base_path=base_path,
            target_endpoint=target_endpoint,
            virtual_host=virtual_host,
            description=description,
            detected_policies=detected_policies,
            frontend_auth_type=frontend_auth,
            backend_auth_type=backend_auth,
            mtls_evidence_level=mtls_level,
            recommended_template=None,  # Set by analyzer
            raw_data=raw_proxy,
            extracted_at=datetime.utcnow().isoformat() + "Z",
            notes=notes
        )
    
    def _guess_frontend_auth(self, raw_proxy: Dict[str, Any]) -> Optional[str]:
        """Heuristic guess of frontend auth type from ESP data."""
        # Look for auth-related fields in policies
        policies = raw_proxy.get("policies", [])
        if isinstance(policies, list):
            for policy in policies:
                if isinstance(policy, dict):
                    policy_type = (policy.get("type") or policy.get("policyType") or "").lower()
                    if "oauth" in policy_type:
                        return "oauth"
                    if "apikey" in policy_type:
                        return "apikey"
                    if "jwt" in policy_type or "verify-jwt" in policy_type:
                        return "jwt"
        
        # Check authentication field directly
        auth_field = raw_proxy.get("authentication")
        if auth_field:
            return str(auth_field).lower()
        
        return None
    
    def _guess_backend_auth(self, raw_proxy: Dict[str, Any]) -> Optional[str]:
        """Heuristic guess of backend auth type from ESP data."""
        policies = raw_proxy.get("policies", [])
        if isinstance(policies, list):
            for policy in policies:
                if isinstance(policy, dict):
                    policy_type = (policy.get("type") or policy.get("policyType") or "").lower()
                    if "client" in policy_type and "cert" in policy_type:
                        return "clientcert"
                    if "mtls" in policy_type:
                        return "mtls"
                    if "basic" in policy_type and "auth" in policy_type:
                        return "basic"
        
        # Check for SSL/TLS config
        ssl_info = raw_proxy.get("sslInfo") or raw_proxy.get("tlsInfo")
        if ssl_info:
            if isinstance(ssl_info, dict):
                if ssl_info.get("clientAuth") or ssl_info.get("clientCertificate"):
                    return "clientcert"
        
        return None
    
    def _guess_mtls_evidence_level(self, raw_proxy: Dict[str, Any]) -> Optional[str]:
        """Heuristic guess of mTLS evidence level."""
        # Look for strong indicators
        backend_auth = self._guess_backend_auth(raw_proxy)
        
        if backend_auth in ("clientcert", "mtls"):
            # Check if there's cert config
            ssl_info = raw_proxy.get("sslInfo") or raw_proxy.get("tlsInfo")
            if ssl_info and isinstance(ssl_info, dict):
                if ssl_info.get("clientCertificate"):
                    return "high"
                else:
                    return "medium"
            return "medium"
        
        # Check policies for any cert-related hints
        policies = raw_proxy.get("policies", [])
        if isinstance(policies, list):
            for policy in policies:
                if isinstance(policy, dict):
                    policy_type = (policy.get("type") or policy.get("policyType") or "").lower()
                    if "cert" in policy_type:
                        return "low"
        
        return "none"
