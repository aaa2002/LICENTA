from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from LangChain_Workflow import pipeline
import uvicorn
from src.agents.entityExtractor.extractor import Extractor
from src.agents.queryGen.qGen import QueryGenerator

extractor = Extractor()
query_generator = QueryGenerator()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class InputData(BaseModel):
    text: str


@app.post("/predict")
async def predict(data: InputData):
    # try:
    result = pipeline.invoke({"text": data.text})
    return result


# except Exception as e:
#     return {"error": str(e)}

@app.post("/generate-query")
async def generate_query(data: InputData):
    text = data.text

    entities = extractor.extract(text)
    print(f"Extracted Entities: {entities}")

    transformed_query = query_generator.generate(entities)
    print(f"Transformed Query: {transformed_query}")

    return transformed_query


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
