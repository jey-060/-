from flask import Flask, render_template, request
import urllib.parse

app = Flask(__name__)

traits_storage = []

@app.route('/')
def index():
    return render_template('index.html', traits_list=traits_storage)

@app.route('/search', methods=['GET'])
def search_wikipedia():
    animal_name = request.args.get('animal')
    
    if animal_name:
        base_url = "https://ko.wikipedia.org/wiki/"
        encoded_name = urllib.parse.quote(animal_name)
        wikipedia_url = base_url + encoded_name
        
        return render_template('index.html', 
                               wikipedia_url=wikipedia_url, 
                               animal_name=animal_name, 
                               traits_list=traits_storage)
    
    return render_template('index.html', traits_list=traits_storage)

@app.route('/add_trait', methods=['POST'])
def add_trait():
    new_trait = request.form.get('trait')
    
    if new_trait:
        traits_storage.append(new_trait)
        
    return render_template('index.html', traits_list=traits_storage)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)