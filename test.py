import requests

BASE = "http://127.0.0.1:5000/"

data = [{"senderName": "Angel",
        "receiverName": "Pablo",
        "category": "Payments",
        "priorityWeight": 50,
        "impactToUser": "This will do something.",
        "body": "User, please pay...Now!"
        },
        {"senderName": "Juan",
        "receiverName": "Pedro",
        "category": "Account Updates",
        "priorityWeight": 10,
        "impactToUser": "Update account.",
        "body": "User, please update..Now!"
        },
        {"senderName": "Jose",
        "receiverName": "Jesus",
        "category": "Reminder",
        "priorityWeight": 1,
        "impactToUser": "This will do something.",
        "body": "You have been reminded of something."
        }]

for i in range(len(data)):
    response = requests.put(BASE + "actionItem/" + str(i), data[i])
    print(response.json())

raw_input()
response = requests.get(BASE + "actionItem/2")
print(response.json())

response = requests.patch(BASE + "actionItem/2", {"priorityWeight": 50})
print(response.json())