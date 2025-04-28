import http.client
import json
import os
import pytest
import shutil
import subprocess
import sys
import time 
import urllib
import sqlite3
from squirrel_db import SquirrelDB

todo = pytest.mark.skip(reason='TODO: pending spec')


def describe_squirrel_server():

    @pytest.fixture(autouse=True)
    def setup_and_cleanup_database():
        shutil.copyfile('system_tests/squirrel_db.db.template', 'system_tests/squirrel_db.db')
        conn = sqlite3.connect('system_tests/squirrel_db.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS squirrels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                size TEXT NOT NULL
            );
        ''')
        conn.commit()
        conn.close()

        yield
        os.remove('system_tests/squirrel_db.db')
    
    @pytest.fixture(autouse=True, scope='session')
    def start_and_stop_server():
        proc = subprocess.Popen([sys.executable, 'system_tests/squirrel_server.py'])
        time.sleep(0.1)
        yield
        proc.kill()

    @pytest.fixture
    def http_client():
        conn = http.client.HTTPConnection('localhost:8080')
        return conn
    
    @pytest.fixture
    def request_body():
        return urllib.parse.urlencode({'name': 'Sam', 'size': 'large'})
    
    @pytest.fixture
    def request_headers():
        return { 'Content-Type' : 'application/x-www-form-urlencoded'}
    
    @pytest.fixture
    def db():
        return SquirrelDB()
    
    @pytest.fixture
    def make_a_squirrel(db):
        db.createSquirrel("Fred", "small")

    '''@pytest.fixture
    def update_a_squirrel(db):
        db.createSquirrel("Fred", "small")
        db.updateSquirrel(1, "Chippy", "large")'''

    def describe_get_squirrels():

        def it_returns_200_status_code(http_client):
            http_client.request("GET", "/squirrels")
            response = http_client.getresponse()
            http_client.close()
            assert response.status == 200

        def it_returns_json_content_type_header(http_client):
            http_client.request("GET", "/squirrels")
            response = http_client.getresponse()
            http_client.close()
            assert response.getheader('Content-Type') == "application/json"

        def it_returns_empty_json_array(http_client):
            http_client.request("GET", "/squirrels")
            response = http_client.getresponse()
            response_body = response.read()
            http_client.close()

            assert json.loads(response_body) == []

        def it_returns_json_array_with_one_squirrel(http_client, make_a_squirrel):
            http_client.request("GET", "/squirrels")
            response = http_client.getresponse()
            response_body = response.read()
            http_client.close()

            assert json.loads(response_body) == [{ 'id': 1, 'name': 'Fred', 'size': 'small'}]
        
        def describe_when_given_unknown_collection():

            def it_returns_404_response(http_client):
                http_client.request("GET", "/bears")
                response = http_client.getresponse()
                http_client.close()
                assert response.status == 404

    def describe_get_squirrel():

        def it_returns_200_status_code(http_client, make_a_squirrel):
            http_client.request("GET", "/squirrels/1")
            response = http_client.getresponse()
            http_client.close()
            assert response.status == 200

        def it_returns_json_content_type_header(http_client, make_a_squirrel):
            http_client.request("GET", "/squirrels/1")
            response = http_client.getresponse()
            http_client.close()
            assert response.getheader('Content-Type') == "application/json"

        def it_returns_the_correct_squirrel(http_client, make_a_squirrel, db):
            http_client.request("GET", "/squirrels/1")
            response = http_client.getresponse()
            http_client.close()

            assert response.status == 200
            assert db.getSquirrel(1) == {'id': 1, 'name': 'Fred', 'size': 'small'}
        
        def describe_when_given_unknown_squirrel():

            def it_returns_404_response(http_client):
                http_client.request("GET", "/squirrels/1")
                response = http_client.getresponse()
                http_client.close()
                assert response.status == 404
        
        def describe_when_given_unknown_collection():

            def it_returns_404_response(http_client):
                http_client.request("GET", "/bears")
                response = http_client.getresponse()
                http_client.close()
                assert response.status == 404

    def describe_create_squirrel():

        def it_returns_201_status_code(http_client, request_body, request_headers):
            http_client.request("POST", "/squirrels", request_body, request_headers)
            response = http_client.getresponse()
            http_client.close()

            assert response.status == 201
        
        def it_creates_the_squirrel_in_database(http_client, request_body, request_headers, db):
            http_client.request("POST", "/squirrels", request_body, request_headers)
            response = http_client.getresponse()
            http_client.close()

            assert response.status == 201
            assert db.getSquirrels() == [{'id': 1, 'name': 'Sam', 'size': 'large'}]

        def describe_when_given_an_id():

            def it_returns_404_response(http_client, request_body, request_headers):
                http_client.request("POST", "/squirrels/1", request_body, request_headers)
                response = http_client.getresponse()
                http_client.close()

                assert response.status == 404
        
        def describe_when_given_unknown_collection():

            def it_returns_404_response(http_client, request_body, request_headers):
                http_client.request("POST", "/bears", request_body, request_headers)
                response = http_client.getresponse()
                http_client.close()

                assert response.status == 404
    
    def describe_update_squirrel():

        def it_returns_204_status_code(http_client, make_a_squirrel, request_body, request_headers):
            http_client.request("PUT", "/squirrels/1", request_body, request_headers)
            response = http_client.getresponse()
            http_client.close()

            assert response.status == 204

        def testing_the_update_in_database(http_client, make_a_squirrel, request_body, request_headers, db):
            db.updateSquirrel(1, "Sam", "large")
    
            squirrel = db.getSquirrel(1)
            assert squirrel == {'id': 1, 'name': 'Sam', 'size': 'large'}
        
        def it_updates_the_squirrel_in_database(http_client, make_a_squirrel, request_body, request_headers, db):
            assert db.getSquirrel(1) == {'id': 1, 'name': 'Fred', 'size': 'small'}
            http_client.request("PUT", "/squirrels/1", request_body, request_headers)
            response = http_client.getresponse()
            http_client.close()

            assert response.status == 204
            assert db.getSquirrel(1) == {'id': 1, 'name': 'Sam', 'size': 'large'}
        
        def describe_when_given_unknown_collection():

            def it_returns_404_response(http_client, request_body, request_headers):
                http_client.request("PUT", "/bears/1", request_body, request_headers)
                response = http_client.getresponse()
                http_client.close()

                assert response.status == 404
        
        def describe_when_given_unknown_squirrel():

            def it_returns_404_response(http_client, request_body, request_headers):
                http_client.request("PUT", "/squirrels/1", request_body, request_headers)
                response = http_client.getresponse()
                http_client.close()

                assert response.status == 404
        
        def describe_when_not_given_id():

            def it_returns_404_response(http_client, request_body, request_headers):
                http_client.request("PUT", "/squirrels", request_body, request_headers)
                response = http_client.getresponse()
                http_client.close()

                assert response.status == 404
    
    def describe_delete_squirrel():

        def it_returns_204_status_code(http_client, make_a_squirrel, request_body, request_headers):
            http_client.request("DELETE", "/squirrels/1", request_body, request_headers)
            response = http_client.getresponse()
            http_client.close()

            assert response.status == 204

        def testing_the_delete_in_database(http_client, make_a_squirrel, request_body, request_headers, db):
            db.deleteSquirrel(1)
    
            squirrel = db.getSquirrel(1)
            assert squirrel is None

        def it_deletes_the_squirrel_in_database(http_client, make_a_squirrel, request_body, request_headers, db):
            assert db.getSquirrel(1) == {'id': 1, 'name': 'Fred', 'size': 'small'}
            http_client.request("DELETE", "/squirrels/1", request_body, request_headers)
            response = http_client.getresponse()
            http_client.close()

            assert response.status == 204
            assert db.getSquirrels() == []

        def describe_when_given_unknown_collection():

            def it_returns_404_response(http_client, request_body, request_headers):
                http_client.request("DELETE", "/bears/1", request_body, request_headers)
                response = http_client.getresponse()
                http_client.close()

                assert response.status == 404

        def describe_when_given_unknown_squirrel():

            def it_returns_404_response(http_client, request_body, request_headers):
                http_client.request("DELETE", "/squirrels/1", request_body, request_headers)
                response = http_client.getresponse()
                http_client.close()

                assert response.status == 404
        
        def describe_when_not_given_id():

            def it_returns_404_response(http_client, request_body, request_headers):
                http_client.request("DELETE", "/squirrels", request_body, request_headers)
                response = http_client.getresponse()
                http_client.close()

                assert response.status == 404