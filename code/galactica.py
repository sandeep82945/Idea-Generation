import galai as gal

model = gal.load_model("mini")
def inference(text):
    response = model.generate(text)
    return response

    