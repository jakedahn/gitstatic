import json
import flask

app = flask.Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True


@app.route('/')
def index():
    return 'welcome to gitstatic'

@app.route('/build', methods=['POST'])
def build():
  params = flask.request.values.to_dict()

  if params.get('git_url'):
    #FIXME(jake): kickoff build here
    res = dict(msg='git url received')
    return json.dumps(res), 202


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888)
