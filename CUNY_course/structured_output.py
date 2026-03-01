from dotenv import load_dotenv
import os
from openai import AzureOpenAI
from pydantic import BaseModel, Field
from CUNY_course.data_types.person import (
    Person,
    Address,
    Person2,
    RelationshipStatus,
    PersonWithRelationships,
)

load_dotenv()

client = AzureOpenAI(
    api_version="2025-03-01-preview",
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    timeout=30,
    max_retries=3,
)


def generate_structured_output(
    instructions: str, input: str, output_model: BaseModel
) -> BaseModel:
    response = client.responses.parse(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        instructions=instructions,
        input=[{"role": "user", "content": input}],
        text_format=output_model,
    )

    return response.output_parsed


text1 = """My name is John Doe. I am in my mid-thirties, 180.5 cm tall, and weigh about
150 pounds. I work as a software engineer. I live at 123 Main St on the
second floor, in New York City. I am currently not really sure about
my girlfriend, as she was weird on the phone last night and I am actually a bit tired
of her."""

text2 = "My name is Lasse Funder Andersen and that is all you need to know about me."

text3 = """My name is Hans. I have a very interesting love life. I am currently married
to Susanne on my third year. She is a wonderful person, but also a little boring, so I
have found myself a secret lover - A young 25 old beauty.
I have also been married twice before.
My first marriage lasted for 10 years, when sadly my wife Mary passed away. I was
devastated, but I eventually moved on and found love again in a feisty opera singer
called Anna - but it ended in a bitter divorce."""

instructions = """Extract information about a person from the input text
and structure it according to the Person data model."""

person_info = generate_structured_output(
    instructions=instructions,
    input=text3,
    output_model=PersonWithRelationships,
)
print(person_info.model_dump_json(indent=2, exclude_none=True))
