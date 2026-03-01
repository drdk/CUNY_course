# delete just one comma, and see what happens...

person = {
    "name": "Lasse",
    "age": 38,
    "city": "Copenhagen",
    "is_data_scientist": True,
    "skills": ["Python", "MongoDB", "RAG", "LLMs"],
    "contact": {"email": "lasse@example.com", "phone": None},
}

print("I know that this person's name is " + person["name"])
