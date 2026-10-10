from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any
import re
import pandas as pd
from .security import redact

@dataclass
class QueryResult:
    intent: str
    answer: str
    data: Dict[str, Any]

class PAIDEngine:
    def __init__(self, data: Dict[str, pd.DataFrame], role: str = "internal") -> None:
        self.data = data
        self.role = role

    # --- Intent classification (very simple for demo) ---
    def classify(self, q: str) -> str:
        ql = q.lower()
        if any(k in ql for k in ["which customers", "who uses", "customers use", "list customers"]):
            return "who_uses_service"
        if "sunset" in ql or "end of life" in ql or "eol" in ql:
            return "sunset_versions_by_customer"
        if any(k in ql for k in ["impacted", "impact", "incident", "outage"]):
            return "service_impact"
        if "gap" in ql or "optimization" in ql or "unused" in ql:
            return "portfolio_gaps"
        return "generic"

    # --- Handlers ---
    def who_uses_service(self, q: str) -> QueryResult:
        m = re.search(r"service\s+([\w\-\s]+)", q, re.I)
        service = m.group(1).strip() if m else None
        cust_df = self.data['customers']
        if service is None:
            # fallback: try last token
            service = q.split()[-1]
        matches = cust_df[cust_df['services'].apply(lambda lst: any(service.lower() in s['name'].lower() for s in lst))]
        customers = sorted(matches['customer'].unique().tolist())
        answer = f"Customers using service '{service}': {', '.join(customers) if customers else 'None found'}"
        return QueryResult("who_uses_service", answer, {"service": service, "customers": customers})

    def sunset_versions_by_customer(self, q: str) -> QueryResult:
        m = re.search(r"customer\s+([\w\-\s]+)", q, re.I)
        customer = m.group(1).strip() if m else None
        cust_df = self.data['customers']
        port_df = self.data['portfolio']
        if customer is None:
            # pick first for demo if not specified
            if not cust_df.empty:
                customer = cust_df.iloc[0]['customer']
        row = cust_df[cust_df['customer'].str.lower() == str(customer).lower()]
        if row.empty:
            return QueryResult("sunset_versions_by_customer", f"No data for customer '{customer}'", {})
        services = row.iloc[0]['services']
        to_sunset = []
        for s in services:
            pf = port_df[(port_df['name'].str.lower() == s['name'].lower()) & (port_df['version'] == s['version'])]
            if not pf.empty and pf.iloc[0]['lifecycle'] in ("sunset", "deprecating"):
                to_sunset.append({"name": s['name'], "version": s['version'], "lifecycle": pf.iloc[0]['lifecycle']})
        return QueryResult("sunset_versions_by_customer", f"Sunset/Deprecating for {customer}: {to_sunset if to_sunset else 'None'}", {"customer": customer, "to_sunset": to_sunset})

    def service_impact(self, q: str) -> QueryResult:
        inc = self.data['incidents']
        # Simple: filter open incidents
        open_inc = inc[inc['status'].isin(["open", "investigating"])]
        # redaction for customers
        redacted = redact(open_inc, role=self.role)
        count = len(redacted)
        return QueryResult("service_impact", f"Active incidents: {count}", {"incidents": redacted.to_dict(orient='records')})

    def portfolio_gaps(self, q: str) -> QueryResult:
        m = re.search(r"customer\s+([\w\-\s]+)", q, re.I)
        customer = m.group(1).strip() if m else None
        cust_df = self.data['customers']
        port_df = self.data['portfolio']
        if customer is None and not cust_df.empty:
            customer = cust_df.iloc[0]['customer']
        row = cust_df[cust_df['customer'].str.lower() == str(customer).lower()]
        if row.empty:
            return QueryResult("portfolio_gaps", f"No data for customer '{customer}'", {})
        have = { (s['name'].lower(), s['version']) for s in row.iloc[0]['services'] }
        # gaps: for each service, if recommended_version newer than what is installed
        gaps = []
        for _, r in port_df.iterrows():
            key = (r['name'].lower(), r['version'])
            if r['recommended'] and not any(r['name'].lower() == h[0] and r['version'] == h[1] for h in have):
                # If the customer uses the service but older version, create a gap entry
                # Identify current version if any
                current = [s for s in row.iloc[0]['services'] if s['name'].lower() == r['name'].lower()]
                if current:
                    gaps.append({
                        'service': r['name'],
                        'current_versions': [c['version'] for c in current],
                        'recommended': r['version'],
                        'benefit': r.get('benefit', 'Performance and reliability improvements')
                    })
        return QueryResult("portfolio_gaps", f"Gaps for {customer}: {len(gaps)} found", {"customer": customer, "gaps": gaps})

    def answer(self, q: str) -> QueryResult:
        intent = self.classify(q)
        if intent == 'who_uses_service':
            return self.who_uses_service(q)
        if intent == 'sunset_versions_by_customer':
            return self.sunset_versions_by_customer(q)
        if intent == 'service_impact':
            return self.service_impact(q)
        if intent == 'portfolio_gaps':
            return self.portfolio_gaps(q)
        return QueryResult('generic', 'Try asking about customers using a service, sunset versions, active incidents, or portfolio gaps.', {})
