### Required Libraries ###
from datetime import datetime
from dateutil.relativedelta import relativedelta

### Functionality Helper Functions ###
def parse_int(n):
    """
    Securely converts a non-integer value to integer.
    """
    try:
        return int(n)
    except ValueError:
        return float("nan")


def build_validation_result(is_valid, violated_slot, message_content):
    """
    Define a result message structured as Lex response.
    """
    if message_content is None:
        return {"isValid": is_valid, "violatedSlot": violated_slot}

    return {
        "isValid": is_valid,
        "violatedSlot": violated_slot,
        "message": {"contentType": "PlainText", "content": message_content},
    }

def get_investmetn_recommendation(risk_level):
    """
    Returns the investment recommendation based on risk profile.
    """
    risk_levels = {
        "None": "90% bonds (AGG), 10% cash in Money Market Savings Account, 0% equities",
        "Very Low": "90% bonds (BIV), 5% Cash in Money Market Savings Account, 5% equities (BRK.A)",
        "Low": "80% bonds (AGG), 15% equities (AAPL), 5% Cash in Money Market Savings Account",
        "Medium": "40% bonds (AGG), 60% equities split equally across (SPY) (AAPL)",
        "High": "10% bonds (AGG), 90% equities split equally across (SPY) (AAPL) (TSLA)",
        "Very High": "0% bonds (AGG), 100% equities split equally across (SPY) (TSLA) (GME) (AAPL) (DIS) (AMC)"
    }
    
        return risk_levels[risk_level.lower()]


def validate_data(age, investment_amount, intent_request):
    """
    Validation check on data entered.
    """
    
    #validate age is valid
    if age is not None:
        age = parse_int(
            age
        )
        if age < 0:
            return build_validation_result(
                False,
                "age",
                "This tools designed for individuals between 0 and 65 years of age, please enter an age greater than 0",
            )
        elif  age >= 65:
            return build_validation_result(
                False,
                "age",
                "This tools designed for individuals between 0 and 65 years of age, please enter an age less than 65.",
            )
        
    #is investment at min $5000
    if investment_amount is not None:
        investment_amount - parse_int(investment_amount)
        if investment_amount < 5000:
            return build_valdiation_results(
                False,
                "investmentAmount",
                "Please provide a greater amount, the minimum investment amount is $5,000.",
            )
    
    return build_validation_restult(True, None, None)


### Dialog Actions Helper Functions ###
def get_slots(intent_request):
    """
    Fetch all the slots and their values from the current intent.
    """
    return intent_request["currentIntent"]["slots"]


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    """
    Defines an elicit slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": intent_name,
            "slots": slots,
            "slotToElicit": slot_to_elicit,
            "message": message,
        },
    }


def delegate(session_attributes, slots):
    """
    Defines a delegate slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {"type": "Delegate", "slots": slots},
    }


def close(session_attributes, fulfillment_state, message):
    """
    Defines a close slot type response.
    """

    response = {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": message,
        },
    }

    return response


### Intents Handlers ###
def recommend_portfolio(intent_request):
    """
    Performs dialog management and fulfillment for recommending a portfolio.
    """

    first_name = get_slots(intent_request)["firstName"]
    age = get_slots(intent_request)["age"]
    investment_amount = get_slots(intent_request)["investmentAmount"]
    risk_level = get_slots(intent_request)["riskLevel"]
    source = intent_request["invocationSource"]

    if source == "DialogCodeHook":
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt
        # for the first violation detected.

        ### YOUR DATA VALIDATION CODE STARTS HERE ###

        ### YOUR DATA VALIDATION CODE ENDS HERE ###

        # Fetch current session attibutes
        output_session_attributes = intent_request["sessionAttributes"]

        return delegate(output_session_attributes, get_slots(intent_request))

    # Get the initial investment recommendation

    ### YOUR FINAL INVESTMENT RECOMMENDATION CODE STARTS HERE ###
    if risk_level == "None":
        initial_recommendation = "90% bonds (AGG), 10% cash in Money Market Savings Account, 0% equities"
    elif risk_level == "Very Low":
        initial_recommendation = "90% bonds (BIV), 5% Cash in Money Market Savings Account, 5% equities (BRK.A)"
    elif risk_level == "Low":
        initial_recommendation = "80% bonds (AGG), 15% equities (AAPL), 5% Cash in Money Market Savings Account"
    elif risk_level == "Medium":
        initial_recommendation = "40% bonds (AGG), 60% equities split equally across (SPY) (AAPL)"
    elif risk_level == "High":
        initial_recommendation = "10% bonds (AGG), 90% equities split equally across (SPY) (AAPL) (TSLA)"
    elif risk_level == "Very High":
        initial_recommendation = "0% bonds (AGG), 100% equities split equally across (SPY) (TSLA) (GME) (AAPL) (DIS) (AMC)"
    else:
        initial_recommendation ="risk_level not recognized
    ### YOUR FINAL INVESTMENT RECOMMENDATION CODE ENDS HERE ###

    # Return a message with the initial recommendation based on the risk level.
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": """{} thank you for your information;
            based on the risk level you defined, my recommendation is to choose an investment portfolio with {}
            """.format(
                first_name, initial_recommendation
            ),
        },
    )


### Intents Dispatcher ###
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    intent_name = intent_request["currentIntent"]["name"]

    # Dispatch to bot's intent handlers
    if intent_name == "RecommendPortfolio":
        return recommend_portfolio(intent_request)

    raise Exception("Intent with name " + intent_name + " not supported")


### Main Handler ###
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    return dispatch(event)
