from django.shortcuts import render
from .models import City, Person
from neo4j import GraphDatabase
import re


AURA_CONNECTION_URI = "neo4j+ssc://d5e585c5.databases.neo4j.io"
AURA_USERNAME = "neo4j"
AURA_PASSWORD = "d3zda0Dd1DzVr_m7GfsPik_YFGlM-qfmdeCjZrxkKFc"

drivers = GraphDatabase.driver(
    AURA_CONNECTION_URI,
    auth=(AURA_USERNAME, AURA_PASSWORD)
)

def city_list(request):
    cypher_query = "MATCH (city:City) RETURN city"
    with drivers as driver:
        result = driver.execute_query(cypher_query)
        
    result_string = str(result)
    
    city_names = re.findall(r"'name': '(.*?)'", result_string)
    
    return render(request, 'city_list.html', {'cities': city_names})

def person_list(request):
    cypher_query = "MATCH (person:Person) RETURN person"
    with drivers as driver:
        result = driver.execute_query(cypher_query)
    
    result_string = str(result)
    
    matches = re.findall(r"'name': '(.*?)', 'age': (\d+)", result_string)
    
    people = [{'name': name, 'age': int(age)} for name, age in matches]
    
    return render(request, 'person_list.html', {'people': people})

def index(request):
    return render(request, 'index.html')

def list_cities_and_users(request):
    cypher_query = (
        "MATCH (person:Person)-[:LIVES_IN]->(city:City)"
        "RETURN city.name AS cityName, COLLECT({name: person.name, age: person.age}) AS residents;"
    )
    
    with drivers as driver:
        driver.verify_connectivity()
        result = driver.execute_query(cypher_query)
        
    driver.close() 
    
    result_string = str(result)
    
    city_pattern = re.compile(r"cityName='(.*?)'")
    residents_pattern = re.compile(r"residents=\[(.*?)\]")

    city_names = re.findall(city_pattern, result_string)

    residents_matches = re.findall(residents_pattern, result_string)
    residents_data = [eval(match) for match in residents_matches] 
    
    cities_with_residents = [{'city': city, 'residents': residents} for city, residents in zip(city_names, residents_data)]

    print(cities_with_residents)
    
    return render(request, 'city_user_list.html', {'cities_with_residents': cities_with_residents})

def add_person(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = int(request.POST.get('age'))

        with drivers as driver:
            driver.execute_query("CREATE (:Person {name: $name, age: $age})", name=name, age=age)

        driver.close() 
        
    return render(request, 'add_person.html')

def add_city(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        with drivers as driver:
            driver.execute_query("CREATE (:City {name: $name})", name=name)

    return render(request, 'add_city.html')

def add_relationship(request):
    if request.method == 'POST':
        person_name = request.POST.get('person_name')
        city_name = request.POST.get('city_name')

        with drivers as driver:
            driver.execute_query("MATCH (p:Person {name: $person_name}), (c:City {name: $city_name}) "
                            "CREATE (p)-[:LIVES_IN]->(c)", person_name=person_name, city_name=city_name)

    return render(request, 'add_relationship.html')