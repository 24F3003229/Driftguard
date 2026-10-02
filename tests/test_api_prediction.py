from src.api.predict import load_model, make_prediction

def test_make_prediction(): 
    # saved baseline model ko laod kr rhe hai. 
    model = load_model()

    # ek sample customer ka input create kr rhe hai.
    # ye vhi 16 features hai jo model training ke time use hue the.
    input_data = {
        "age": 30,
        "job": "technician",
        "marital": "single",
        "education": "tertiary",
        "default": "no",
        "balance": 1500,
        "housing": "yes",
        "loan": "no",
        "contact": "cellular",
        "day": 15,
        "month": "may",
        "duration": 300,
        "campaign": 1,
        "pdays": -1,
        "previous": 0,
        "poutcome": "unknown",
    }

    # model se prediction generate kr rhe hai.
    result = make_prediction(model, input_data)

    # check kr rhe hai ki prediction response me required fields hai.
    assert "prediction" in result
    assert "probability" in result

    # prediction sirf 0 ya 1 hona chahiye
    assert result["prediction"] in [0, 1]

    # probability 0 or 1 ke bich me honi chahiye
    assert 0 <= result["probability"] <= 1