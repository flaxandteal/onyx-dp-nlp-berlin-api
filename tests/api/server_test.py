

def test_health_check(test_client):
    response = test_client.get("/health")
    assert response.status_code == 200
    assert '"OK"' in response.text


def test_code_with_berlin(test_client_with_berlin):
    response = test_client_with_berlin.get("/berlin/code/UN-LOCODE-bg:blo")
    assert response.status_code == 200
    assert isinstance(response.json, dict)
    assert response.json == {
        "encoding": "UN-LOCODE",
        "id": "bg:blo",
        "key": "UN-LOCODE-bg:blo",
        "names": ["lyuliakovo"],
        "words": ["lyuliakovo"],
        "codes": ["blo"],
        "state": ["bg", "ISO-3166-1-bg"],
        "subdiv": ["02", "ISO-3166-2-bg:02"],
    }
    print(response.json)


def test_search_with_scores_with_berlin(test_client_with_berlin):
    response = test_client_with_berlin.get(
        "/berlin/search?q=Dentists+in+Lyuliakovo&state=BG&limit=2&with_scores=1"
    )
    assert response.status_code == 200
    assert isinstance(response.json, dict)
    assert response.json == {
        "matches": [{
            "loc": {
                "encoding": "UN-LOCODE",
                "id": "bg:blo",
                "key": "UN-LOCODE-bg:blo",
                "names": ["lyuliakovo"],
                "words": ["lyuliakovo"],
                "codes": ["blo"],
                "state": ["bg", "ISO-3166-1-bg"],
                "subdiv": ["02", "ISO-3166-2-bg:02"],
            },
            "match": {
                "offset": [12, 22],
                "score": 1010
            }
        }]
    }
    print(response.json)

def test_search_with_state_with_berlin(test_client_with_berlin):
    response = test_client_with_berlin.get(
        "/berlin/search?q=Lyuliakovo&state=BG&limit=2&with_scores=1"
    )
    assert response.status_code == 200
    assert isinstance(response.json, dict)
    assert response.json == {
        'matches': [{
            'loc': {
                'codes': ['blo'],
                'encoding': 'UN-LOCODE', 
                'id': 'bg:blo', 
                'key': 'UN-LOCODE-bg:blo', 
                'names': ['lyuliakovo'], 
                'state': ['bg', 'ISO-3166-1-bg'], 
                'subdiv': ['02', 'ISO-3166-2-bg:02'], 
                'words': ['lyuliakovo']
            }, 
            'match': {
                'offset': [0, 10], 
                'score': 1010
            }
        }]
    }
    print(response.json)


def test_search_with_state(test_client):
    response = test_client.get("/berlin/search?q=Manch&state=GB&limit=2&with_scores=1")
    print(response.json)
    assert response.status_code == 200
    assert isinstance(response.json, dict)
    assert response.json == {
        'matches': [{
            'loc': {
                'codes': ['mnc'], 
                'encoding': 'B', 
                'id': 'X', 
                'key': 'A', 
                'names': ['manc'], 
                'state': ['gb', 'gb-nom'], 
                'subdiv': ['mac', 'gb-mac-name'], 
                'words': ['Manchester']
            }, 
            'match': {
                'offset': [0, 10], 
                'score': 1010
            
            }
        }]
    }
    print(response.json)

