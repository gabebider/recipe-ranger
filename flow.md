1. Get recipe either from url or from recipe search
2. Parse recipe
3. Output ingredients
4. Option to see all steps or just the first step
5. For all steps
    1. Output text
    2. Get input
    3. If input is question
        - TODO - Make list of question words
        1. Determine if question is about ingredients
            1. What is X?
            2. What can I substitute for X?
        2. Determine if question is about steps
            3. Determine if question is about parameters
                1. What is the temperature?
                2. What is the time?
                3. How much of X?
                4. What is X?
                5. What
    4. If input is navigation
        1. TODO - Make list of navigation words
        2. Determine if navigation is about steps
            1. Next
            2. Previous
            3. Repeat
            4. Skip
            5. Go back
            6. Okay
        3. Do navigation
    

- TODO
    - Include case where user asks for a new recipe
    - Include case where user asks for all steps after selecting just the first step
    - Include case where user ends or says finished or exit etc.
    