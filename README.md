# rest-api-intern-task-
Ege Meriç Erdoğan(Rest-Api Backend Task)  


 ## Example request:
```sh
curl -i --header "Content-Type: application/json"   --request POST   --data '{"text":"ege meric erdogan"}'   http://localhost:8000/analyze
```
## Output:
```json
{
    "wordCount": 3,
    "letters": 15,
    "longest": "erdogan",
    "avgLength": 5.0,
    "duration": 0.8999999999999999,
    "medianWordLength": 5,
    "medianWord": "meric",
    "topfivewords": [
        "ege",
        "meric",
        "erdogan"
    ]
}
``` 
## or you can request by "analysis" keyword and you can put options in a array
```sh
curl --header "Content-Type: application/json"   --request POST   --data '{"text":"ege meric erdogan","analysis": ["medianWord"]}'   http://127.0.0.1:8000/analyze
```
## Response:
```json
{
    "medianWord": "meric"
}
```
