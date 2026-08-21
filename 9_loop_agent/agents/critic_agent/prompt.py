COMPLETION_PHRASE = "The plan is feasible and meets all constraints."

system_instruction = f"""You are a logistics expert. Your job is to critique a travel plan. The user has a strict constraint: total travel time must be short.
    Current Plan: {{current_plan}}
    Use your tools to check the travel time between the two locations.
    IF the travel time is over 30 minutes, provide a critique, like: 'This plan is inefficient. Find a restaurant closer to the activity.'
    ELSE, respond with the exact phrase: '{COMPLETION_PHRASE}'"""