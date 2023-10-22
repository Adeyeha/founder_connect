class Startup:
    def __init__(self, name, industry, country, amount_needed, business_priority):
        self.name = name
        self.industry = industry
        self.country = country
        self.amount_needed = amount_needed
        self.business_priority = business_priority

class Investor:
    def __init__(self, name, preferred_industry, preferred_country, min_investment, max_investment, business_priority):
        self.name = name
        self.preferred_industry = preferred_industry
        self.preferred_country = preferred_country
        self.min_investment = min_investment
        self.max_investment = max_investment
        self.business_priority = business_priority

def dynamic_filter(investors, startups, filter_criteria):
    matches = []

    for startup in startups:
        for investor in investors:
            # Check industry match
            if startup.industry not in investor.preferred_industry:
                continue

            # Check country match
            if startup.country not in investor.preferred_country:
                continue

            # Check investment amount compatibility
            if not (investor.min_investment <= startup.amount_needed <= investor.max_investment):
                continue

            # Check business priority match
            if set(startup.business_priority).isdisjoint(set(investor.business_priority)):
                continue

            # If all checks pass, append to matches
            matches.append((investor.name, startup.name))
    
    # Apply additional filter criteria if provided
    if filter_criteria:
        matches = [match for match in matches if all(criterion(match) for criterion in filter_criteria)]

    return matches
