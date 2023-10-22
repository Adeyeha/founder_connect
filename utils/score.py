weights = {
'startup':{'investor_expertise': 0.025, 'investor_attributes': 0.0125, 'business_priorities': 0.1, 'founder_gender': 0.025, 'investment_round': 0.1, 'startup_industries': 0.1, 'startup_countries': 0.0125, 'business_models': 0.25, 'startup_stage': 0.1, 'engagement_lengths': 0.025, 'engagement_models': 0.05, 'investment_needed': 0.2, 'startup_age': 0.02, 'team_size': 0.02},
'investor' : {'investor_expertise': 0.025, 'preferred_attributes': 0.0125, 'preferred_business_priority': 0.1, 'preferred_founder_gender': 0.025, 'preferred_investment_round': 0.1, 'preferred_industry': 0.1, 'preferred_country': 0.0125, 'preferred_business_model': 0.25, 'preferred_business_stage': 0.1, 'preferred_engagement_length': 0.025, 'preferred_engagement_model': 0.05, 'investment_needed': 0.2, 'startup_age': 0.02, 'team_size': 0.02}
}

def calculate_match_score(investor_data, startup_data, reference, tolerance=0.1):
    metric_scores = {}  # Dictionary to store the scores of each metric

    # Common Metrics
    common_metrics = [
        ('investor_expertise', 'investor_expertise'),
        ('preferred_attributes', 'investor_attributes'),
        ('preferred_business_priority', 'business_priorities'),
        ('preferred_founder_gender', 'founder_gender'),
        ('preferred_investment_round', 'investment_round'),
        ('preferred_industry', 'startup_industries'),
        ('preferred_country', 'startup_countries'),
        ('preferred_business_model', 'business_models'),
        ('preferred_business_stage', 'startup_stage'),
        ('preferred_engagement_length', 'engagement_lengths'),
        ('preferred_engagement_model', 'engagement_models'),
    ]

    for investor_field, startup_field in common_metrics:
        reference_field = investor_field if reference.lower() == 'investor' else startup_field
        investor_value = investor_data.get(investor_field, [])
        startup_value = startup_data.get(startup_field, [])

        # Convert single values to list for consistency
        if not isinstance(investor_value, list):
            investor_value = [investor_value]
        if not isinstance(startup_value, list):
            startup_value = [startup_value]
        
        # Score increment for each matching item
        matching_items = set(investor_value) & set(startup_value)
        metric_score = (len(matching_items) / max(len(startup_value), len(startup_value))) * 100 if matching_items else 0
        metric_scores[reference_field] = metric_score  # Store the score of this metric in the dictionary

    # Numeric Metrics
    numeric_metrics = [
        ('min_investment', 'investment_needed', 'max_investment'),
        ('preferred_startup_age_min', 'startup_age', 'preferred_startup_age_max'),
        ('preferred_team_size_min', 'team_size', 'preferred_team_size_max')
    ]

    for min_field, value_field, max_field in numeric_metrics:
        min_value = investor_data.get(min_field, 0)
        value = startup_data.get(value_field, 0)
        max_value = investor_data.get(max_field, 0)

        metric_score = 100 if (min_value * (1 - tolerance)) <= value <= (max_value * (1 + tolerance)) else 0
        metric_scores[value_field] = metric_score  # Store the score of this metric in the dictionary

    return metric_scores  # Return the dictionary of metric scores


def calculate_weighted_average_score(scores, weights):
    weighted_sum = 0
    total_weight = 0

    for metric, score in scores.items():
        weight = weights.get(metric, 0)  # Get the weight of the metric, or 0 if not defined
        weighted_sum += score * weight
        total_weight += weight

    weighted_average = weighted_sum / total_weight if total_weight > 0 else 0
    return weighted_average


def generate_scores(investor_sample_data, startup_sample_data, reference, weights=weights, tolerance=0.1):
    scores = calculate_match_score(investor_sample_data, startup_sample_data, reference)
    weighted = calculate_weighted_average_score(scores,weights[reference.lower()])
    return scores,round(weighted,2)