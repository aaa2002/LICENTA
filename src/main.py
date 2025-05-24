from LangChain_Workflow import pipeline

if __name__ == "__main__":
    # input_text = "Breaking news: Aliens have landed in Times Square to discuss trade deals."
    input_text = "Donald Trump is the 45th President of the United States and was impeached twice."
    result = pipeline.invoke({"text": input_text})
    print(result)
